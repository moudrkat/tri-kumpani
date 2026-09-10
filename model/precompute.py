"""Qwen 3.5 0.8B přečte čtyři verše a my si zapíšeme, co se s tokeny děje uvnitř.

Qwen 3.5 je hybrid: z 24 vrstev má jen každá čtvrtá (4, 8, 12, 16, 20, 24) klasickou
attention s maticí N × N, ostatní jsou lineární (Gated DeltaNet) a žádnou matici nemají.
Zapisujeme tedy jen těch šest.

Výstup model/qwen.json:
  tokeny          id + text každého tokenu
  att_vrstvy      čísla vrstev (od 1), které mají plnou attention
  attention       len(att_vrstvy) × 8 hlav × N × N, kvantované na bajt (0..255 = 0..1), base64
  logit_lens      pro každou z 24 vrstev a pozici top-3 tokeny, které by model hádal jako další
  dalsi_vers      pro čínský originál, anglický překlad a celé Mathesiovy Tři kumpány:
                  celý text po řádcích a jak by model pokračoval, až čtyři verše. Pro každou
                  teplotu šest vzorků (každý = seznam řádků) a přesné pravděpodobnosti 40
                  nejnadějnějších prvních tokenů při té teplotě (teplota 0 = greedy, jeden vzorek)

    uv sync --extra model
    uv run python model/precompute.py      # na GPU, když je; na CPU to trvá pár minut
"""
import base64
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen3.5-0.8B-Base"
KAM = Path(__file__).resolve().parent / "qwen.json"
BASNE = Path(__file__).resolve().parent.parent / "basne"
TEXTY = {"zh": "yue_xia_du_zhuo.txt", "en": "yue_xia_du_zhuo_en.txt", "cs": "tri_kumpani.txt"}

cely = {k: BASNE.joinpath(f).read_text(encoding="utf-8").rstrip("\n") for k, f in TEXTY.items()}
verse = [v.rstrip(",") for v in cely["cs"].splitlines()[:4]]
text = "\n".join(verse)

tok = AutoTokenizer.from_pretrained(MODEL)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32, attn_implementation="eager").to(device)
model.eval()
print("model:", MODEL, "na", device)

ids = tok(text, return_tensors="pt").input_ids.to(device)
with torch.no_grad():
    out = model(ids, output_attentions=True, output_hidden_states=True)

tokeny = [{"id": int(i), "s": tok.decode([int(i)])} for i in ids[0]]
n = len(tokeny)
print("tokenů:", n)

# attention: (vrstva, hlava, i, j) -> uint8; jen vrstvy, které ji mají
typy = model.config.layer_types
att_vrstvy = [i + 1 for i, t in enumerate(typy) if t == "full_attention"]
att = torch.stack([a[0] for a in out.attentions if a is not None])   # L_att × H × N × N
assert att.shape[0] == len(att_vrstvy), (att.shape, att_vrstvy)
H = att.shape[1]
att_u8 = (att.clamp(0, 1) * 255).round().to(torch.uint8).cpu().numpy()
print("attention:", att_u8.shape, "vrstvy", att_vrstvy)

# logit lens: finální norma + lm_head na hidden state každé vrstvy
norm, head = model.model.norm, model.lm_head
lens = []
for l, h in enumerate(out.hidden_states[1:]):               # hidden_states[0] je embedding
    with torch.no_grad():
        logits = head(norm(h[0]))
        p = torch.softmax(logits, dim=-1)
        top = torch.topk(p, 3, dim=-1)
    lens.append([[{"s": tok.decode([int(t)]), "p": round(float(pp), 3)} for pp, t in zip(top.values[i], top.indices[i])]
                 for i in range(n)])

# další verš: čistá teplota, bez top-p a top-k, ať posuvník v appce říká pravdu
TEPLOTY = [0.3, 0.6, 0.8, 1.0, 1.3, 1.7]
cisty = dict(top_p=1.0, top_k=0, repetition_penalty=1.0, max_new_tokens=96)
VERSU = 4


def dopis(text):
    """Model dostane celý text a řádek navíc; vrátí kandidáty prvního tokenu a verše po teplotách."""
    prompt = tok(text + "\n", return_tensors="pt").input_ids.to(device)

    def radek(seq):
        """Prvních pár neprázdných řádků, co model dopsal."""
        radky = [r.strip() for r in tok.decode(seq[prompt.shape[1]:], skip_special_tokens=True).split("\n")]
        return [r for r in radky if r][:VERSU]

    with torch.no_grad():
        logity = model(prompt).logits[0, -1].float()
        top = torch.topk(logity, 40)
        kandidati = [{"s": tok.decode([int(i)]), "logit": round(float(v), 3)} for v, i in zip(top.values, top.indices)]
        g = model.generate(prompt, do_sample=False, **cisty)
        teploty = [{"t": 0, "verse": [radek(g[0])],
                    "p": [1.0 if int(i) == int(top.indices[0]) else 0.0 for i in top.indices]}]
        for t in TEPLOTY:
            torch.manual_seed(7)
            s = model.generate(prompt, do_sample=True, temperature=t, num_return_sequences=6, **cisty)
            p = torch.softmax(logity / t, dim=-1)
            teploty.append({"t": t, "verse": [radek(x) for x in s], "p": [round(float(p[i]), 4) for i in top.indices]})
    return {"kandidati": kandidati, "teploty": teploty}


dalsi = {}
for k, t in cely.items():
    dalsi[k] = dict(radky=t.splitlines(), **dopis(t))
    for z in dalsi[k]["teploty"]:
        print(f"{k} teplota {z['t']}: {z['verse']}")

KAM.write_text(json.dumps({
    "model": MODEL,
    "verse": verse,
    "tokeny": tokeny,
    "vrstvy": len(typy), "att_vrstvy": att_vrstvy, "hlavy": H,
    "attention": base64.b64encode(att_u8.tobytes()).decode(),
    "logit_lens": lens,
    "dalsi_vers": dalsi,
}, ensure_ascii=False), encoding="utf-8")
print("zapsáno", KAM, KAM.stat().st_size // 1024, "kB")

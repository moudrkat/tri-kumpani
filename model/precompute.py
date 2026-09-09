"""Qwen 2.5 0.5B přečte čtyři verše a my si zapíšeme, co se s tokeny děje uvnitř.

Výstup model/qwen.json:
  tokeny          id + text každého tokenu
  attention       24 vrstev × 14 hlav × N × N, kvantované na bajt (0..255 = 0..1), base64
  logit_lens      pro každou vrstvu a pozici top-3 tokeny, které by model hádal jako další
  pokracovani     jak by model pokračoval (pátý verš), greedy a jeden vzorek

    uv sync --extra model
    uv run python model/precompute.py
"""
import base64
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B"
KAM = Path(__file__).resolve().parent / "qwen.json"
BASNE = Path(__file__).resolve().parent.parent / "basne" / "tri_kumpani.txt"

verse = [v.rstrip(",") for v in BASNE.read_text(encoding="utf-8").split("\n\n")[0].splitlines()[:4]]
text = "\n".join(verse)

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32, attn_implementation="eager")
model.eval()

ids = tok(text, return_tensors="pt").input_ids
with torch.no_grad():
    out = model(ids, output_attentions=True, output_hidden_states=True)

tokeny = [{"id": int(i), "s": tok.decode([int(i)])} for i in ids[0]]
n = len(tokeny)
print("tokenů:", n)

# attention: (vrstva, hlava, i, j) -> uint8
att = torch.stack([a[0] for a in out.attentions])          # L × H × N × N
L, H = att.shape[:2]
att_u8 = (att.clamp(0, 1) * 255).round().to(torch.uint8).numpy()
print("attention:", att_u8.shape)

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

# pokračování: pátý verš
prompt = tok(text + "\n", return_tensors="pt").input_ids
with torch.no_grad():
    g = model.generate(prompt, max_new_tokens=24, do_sample=False)
    torch.manual_seed(7)
    s = model.generate(prompt, max_new_tokens=24, do_sample=True, temperature=0.8, top_p=0.9)
greedy = tok.decode(g[0][prompt.shape[1]:]).split("\n")[0]
sampled = tok.decode(s[0][prompt.shape[1]:]).split("\n")[0]
print("greedy:", greedy)
print("vzorek:", sampled)

KAM.write_text(json.dumps({
    "model": MODEL,
    "verse": verse,
    "tokeny": tokeny,
    "vrstvy": L, "hlavy": H,
    "attention": base64.b64encode(att_u8.tobytes()).decode(),
    "logit_lens": lens,
    "pokracovani": {"greedy": greedy, "vzorek": sampled},
}, ensure_ascii=False), encoding="utf-8")
print("zapsáno", KAM, KAM.stat().st_size // 1024, "kB")

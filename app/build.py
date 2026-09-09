"""Slepí appku: app/template.html + model/qwen.json + merges tokenizeru -> app/index.html.

Appka běží celá v prohlížeči bez sítě, proto je všechno v jednom souboru:
tokenizer Qwen 2.5 (jen merges, slovník se z nich doskládá) a to, co model
zapsal při čtení básně (model/precompute.py).

    uv run python app/build.py
"""
import json
from pathlib import Path

from huggingface_hub import hf_hub_download

TADY = Path(__file__).resolve().parent
QWEN = TADY.parent / "model" / "qwen.json"

tok = json.load(open(hf_hub_download("Qwen/Qwen2.5-0.5B", "tokenizer.json"), encoding="utf-8"))
merges = tok["model"]["merges"]
if not isinstance(merges[0], str):
    merges = [" ".join(m) for m in merges]

html = (TADY / "template.html").read_text(encoding="utf-8")
# části vícebajtových znaků dekódují na U+FFFD; do JS jde jako escape, aby ho hosting nezahodil
html = html.replace("__QWEN__", QWEN.read_text(encoding="utf-8").replace("\ufffd", "\\ufffd"))
html = html.replace("__MERGES__", json.dumps("\n".join(merges), ensure_ascii=False))
(TADY / "index.html").write_text(html, encoding="utf-8")
print("zapsáno app/index.html", (TADY / "index.html").stat().st_size // 1024, "kB")

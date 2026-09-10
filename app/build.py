"""Slepí appku: app/template.html + model/qwen.json -> app/index.html.

Appka běží celá v prohlížeči bez sítě, proto je všechno v jednom souboru:
to, co model zapsal při čtení básně (model/precompute.py).

    uv run python app/build.py
"""
import json
from pathlib import Path

TADY = Path(__file__).resolve().parent
QWEN = TADY.parent / "model" / "qwen.json"

html = (TADY / "template.html").read_text(encoding="utf-8")
# části vícebajtových znaků dekódují na U+FFFD; do JS jde jako escape, aby ho hosting nezahodil
html = html.replace("__QWEN__", QWEN.read_text(encoding="utf-8").replace("�", "\\ufffd"))
(TADY / "index.html").write_text(html, encoding="utf-8")
print("zapsáno app/index.html", (TADY / "index.html").stat().st_size // 1024, "kB")

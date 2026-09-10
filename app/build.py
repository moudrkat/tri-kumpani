"""Slepí appku: app/template.html + model/qwen.json -> app/index.html a docs/index.html.

Appka běží celá v prohlížeči bez sítě, proto je všechno v jednom souboru:
to, co model zapsal při čtení básně (model/precompute.py).

  app/index.html   jen obsah stránky, pro hosting, který si přidá vlastní <head> (claude.ai)
  docs/index.html  celý dokument s UTF-8 a viewportem, pro GitHub Pages a HF Space

    uv run python app/build.py
"""
from pathlib import Path

TADY = Path(__file__).resolve().parent
QWEN = TADY.parent / "model" / "qwen.json"
DOCS = TADY.parent / "docs"

html = (TADY / "template.html").read_text(encoding="utf-8")
# části vícebajtových znaků dekódují na U+FFFD; do JS jde jako escape, aby ho hosting nezahodil
html = html.replace("__QWEN__", QWEN.read_text(encoding="utf-8").replace("�", "\\ufffd"))
(TADY / "index.html").write_text(html, encoding="utf-8")

DOCS.mkdir(exist_ok=True)
(DOCS / ".nojekyll").touch()
(DOCS / "index.html").write_text(
    '<!doctype html>\n<html lang="cs">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Ccircle cx=%2216%22 cy=%2216%22 r=%2212%22 fill=%22%23efe4c6%22/%3E%3C/svg%3E">\n'
    '<style>html,body{margin:0}</style>\n</head>\n<body>\n' + html + '\n</body>\n</html>\n',
    encoding="utf-8")
for f in ("index.html", "docs/index.html"):
    print("zapsáno", f, (TADY.parent / ("app/" + f if f == "index.html" else f)).stat().st_size // 1024, "kB")

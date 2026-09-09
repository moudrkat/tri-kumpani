"""Tisková předloha na záda: první čtyři verše, tři kumpáni, černé pozadí.

    uv sync --extra tisk
    uv run python bunda.py            # zapíše bunda.svg a bunda.png (3200 px na šířku)
"""
from html import escape

from lekce import sloky
from napis import KumpanBPE

VERSE = [v.rstrip(",") for v in sloky("tri_kumpani")[0][:4]]
SIRKA, OKRAJ = 1600, 100          # px, poměr zhruba 40 cm zad
FONT = '"DejaVu Sans Mono", "JetBrains Mono", monospace'


def hex_radky(vers: str, na_radek: int = 24) -> list[str]:
    b = vers.encode("utf-8")
    return [" ".join(f"{x:02x}" for x in b[i:i + na_radek]) for i in range(0, len(b), na_radek)]


def main() -> None:
    bpe = KumpanBPE("\n".join("\n".join(s) for s in sloky("tri_kumpani")), 120)
    y = OKRAJ + 40
    prvky = []
    for vers in VERSE:
        prvky.append(f'<text class="ja" x="{OKRAJ}" y="{y}">{escape(vers)}</text>')
        y += 64
        mesic = "·".join(t.replace(" ", "▁") for t in bpe.tokeny(vers))
        prvky.append(f'<text class="mesic" x="{OKRAJ}" y="{y}">{escape(mesic)}</text>')
        y += 48
        for r in hex_radky(vers):
            prvky.append(f'<text class="stin" x="{OKRAJ}" y="{y}">{r}</text>')
            y += 34
        y += 70
    vyska = y + OKRAJ - 70
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIRKA}" height="{vyska}" viewBox="0 0 {SIRKA} {vyska}">
<style>
  text {{ font-family: {FONT}; white-space: pre; }}
  .ja    {{ font-size: 52px; font-weight: bold; fill: #ffffff; }}
  .mesic {{ font-size: 34px; fill: #d9d9d9; }}
  .stin  {{ font-size: 24px; fill: #6f6f6f; }}
</style>
<rect width="100%" height="100%" fill="#0b0b0b"/>
{chr(10).join(prvky)}
</svg>
"""
    open("bunda.svg", "w", encoding="utf-8").write(svg)
    print("zapsáno bunda.svg")
    try:
        import cairosvg  # uv sync --extra tisk
    except ImportError:
        print("pro PNG: uv sync --extra tisk")
        return
    cairosvg.svg2png(url="bunda.svg", write_to="bunda.png", output_width=3200)
    print("zapsáno bunda.png")


if __name__ == "__main__":
    main()

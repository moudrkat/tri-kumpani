"""Třetí předloha na záda: tokeny velké, čísla drobná pod nimi.

Každé slovo je jeden token slovníku Qwen 2.5, pod ním šedě jeho číslo.
Bez políček, bez barev.

    uv run python bunda_slova.py      # zapíše bunda_slova.svg a bunda_slova.png
"""
from html import escape

from lekce import sloky
from lekce.qwen_tok import decode, encode

VERSE = [v.rstrip(",") for v in sloky("tri_kumpani")[0][:4]]
POZADI, SLOVO, CISLO = "#0b0b0b", "#ffffff", "#6a6762"
SIRKA, OKRAJ = 1800, 80
FONT = '"DejaVu Sans Mono", "JetBrains Mono", monospace'
VEL_SLOVO, VEL_CISLO = 52, 18
SIRKA_ZNAKU = 0.602
MEZERA, VYSKA_RADKU, MEZERA_VERSE = 30, 88, 46


def main() -> None:
    prvky = []
    y = OKRAJ + 50
    for vers in VERSE:
        x = OKRAJ
        for tid in encode(vers):
            slovo = decode([tid]).replace(" ", "▁")
            w = max(len(slovo) * VEL_SLOVO, len(str(tid)) * VEL_CISLO) * SIRKA_ZNAKU
            if x + w > SIRKA - OKRAJ:
                x = OKRAJ
                y += VYSKA_RADKU
            prvky.append(f'<text class="s" x="{x:.0f}" y="{y}">{escape(slovo)}</text>')
            prvky.append(f'<text class="c" x="{x:.0f}" y="{y + 26}">{tid}</text>')
            x += w + MEZERA
        y += VYSKA_RADKU + MEZERA_VERSE
    vyska = y - VYSKA_RADKU - MEZERA_VERSE + 40 + OKRAJ
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIRKA}" height="{vyska}" viewBox="0 0 {SIRKA} {vyska}">
<style>
  text {{ font-family: {FONT}; white-space: pre; }}
  .s {{ font-size: {VEL_SLOVO}px; font-weight: bold; fill: {SLOVO}; }}
  .c {{ font-size: {VEL_CISLO}px; fill: {CISLO}; }}
</style>
<rect width="100%" height="100%" fill="{POZADI}"/>
{chr(10).join(prvky)}
</svg>
"""
    open("bunda_slova.svg", "w", encoding="utf-8").write(svg)
    import cairosvg
    cairosvg.svg2png(url="bunda_slova.svg", write_to="bunda_slova.png", output_width=3200)
    print("zapsáno bunda_slova.svg, bunda_slova.png")


if __name__ == "__main__":
    main()

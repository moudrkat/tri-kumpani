"""Druhá předloha na záda: čísla velká, slova drobná.

Stěna čísel, která je tajně báseň. Každé číslo je token ve slovníku
Qwen 2.5, pod ním šedě to, co v něm je. Bez políček, bez barev.

    uv run python bunda_cisla.py      # zapíše bunda_cisla.svg a bunda_cisla.png
"""
from html import escape

from lekce import sloky
from lekce.qwen_tok import decode, encode
VERSE = [v.rstrip(",") for v in sloky("tri_kumpani")[0][:4]]
POZADI, CISLO, SLOVO = "#0b0b0b", "#ffffff", "#6a6762"
SIRKA, OKRAJ = 1800, 80
FONT = '"DejaVu Sans Mono", "JetBrains Mono", monospace'
VEL_CISLO, VEL_SLOVO = 40, 17
SIRKA_ZNAKU = 0.602
MEZERA, VYSKA_RADKU, MEZERA_VERSE = 28, 80, 50


def main() -> None:
    prvky = []
    y = OKRAJ + 50
    for vers in VERSE:
        x = OKRAJ
        for tid in encode(vers):
            slovo = decode([tid]).replace(" ", "▁")
            w = max(len(str(tid)) * VEL_CISLO, len(slovo) * VEL_SLOVO) * SIRKA_ZNAKU
            if x + w > SIRKA - OKRAJ:
                x = OKRAJ
                y += VYSKA_RADKU
            prvky.append(f'<text class="c" x="{x:.0f}" y="{y}">{tid}</text>')
            prvky.append(f'<text class="s" x="{x:.0f}" y="{y + 26}">{escape(slovo)}</text>')
            x += w + MEZERA
        y += VYSKA_RADKU + MEZERA_VERSE
    vyska = y - VYSKA_RADKU - MEZERA_VERSE + 40 + OKRAJ
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIRKA}" height="{vyska}" viewBox="0 0 {SIRKA} {vyska}">
<style>
  text {{ font-family: {FONT}; white-space: pre; }}
  .c {{ font-size: {VEL_CISLO}px; font-weight: bold; fill: {CISLO}; }}
  .s {{ font-size: {VEL_SLOVO}px; fill: {SLOVO}; }}
</style>
<rect width="100%" height="100%" fill="{POZADI}"/>
{chr(10).join(prvky)}
</svg>
"""
    open("bunda_cisla.svg", "w", encoding="utf-8").write(svg)
    import cairosvg
    cairosvg.svg2png(url="bunda_cisla.svg", write_to="bunda_cisla.png", output_width=3200)
    print("zapsáno bunda_cisla.svg, bunda_cisla.png")


if __name__ == "__main__":
    main()

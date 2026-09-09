"""Tisková předloha na záda: čtyři verše, jednou, ale tak, jak je vidí model.

Každý token ve svém políčku, pod ním jeho číslo ve slovníku. Tokenizer je
skutečný: o200k_base od OpenAI (GPT-4o a novější), 200 019 tokenů. Appka
používá tentýž slovník, takže čísla na bundě jsou ta, která jdou do modelu.

    uv sync --extra tisk
    uv run python bunda.py            # zapíše bunda.svg a bunda.png (3200 px na šířku)
"""
from html import escape

import tiktoken

from lekce import sloky

KODOVANI = "o200k_base"

VERSE = [v.rstrip(",") for v in sloky("tri_kumpani")[0][:4]]
BARVY = ["#2f6f9f", "#b0552f", "#3e8a58", "#7b4f9d"]   # čtyři tlumené, střídají se
POZADI, PISMO, CISLO = "#0b0b0b", "#ffffff", "#e6e6e6"

SIRKA, OKRAJ = 1620, 80
FONT = '"DejaVu Sans Mono", "JetBrains Mono", monospace'
VEL_TOKEN, VEL_CISLO = 40, 18
SIRKA_ZNAKU = 0.602          # poměr šířky znaku k velikosti písma u DejaVu Sans Mono
PAD_X, MEZERA, VYSKA_BOXU, MEZERA_RADKU, MEZERA_VERSE = 12, 8, 92, 14, 56


def sirka_tokenu(t: str) -> float:
    return len(t) * VEL_TOKEN * SIRKA_ZNAKU + 2 * PAD_X


def main() -> None:
    enc = tiktoken.get_encoding(KODOVANI)
    prvky = []
    y = OKRAJ
    for vers in VERSE:
        x = OKRAJ
        barva = 0
        for tid in enc.encode(vers):
            txt = enc.decode([tid]).replace(" ", "▁")
            w = max(sirka_tokenu(txt), len(str(tid)) * VEL_CISLO * SIRKA_ZNAKU + 2 * PAD_X)
            if x + w > SIRKA - OKRAJ:
                x = OKRAJ
                y += VYSKA_BOXU + MEZERA_RADKU
            b = BARVY[barva % len(BARVY)]
            barva += 1
            prvky.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{VYSKA_BOXU}" rx="10" fill="{b}"/>')
            prvky.append(f'<text class="tok" x="{x + w / 2:.0f}" y="{y + 50}">{escape(txt)}</text>')
            prvky.append(f'<text class="id" x="{x + w / 2:.0f}" y="{y + 78}">{tid}</text>')
            x += w + MEZERA
        y += VYSKA_BOXU + MEZERA_VERSE
    vyska = y - MEZERA_VERSE + OKRAJ
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIRKA}" height="{vyska}" viewBox="0 0 {SIRKA} {vyska}">
<style>
  text {{ font-family: {FONT}; text-anchor: middle; white-space: pre; }}
  .tok {{ font-size: {VEL_TOKEN}px; font-weight: bold; fill: {PISMO}; }}
  .id  {{ font-size: {VEL_CISLO}px; fill: {CISLO}; }}
</style>
<rect width="100%" height="100%" fill="{POZADI}"/>
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

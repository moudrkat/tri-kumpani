"""Nápis na bundu: každý verš třikrát pod sebou, pokaždé jiným tokenizerem.

    já      po slovech   Jasmínu▁loubí.▁Sedím▁u▁vína,
    měsíc   BPE          Jas·mín·u ·lou·bí·. ·Se·dím ·u ·ví·na·,
    stín    po bajtech   4a 61 73 6d c3 ad 6e 75 20 ...

Tři kumpáni: básník, který mluví slovy; měsíc, který si kusy skládá sám;
a stín, který je jen otisk bajtů.

Spuštění:
    uv run python napis.py                 # vypíše na terminál
    uv run python napis.py --svg napis.svg # šablona na tisk / nažehlovačku
    uv run python napis.py --sloka 1       # jen jednu sloku (od 1)
"""
import argparse
import re
from collections import Counter
from html import escape

from lekce import sloky
from lekce.l03_bpe import sluc, spocitej_pary

# Předsekání jako v GPT-2: slovo, interpunkce, nebo mezera přilepená k dalšímu slovu.
PREDSEKANI = re.compile(r" ?\w+| ?[^\w\s]+|\s+")


class KumpanBPE:
    """BPE nad znaky (ne bajty), aby žádný token nebyl půlka písmene.

    Spojuje jen uvnitř předsekaných kusů, takže se nikdy nesrostou dvě slova.
    """

    def __init__(self, text: str, spojeni: int) -> None:
        self.znaky = sorted(set(text))
        self.idx = {z: i for i, z in enumerate(self.znaky)}
        self.slovnik: dict[int, str] = dict(enumerate(self.znaky))
        self.pravidla: dict[tuple[int, int], int] = {}
        kusy = [self._ids(k) for k in PREDSEKANI.findall(text)]
        for novy in range(len(self.znaky), len(self.znaky) + spojeni):
            pary: Counter = Counter()
            for k in kusy:
                pary.update(spocitej_pary(k))
            if not pary:
                break
            par, pocet = pary.most_common(1)[0]
            if pocet < 2:
                break
            kusy = [sluc(k, par, novy) for k in kusy]
            self.pravidla[par] = novy
            self.slovnik[novy] = self.slovnik[par[0]] + self.slovnik[par[1]]

    def _ids(self, kus: str) -> list[int]:
        return [self.idx[z] for z in kus]

    def tokeny(self, text: str) -> list[str]:
        out = []
        for kus in PREDSEKANI.findall(text):
            ids = self._ids(kus)
            while len(ids) > 1:
                pary = spocitej_pary(ids)
                par = min(pary, key=lambda p: self.pravidla.get(p, float("inf")))
                if par not in self.pravidla:
                    break
                ids = sluc(ids, par, self.pravidla[par])
            out.extend(self.slovnik[i] for i in ids)
        return out


def ja(vers: str) -> str:
    return vers.replace(" ", "▁")


def mesic(vers: str, bpe: KumpanBPE) -> str:
    return "·".join(t.replace(" ", "▁") for t in bpe.tokeny(vers))


def stin(vers: str) -> str:
    return " ".join(f"{b:02x}" for b in vers.encode("utf-8"))


def trojice(vers: str, bpe: KumpanBPE) -> list[str]:
    return [ja(vers), mesic(vers, bpe), stin(vers)]


def napis(basen: list[list[str]], spojeni: int = 120) -> list[list[list[str]]]:
    bpe = KumpanBPE("\n".join("\n".join(s) for s in basen), spojeni)
    return [[trojice(v, bpe) for v in sloka] for sloka in basen]


def do_textu(vysledek: list[list[list[str]]]) -> str:
    radky = []
    for sloka in vysledek:
        for trojka in sloka:
            radky.extend(trojka)
            radky.append("")
        radky.append("")
    return "\n".join(radky).rstrip() + "\n"


def do_svg(vysledek: list[list[list[str]]], sirka: int = 900) -> str:
    vyska_radku, mezera_vers, mezera_sloka = 22, 12, 30
    styly = ["ja", "mesic", "stin"]
    y = 40
    prvky = []
    for sloka in vysledek:
        for trojka in sloka:
            for styl, radek in zip(styly, trojka):
                prvky.append(f'<text class="{styl}" x="30" y="{y}">{escape(radek)}</text>')
                y += vyska_radku
            y += mezera_vers
        y += mezera_sloka
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{sirka}" height="{y}" viewBox="0 0 {sirka} {y}">
<style>
  text {{ font-family: "DejaVu Sans Mono", monospace; font-size: 16px; fill: #111; white-space: pre; }}
  .ja {{ font-weight: bold; }}
  .mesic {{ fill: #444; }}
  .stin {{ fill: #888; font-size: 13px; }}
</style>
<rect width="100%" height="100%" fill="white"/>
{chr(10).join(prvky)}
</svg>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--basen", default="tri_kumpani")
    ap.add_argument("--sloka", type=int, help="jen tahle sloka, od 1")
    ap.add_argument("--spojeni", type=int, default=120, help="kolik BPE pravidel se naučit")
    ap.add_argument("--svg", help="kam zapsat SVG")
    a = ap.parse_args()
    basen = sloky(a.basen)
    vysledek = napis(basen, a.spojeni)
    if a.sloka:
        vysledek = [vysledek[a.sloka - 1]]
    if a.svg:
        with open(a.svg, "w", encoding="utf-8") as f:
            f.write(do_svg(vysledek))
        print(f"zapsáno {a.svg}")
    else:
        print(do_textu(vysledek), end="")


if __name__ == "__main__":
    main()

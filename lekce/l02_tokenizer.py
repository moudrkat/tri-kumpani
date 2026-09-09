"""Lekce 2: tokenizer je jen rozhodnutí, co je jeden kus.

Tři nejjednodušší volby a co dělají s tou samou básní:
  - po bajtech:  slovník má 256 položek, čínský znak je 3 tokeny
  - po znacích:  slovník je tak velký, kolik různých znaků potkáš
  - po slovech:  pro čínštinu bez mezer nemá smysl, pro překlad ano

Tokenizer se skládá ze dvou půlek: `encode` (text -> čísla) a `decode`
(čísla -> text). Slovník je jen tabulka mezi nimi.

Spuštění: uv run python -m lekce.l02_tokenizer
"""
import re

from lekce import nacti


class Tokenizer:
    def __init__(self, kusy: list[str]) -> None:
        self.slovnik = {k: i for i, k in enumerate(dict.fromkeys(kusy))}
        self.zpet = {i: k for k, i in self.slovnik.items()}

    def rozsekej(self, text: str) -> list[str]:
        raise NotImplementedError

    def encode(self, text: str) -> list[int]:
        return [self.slovnik[k] for k in self.rozsekej(text)]

    def decode(self, ids: list[int]) -> str:
        return "".join(self.zpet[i] for i in ids)


class PoZnacich(Tokenizer):
    def __init__(self, text: str) -> None:
        super().__init__(list(text))

    def rozsekej(self, text: str) -> list[str]:
        return list(text)


class PoBajtech(Tokenizer):
    def __init__(self) -> None:
        self.slovnik = {i: i for i in range(256)}
        self.zpet = self.slovnik

    def encode(self, text: str) -> list[int]:
        return list(text.encode("utf-8"))

    def decode(self, ids: list[int]) -> str:
        return bytes(ids).decode("utf-8", errors="replace")


class PoSlovech(Tokenizer):
    def __init__(self, text: str) -> None:
        super().__init__(self.rozsekej(text))

    def rozsekej(self, text: str) -> list[str]:
        # slovo, nebo bílé místo (mezery i konce řádků) jako vlastní kus
        return re.findall(r"\S+|\s+", text)


def main() -> None:
    text = nacti()
    for jmeno, tok in [("bajty", PoBajtech()), ("znaky", PoZnacich(text))]:
        ids = tok.encode(text)
        print(f"{jmeno:6} slovník {len(tok.slovnik):3}  tokenů {len(ids):3}  "
              f"kulaté: {tok.decode(ids) == text}")
        print("       ", ids[:12], "...")
    cz = "Před postelí svit měsíce,\nsnad jinovatka na zemi."
    tok = PoSlovech(cz)
    ids = tok.encode(cz)
    print(f"slova  slovník {len(tok.slovnik):3}  tokenů {len(ids):3}  "
          f"kulaté: {tok.decode(ids) == cz}")
    print("       ", tok.rozsekej(cz))
    print()
    print("Všimni si: 'měsíce,' a 'měsíc' by byla dvě různá slova.")
    print("Přesně to řeší lekce 3: kusy, které si tokenizer vyrobí sám z dat.")


if __name__ == "__main__":
    main()

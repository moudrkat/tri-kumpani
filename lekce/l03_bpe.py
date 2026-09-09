"""Lekce 3: Byte Pair Encoding. Slovník, který si text vyrobí sám.

Začni s 256 bajty. Opakuj: najdi nejčastější sousední dvojici, nahraď ji
novým tokenem, zapiš si to jako pravidlo. Skonči, až máš tolik tokenů,
kolik chceš. Encode pak aplikuje pravidla ve stejném pořadí, decode
je jen zpětné rozbalení na bajty.

Tohle je přesně to, co dělá GPT-2/tiktoken (byte-level BPE), jen tam je
před tím ještě regex, který text předseká na slova, aby se nesrůstalo
přes mezery.

Na básni o 60 bajtech se to dá sledovat pravidlo po pravidlu: první
spojení jsou bajty jednoho znaku (e5 a4 ...), pak celé znaky a nakonec
明月 jako jeden token, protože se opakuje.

Spuštění: uv run python -m lekce.l03_bpe
"""
from collections import Counter

from lekce import nacti

Par = tuple[int, int]


def spocitej_pary(ids: list[int]) -> Counter[Par]:
    return Counter(zip(ids, ids[1:]))


def sluc(ids: list[int], par: Par, novy: int) -> list[int]:
    out: list[int] = []
    i = 0
    while i < len(ids):
        if i + 1 < len(ids) and (ids[i], ids[i + 1]) == par:
            out.append(novy)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


class BPE:
    def __init__(self) -> None:
        self.pravidla: dict[Par, int] = {}
        self.slovnik: dict[int, bytes] = {i: bytes([i]) for i in range(256)}

    def nauc(self, text: str, velikost: int, ukazuj: bool = False) -> None:
        ids = list(text.encode("utf-8"))
        for novy in range(256, velikost):
            pary = spocitej_pary(ids)
            if not pary:
                break
            par, pocet = pary.most_common(1)[0]
            if pocet < 2:
                break
            ids = sluc(ids, par, novy)
            self.pravidla[par] = novy
            self.slovnik[novy] = self.slovnik[par[0]] + self.slovnik[par[1]]
            if ukazuj:
                kus = self.slovnik[novy].decode("utf-8", errors="replace")
                print(f"  {novy}: {par} x{pocet} -> {self.slovnik[novy].hex()}  {kus!r}")

    def encode(self, text: str) -> list[int]:
        ids = list(text.encode("utf-8"))
        while len(ids) > 1:
            pary = spocitej_pary(ids)
            par = min(pary, key=lambda p: self.pravidla.get(p, float("inf")))
            if par not in self.pravidla:
                break
            ids = sluc(ids, par, self.pravidla[par])
        return ids

    def decode(self, ids: list[int]) -> str:
        return b"".join(self.slovnik[i] for i in ids).decode("utf-8", errors="replace")


def main() -> None:
    text = nacti()
    bpe = BPE()
    print("učím se pravidla:")
    bpe.nauc(text, 256 + 40, ukazuj=True)
    ids = bpe.encode(text)
    print()
    print(f"bajtů {len(text.encode())}, tokenů po BPE {len(ids)}, kulaté: {bpe.decode(ids) == text}")
    print("tokeny:", [bpe.slovnik[i].decode("utf-8", errors="replace") for i in ids])
    print("  (� je token, který je jen část bajtů jednoho znaku: znak se v básni")
    print("   vyskytl jednou, takže se jeho bajty neměly proč spojit)")
    print()
    print("Zkus: nauč BPE na delším čínském textu (basne/*.txt) a podívej se,")
    print("jestli 明月 pořád vyjde jako jeden token, nebo se rozpadne.")


if __name__ == "__main__":
    main()

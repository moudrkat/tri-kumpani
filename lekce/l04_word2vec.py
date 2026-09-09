"""Lekce 4: word2vec. Číslo pro token, které něco znamená.

Tokenizer dá každému kusu textu pořadové číslo, ale 明 = 3 a 月 = 4
neříká nic o tom, že spolu souvisí. Word2vec (skip-gram) se učí pro každý
token vektor tak, aby z vektoru šlo uhodnout, co stojí kolem něj.
Tokeny, které se vyskytují v podobném okolí, skončí blízko sebe.

Tady je skip-gram s negativním vzorkováním v čistém numpy, na tokenech
po znacích. Dvacet znaků je málo na cokoli chytrého, ale dost na to,
aby šlo vidět, že 明 a 月 se k sobě přitáhnou, protože se vyskytují
vedle sebe dvakrát. Pro opravdový výsledek přidej do basne/ víc básní.

Spuštění: uv run python -m lekce.l04_word2vec
"""
import numpy as np

from lekce import nacti


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


class SkipGram:
    def __init__(self, tokeny: list[str], dim: int = 8, seed: int = 0) -> None:
        self.slovnik = list(dict.fromkeys(tokeny))
        self.idx = {t: i for i, t in enumerate(self.slovnik)}
        rng = np.random.default_rng(seed)
        n = len(self.slovnik)
        self.W_in = rng.normal(0, 0.1, (n, dim))   # vektor slova jako středu
        self.W_out = rng.normal(0, 0.1, (n, dim))  # vektor slova jako souseda
        self.rng = rng

    def pary(self, tokeny: list[str], okno: int) -> list[tuple[int, int]]:
        ids = [self.idx[t] for t in tokeny]
        out = []
        for i, stred in enumerate(ids):
            for j in range(max(0, i - okno), min(len(ids), i + okno + 1)):
                if j != i:
                    out.append((stred, ids[j]))
        return out

    def krok(self, stred: int, soused: int, negativ: int, lr: float) -> float:
        v = self.W_in[stred]
        ztrata = 0.0
        grad_v = np.zeros_like(v)
        for cil, label in [(soused, 1.0), *[(n, 0.0) for n in [negativ]]]:
            u = self.W_out[cil]
            p = sigmoid(v @ u)
            g = p - label
            ztrata -= np.log(p if label else 1 - p)
            grad_v += g * u
            self.W_out[cil] -= lr * g * v
        self.W_in[stred] -= lr * grad_v
        return ztrata

    def trenuj(self, tokeny: list[str], okno: int = 2, epochy: int = 300, lr: float = 0.05) -> None:
        pary = self.pary(tokeny, okno)
        n = len(self.slovnik)
        for e in range(epochy):
            self.rng.shuffle(pary)
            ztrata = 0.0
            for stred, soused in pary:
                negativ = int(self.rng.integers(n))
                ztrata += self.krok(stred, soused, negativ, lr)
            if e % 100 == 0 or e == epochy - 1:
                print(f"  epocha {e:4}  ztráta {ztrata / len(pary):.3f}")

    def vektor(self, token: str) -> np.ndarray:
        v = self.W_in[self.idx[token]]
        return v / np.linalg.norm(v)

    def nejblizsi(self, token: str, k: int = 3) -> list[tuple[str, float]]:
        v = self.vektor(token)
        vsechny = self.W_in / np.linalg.norm(self.W_in, axis=1, keepdims=True)
        skore = vsechny @ v
        poradi = np.argsort(-skore)
        return [(self.slovnik[i], float(skore[i])) for i in poradi if self.slovnik[i] != token][:k]


def main() -> None:
    tokeny = [z for z in nacti() if z != "\n"]
    model = SkipGram(tokeny, dim=8)
    print("trénuju skip-gram na", len(model.slovnik), "znacích:")
    model.trenuj(tokeny)
    print()
    for z in "明月头思":
        print(f"{z} ~", "  ".join(f"{t} {s:.2f}" for t, s in model.nejblizsi(z)))
    print()
    print("Uložím vektory do vektory.npy, ať se dají kreslit (PCA na 2D).")
    np.save("vektory.npy", model.W_in)


if __name__ == "__main__":
    main()

# li-po-jacket

Na zádech bundy bude Li Po, **Tři kumpáni** v Mathesiově přebásnění.
Každý verš třikrát pod sebou, pokaždé jiným tokenizerem, protože kumpáni
jsou tři:

```text
já      Jasmínu▁loubí.▁Sedím▁u▁vína,                   po slovech
měsíc   Jas·mín·u·▁lou·bí·.·▁Se·dím·▁u·▁ví·na·,        BPE, kusy naučené z básně
stín    4a 61 73 6d c3 ad 6e 75 20 6c 6f 75 62 c3 ad   bajty UTF-8
```

Po cestě se naučím, co je pod textem: bajty, tokenizery, BPE a word2vec.

## Spuštění

```bash
uv sync --extra dev
uv run python napis.py                  # celý nápis na terminál
uv run python napis.py --sloka 1        # jen první sloka
uv run python napis.py --verse 1-4      # nápis končí „se mi uklání“
uv run python bunda.py                  # tisková předloha bunda.svg + bunda.png
uv run pytest
```

## Lekce

Každá je jeden skript, pustí se `uv run python -m lekce.l0X_...` a vypíše,
co se v něm děje. Čtou se v tomhle pořadí:

1. `lekce/l01_bajty.py`: znak, kódový bod, bajt. Proč má 月 tři bajty a jak
   UTF-8 pozná začátek znaku.
2. `lekce/l02_tokenizer.py`: tokenizer je jen rozhodnutí, co je jeden kus.
   Po bajtech, po znacích, po slovech, a co to dělá s velikostí slovníku.
3. `lekce/l03_bpe.py`: Byte Pair Encoding od nuly. Slovník, který si text
   vyrobí sám; sledovatelné pravidlo po pravidlu na dvaceti znacích.
4. `lekce/l04_word2vec.py`: skip-gram v čistém numpy. Číslo pro token, které
   něco znamená; 明 a 月 se k sobě přitáhnou.

`napis.py` používá totéž BPE jako lekce 3, jen nad znaky místo bajtů a
s předsekáním na slova jako GPT-2, aby žádný token nebyl půlka písmene
a nesrostla dvě slova.

## Úkoly na později

- Srovnat vlastní BPE s `tiktoken` a HF `tokenizers` (`uv sync --extra srovnani`):
  kolik tokenů dá GPT-2 tokenizer na Tři kumpány a kde seká jinak.
- Nakreslit vektory z lekce 4 (PCA do 2D) a přidat víc básní, ať je na čem
  trénovat.
- Appka k bundě: naskenovat QR na rukávu a vidět, jak se verš rozpadá na
  tokeny živě. Až bude foto bundy.

## Básně

Viz [`basne/README.md`](basne/README.md): odkud je text, kde se opisy liší,
a originál 月下独酌 pro srovnání.

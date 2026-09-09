# li-po-jacket

Na zádech bundy jsou první čtyři verše Li Po, **Tři kumpáni** v Mathesiově
přebásnění, končí „se mi uklání". Jednou, ale tak, jak je vidí jazykový model:
každý token ve svém políčku a pod ním jeho číslo ve slovníku o200k_base
(tokenizer GPT-4o a novějších). Na rukávu je QR na appku, kde tentýž
tokenizer rozseká cokoli a řekne, kolik z toho už Li Po řekl.

- `bunda.py` → `bunda.png` / `bunda.svg`: tisková předloha na záda
- `rukav_qr.png` / `.svg`: QR na rukáv, vede na appku
- `app/index.html`: appka, běží celá v prohlížeči (tokenizer z CDN, 2 MB)
- `napis.py`: první verze, každý verš třikrát (slova, vlastní BPE, bajty)

Po cestě se učím, co je pod textem: bajty, tokenizery, BPE a word2vec.

## Spuštění

```bash
uv sync --extra dev
uv run python napis.py                  # celý nápis na terminál
uv run python napis.py --sloka 1        # jen první sloka
uv run python napis.py --verse 1-4      # nápis končí „se mi uklání“
uv sync --extra tisk
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
- Appka: word2vec sousedi tokenu, natrénované na celých Zpěvech staré Číny.
- Až bude foto bundy: přeměřit šířku zad proti `bunda.py`.

## Básně

Viz [`basne/README.md`](basne/README.md): odkud je text, kde se opisy liší,
a originál 月下独酌 pro srovnání.

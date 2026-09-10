# Tři kumpáni

Li Po's *Drinking Alone under the Moon* (月下独酌), in Bohumil Mathesius's Czech
rendering, read by a small language model. Four verses go on the back of a
jacket as tokens; the app on the sleeve shows where the model looked while
reading them, head by head, and what it would write next.

```
Jasmínu loubí. Sedím u vína,
zve dobré druhy dobrá hodina –
a já jsem sám. Vtom náhle nad strání
kulatý měsíc se mi uklání
```

App: https://huggingface.co/spaces/Unt1l1f1nd/tri-kumpani (the sleeve QR points to https://unt1l1f1nd-tri-kumpani.static.hf.space/)

## Run

```bash
uv sync --extra model --extra tisk
uv run python model/precompute.py   # Qwen 2.5 0.5B reads the poem: attention, logit lens, next verse
uv run python app/build.py          # -> app/index.html, self-contained
uv run python bunda_cisla.py        # print template for the jacket (numbers large, words small)
uv run python bunda.py              # alternative: colored token boxes
uv run pytest
```

## Layout

- `app/` static app, one file, no network
- `model/precompute.py` what the model wrote down while reading
- `bunda*.py`, `rukav_qr.*` print templates for back and sleeve
- `space/README.md` front matter for the Hugging Face Space; upload it with `app/index.html`
- `lekce/` byte encoding, tokenizers, BPE from scratch, word2vec in numpy
- `basne/` the poem, Czech and original

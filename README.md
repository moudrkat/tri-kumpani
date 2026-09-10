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

Mathesius worked from German and French versions, so the jasmine, the bower
and the bow are his. Li Po's opening couplets, and what they say:

```
花间一壶酒    Among the flowers, a jug of wine.
独酌无相亲    I drink alone, no one close.
举杯邀明月    I raise my cup and invite the bright moon;
对影成三人    with my shadow, that makes three.
```

The Czech, word for word: *A jasmine bower. I sit with wine; the good hour calls
for good company, and I am alone. Then suddenly, over the hillside, the round
moon bows to me.*

App: https://moudrkat.github.io/tri-kumpani/ (also on
[Hugging Face](https://huggingface.co/spaces/Unt1l1f1nd/tri-kumpani)).
The sleeve carries the address in plain text.

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
- `bunda*.py`, `rukav.py` print templates for back (numbers large, words large, or colored boxes) and sleeve
- `docs/` the built app, served by GitHub Pages
- `space/README.md` front matter for the Hugging Face Space; upload it with `docs/index.html`
- `lekce/` byte encoding, tokenizers, BPE from scratch, word2vec in numpy
- `basne/` the poem: Czech, and the original with a plain English rendering

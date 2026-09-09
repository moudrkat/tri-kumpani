from lekce import nacti, sloky, verse
from lekce.l02_tokenizer import PoBajtech, PoSlovech, PoZnacich
from lekce.l03_bpe import BPE
from napis import KumpanBPE, napis, stin


def test_ticha_noc_ma_dvacet_znaku():
    assert sum(len(v) for v in verse("ticha_noc")) == 20


def test_tri_kumpani_ma_pet_slok():
    assert [len(s) for s in sloky("tri_kumpani")] == [8, 4, 6, 4, 2]


def test_tokenizery_jsou_kulate():
    text = nacti("tri_kumpani")
    for tok in (PoBajtech(), PoZnacich(text), PoSlovech(text)):
        assert tok.decode(tok.encode(text)) == text


def test_bpe_je_kulate_a_kratsi():
    text = nacti("ticha_noc")
    bpe = BPE()
    bpe.nauc(text, 256 + 40)
    ids = bpe.encode(text)
    assert bpe.decode(ids) == text
    assert len(ids) < len(text.encode())
    assert "明月".encode() in bpe.slovnik.values()


def test_kumpan_bpe_nesrusti_slova():
    text = nacti("tri_kumpani")
    bpe = KumpanBPE(text, 120)
    for vers in verse("tri_kumpani"):
        tokeny = bpe.tokeny(vers)
        assert "".join(tokeny) == vers
        assert all(" " not in t.strip() for t in tokeny)


def test_napis_ma_tri_radky_na_vers():
    vysledek = napis(sloky("tri_kumpani"))
    for sloka in vysledek:
        for trojka in sloka:
            assert len(trojka) == 3


def test_stin_je_hex():
    assert stin("já") == "6a c3 a1"

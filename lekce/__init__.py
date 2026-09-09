from pathlib import Path

BASNE = Path(__file__).resolve().parent.parent / "basne"


def nacti(jmeno: str = "ticha_noc") -> str:
    return (BASNE / f"{jmeno}.txt").read_text(encoding="utf-8").strip()


def verse(jmeno: str = "ticha_noc") -> list[str]:
    """Verše bez prázdných řádků mezi slokami."""
    return [r for r in nacti(jmeno).splitlines() if r.strip()]


def sloky(jmeno: str = "tri_kumpani") -> list[list[str]]:
    return [s.splitlines() for s in nacti(jmeno).split("\n\n")]

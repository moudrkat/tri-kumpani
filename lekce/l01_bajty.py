"""Lekce 1: co je pod textem. Znak, kódový bod, bajt.

Python `str` je posloupnost kódových bodů Unicode (čísel). Na disk, po drátu
a do modelu jdou bajty, a UTF-8 je předpis, jak číslo rozsekat do 1 až 4 bajtů.
Čínský znak potřebuje 3 bajty, "a" jeden, "ě" dva.

Spuštění: uv run python -m lekce.l01_bajty
"""
from lekce import nacti


def rozbor(znak: str) -> str:
    bod = ord(znak)
    bajty = znak.encode("utf-8")
    hexa = " ".join(f"{b:02x}" for b in bajty)
    bity = " ".join(f"{b:08b}" for b in bajty)
    return f"{znak}  U+{bod:04X}  {len(bajty)} B  [{hexa}]  {bity}"


def main() -> None:
    text = nacti()
    znaky = [z for z in text if z != "\n"]
    print(f"znaků: {len(znaky)}, bajtů: {len(text.replace(chr(10), '').encode())}")
    print()
    for z in znaky:
        print(rozbor(z))
    print()
    print("pro srovnání:")
    for z in "aě€😀":
        print(rozbor(z))
    print()
    print("UTF-8 první bajt říká, kolik bajtů následuje:")
    print("  0xxxxxxx = 1 bajt (ASCII), 110xxxxx = 2, 1110xxxx = 3, 11110xxx = 4")
    print("  pokračovací bajty začínají 10xxxxxx, proto jde v proudu bajtů")
    print("  vždycky najít začátek znaku, i když začneš číst uprostřed.")


if __name__ == "__main__":
    main()

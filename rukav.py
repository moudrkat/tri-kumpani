"""Rukáv: adresa appky jako text, ve stejném písmu jako záda. Plus QR pro jistotu.

    uv run --with qrcode --with pillow python rukav.py
"""
URL = "moudrkat.github.io/tri-kumpani"
POZADI, PISMO = "#0b0b0b", "#ffffff"
FONT = '"DejaVu Sans Mono", "JetBrains Mono", monospace'


def main() -> None:
    vel, okraj = 40, 40
    w = int(len(URL) * vel * 0.602 + 2 * okraj)
    h = vel + 2 * okraj
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="100%" height="100%" fill="{POZADI}"/>
<text x="{okraj}" y="{okraj + vel * 0.78:.0f}" font-family='{FONT}' font-size="{vel}" font-weight="bold" fill="{PISMO}">{URL}</text>
</svg>
"""
    open("rukav.svg", "w", encoding="utf-8").write(svg)
    import cairosvg
    cairosvg.svg2png(url="rukav.svg", write_to="rukav.png", output_width=2400)
    print("zapsáno rukav.svg, rukav.png")
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=2)
    q.add_data("https://" + URL + "/"); q.make()
    q.make_image(fill_color="white", back_color=POZADI).resize((1200, 1200), 0).save("rukav_qr.png")
    print("zapsáno rukav_qr.png")


if __name__ == "__main__":
    main()

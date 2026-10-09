"""Anúncio feed 4:5 (1080x1350) - Rouanet Urgente. Uso: python3 gerar_anuncio.py [logo_zion.png]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
M = 86                         # margem lateral (8%)
TOP_SAFE = 135                 # 10% superior sem texto
BOTTOM = 1080                  # 80%: abaixo disso, sem texto
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
NAVY, GOLD, WHITE = (13, 27, 62), (255, 196, 0), (255, 255, 255)
f = lambda s: ImageFont.truetype(B, s)

# fundo: degradê azul-escuro + círculos suaves (só continuação visual)
im = Image.new("RGB", (W, H), NAVY)
px = ImageDraw.Draw(im)
for y in range(H):
    t = y / H
    px.line([(0, y), (W, y)], fill=(int(13 + 12 * t), int(27 + 20 * t), int(62 + 40 * t)))
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.ellipse((-260, 1150, 380, 1790), fill=(255, 196, 0, 28))
od.ellipse((760, 1000, 1400, 1640), fill=(255, 255, 255, 18))
od.ellipse((820, 300, 1200, 680), fill=(255, 196, 0, 20))
im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
d = ImageDraw.Draw(im)

def wrap(text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def lh(size): return int(size * 1.12)
maxw = W - 2 * M

# ---- faixa do produto (ancorada em 80% = 1080) ----
L1 = ["Rouanet Urgente -", "Desafio de 3 Dias"]
L2 = wrap("Da ideia ao projeto enviado", f(61), maxw)
L3 = wrap("A última data pra enviar projetos ao MinC é 31/10/2026", f(61), maxw)
PAD = 26
h_main = PAD + len(L1) * lh(70) + 8 + len(L2) * lh(61) + PAD
h_tarja = 20 + len(L3) * lh(61) + 20
band_top = BOTTOM - h_main - h_tarja
d.rectangle((0, band_top, W, BOTTOM), fill=WHITE)
y = band_top + PAD
for l in L1:
    d.text((W / 2, y), l, font=f(70), fill=NAVY, anchor="ma"); y += lh(70)
y += 8
for l in L2:
    d.text((W / 2, y), l, font=f(61), fill=NAVY, anchor="ma"); y += lh(61)
tarja_top = BOTTOM - h_tarja
d.rectangle((0, tarja_top, W, BOTTOM), fill=GOLD)
y = tarja_top + 20
for l in L3:
    d.text((W / 2, y), l, font=f(61), fill=NAVY, anchor="ma"); y += lh(61)

# ---- CTA em texto, sem botão ----
cta_h = 81
cta_top = band_top - cta_h
cta = "Clique aqui para saber mais!"
cf = f(59)
aw = 50                       # seta desenhada (negrito) apontando p/ baixo
tw = d.textlength(cta, font=cf) + 24 + aw
x0 = (W - tw) / 2; cy = cta_top + cta_h / 2
d.text((x0, cy), cta, font=cf, fill=GOLD, anchor="lm")
ax = x0 + tw - aw / 2
d.rectangle((ax - 7, cy - 26, ax + 7, cy + 4), fill=GOLD)
d.polygon([(ax - 25, cy), (ax + 25, cy), (ax, cy + 28)], fill=GOLD)

# ---- parte de cima (criativo): 135 -> cta_top ----
creative_top, creative_bottom = TOP_SAFE, cta_top - 10
logo_h = 80
logo_y = TOP_SAFE + 10
logo_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_zion_branca.png")
if logo_path and os.path.exists(logo_path):
    lg = Image.open(logo_path).convert("RGBA")
    lw = round(lg.width * logo_h / lg.height)
    lg = lg.resize((lw, logo_h), Image.LANCZOS)
    im.paste(lg, (W - M - lw, logo_y), lg)

blocks = [("3 DIAS", 130, GOLD), ("pra tirar seu projeto", 64, WHITE), ("do papel", 64, WHITE)]
total = sum(lh(s) for _, s, _ in blocks)
area_top = logo_y + logo_h + 10
y = area_top + (creative_bottom - area_top - total) / 2
for t, s, c in blocks:
    d.text((M, y), t, font=f(s), fill=c); y += lh(s)

im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "anuncio_rouanet_1080x1350.png"))
print("faixa", band_top, "CTA", cta_top, "criativo", creative_top, "-", creative_bottom, "texto", round(area_top + (creative_bottom - area_top - total) / 2), "tw", tw)

from PIL import Image, ImageDraw, ImageFont

S = 3  # supersampling: mesma proporção, maior resolução
R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
GREEN = (30, 120, 50)
INK = (25, 40, 30)

im = Image.open("modelo_banner.jpg").convert("RGB")
im = im.resize((im.width * S, im.height * S), Image.LANCZOS)
d = ImageDraw.Draw(im)

def font(p, s): return ImageFont.truetype(p, int(s))

def wrap(par, f, w):
    words, lines, cur = par.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= w: cur = t
        else: lines.append(cur); cur = wd
    lines.append(cur)
    return lines

def layout(paras, box, path, size, lh, pad):
    x0, y0, x1, y1 = [v * S for v in box]
    w = x1 - x0 - 2 * pad * S
    f = font(path, size * S)
    out = []
    for p in paras:
        if p == "": out.append(("", 0.5)); continue
        for l in wrap(p, f, w): out.append((l, 1))
    h = sum(k for _, k in out) * size * S * lh
    return f, out, h, (x0, y0, x1, y1)

def fill(paras, box, path=R, center=False, pad=10, lh=1.18, maxsize=30, bold_first=False, minsize=6):
    x0, y0, x1, y1 = [v * S for v in box]
    avail = y1 - y0 - 2 * 8 * S
    size = maxsize
    while size > minsize:
        f, out, h, _ = layout(paras, box, path, size, lh, pad)
        if h <= avail: break
        size -= 0.25
    f, out, h, _ = layout(paras, box, path, size, lh, pad)
    y = y0 + ((y1 - y0) - h) / 2 if center else y0 + 8 * S
    for l, k in out:
        if l:
            tx = x0 + pad * S
            if center: tx = (x0 + x1) / 2 - d.textlength(l, font=f) / 2
            d.text((tx, y), l, font=f, fill=INK)
        y += k * size * S * lh
    return size

def fill_lines(lines, box):
    """lines: list of (text, fontpath, size)"""
    x0, y0, x1, y1 = [v * S for v in box]
    h = sum(s * S * 1.25 for _, _, s in lines)
    y = y0 + ((y1 - y0) - h) / 2
    for t, p, s in lines:
        f = font(p, s * S)
        d.text(((x0 + x1) / 2 - d.textlength(t, font=f) / 2, y), t, font=f, fill=INK)
        y += s * S * 1.25

# TÍTULO
titulo = "ÁGUAS DE RESISTÊNCIA: ANÁLISE DO RACISMO AMBIENTAL ATRAVÉS DO PH DA ÁGUA E DA QUÍMICA ANCESTRAL NEGRA NOS 55 ANOS DO 20 DE NOVEMBRO (1971–2026)"
def title():
    box = (68, 372, 1130, 466)
    for sz in range(40, 10, -1):
        f = font(B, sz * S)
        ls = wrap(titulo, f, (1130 - 68 - 40) * S)
        h = len(ls) * sz * S * 1.15
        if h <= (466 - 372 - 10) * S: break
    y = (372 + 466) / 2 * S - h / 2 + 2 * S
    for l in ls:
        d.text(((68 + 1130) / 2 * S - d.textlength(l, font=f) / 2, y), l, font=f, fill=GREEN)
        y += sz * S * 1.15
title()

# AUTORES
fill_lines([
    ("Raíssa Victória de Mattos e Otávio de Souza", B, 20),
    ("I.E. Dom Diogo de Souza – DDS 1930 – Porto Alegre – RS", R, 15),
    ("Mostra Científica 2026", R, 15),
    ("Orientação: Biologia e Química", R, 15),
], (70, 535, 1132, 627))

intro = ["O dia 20 de Novembro, instituído em 1971 pelo Grupo Palmares, representa um marco de resistência e valorização da história e da cultura negra. O racismo ambiental está relacionado à exposição desigual de comunidades negras e periféricas a problemas ambientais e à falta de infraestrutura adequada.",
"Em Porto Alegre, bairros periféricos apresentam desigualdades no acesso ao saneamento básico. Este projeto relaciona conhecimentos de Química e Biologia para discutir a qualidade da água, utilizando o pH como indicador químico, além de valorizar conhecimentos ancestrais relacionados ao uso de plantas medicinais."]
obj = ["Analisar o pH da água por meio de um indicador natural e relacioná-lo à importância da qualidade da água e do saneamento, discutindo também as desigualdades ambientais e valorizando conhecimentos ancestrais sobre plantas medicinais como formas de cuidado, conhecimento e resistência."]
met = ["Foi realizado um experimento utilizando repolho roxo como indicador natural de pH, além de água, vinagre e detergente.",
"1. O extrato de repolho roxo foi obtido por meio de fervura.",
"2. Em seguida, foram adicionados 10 mL do indicador às diferentes amostras.",
"3. As mudanças de coloração foram observadas e relacionadas aos diferentes níveis de pH.",
"Também foi realizada pesquisa bibliográfica sobre racismo ambiental, saneamento, 20 de Novembro e conhecimentos ancestrais relacionados às plantas medicinais."]
res = ["O experimento apresentou mudanças de coloração do indicador de repolho roxo conforme as características das amostras:",
"• Água limpa: coloração roxa (pH ≈ 7) – neutro;",
"• Vinagre: coloração rosada (pH ≈ 4) – ácido;",
"• Detergente: coloração esverdeada (pH ≈ 10) – básico.",
"Os resultados demonstraram que o indicador natural de repolho roxo permite visualizar diferenças de pH de maneira simples e acessível. A pesquisa também evidenciou a importância de discutir as desigualdades de acesso ao saneamento e seus impactos ambientais e sociais."]
conc = ["O experimento demonstrou que o repolho roxo pode ser utilizado como indicador natural de pH, permitindo identificar visualmente diferenças entre substâncias ácidas, neutras e básicas. A pesquisa mostrou também que a discussão sobre água e saneamento ultrapassa a questão química, envolvendo saúde, meio ambiente, qualidade de vida e justiça ambiental. Nesse sentido, o racismo ambiental evidencia a necessidade de discutir as desigualdades que afetam comunidades negras e periféricas. Além disso, a valorização dos conhecimentos ancestrais relacionados às plantas medicinais contribui para reconhecer a importância histórica e cultural da população negra na construção de saberes e práticas de cuidado."]
ref = ["1. BRASIL. Lei nº 10.639/2003. História e Cultura Afro-Brasileira.",
"2. HERCULANO, S. O clamor por justiça ambiental e contra o racismo ambiental. 2008.",
"3. GRUPO PALMARES. 20 de Novembro.",
"4. IBGE. Dados sobre saneamento básico.",
"5. Fontes bibliográficas utilizadas na pesquisa sobre plantas medicinais, racismo ambiental e qualidade da água."]

sizes = {}
for name, p, box in [("intro", intro, (68, 700, 585, 808)), ("obj", obj, (615, 700, 1133, 808)),
    ("met", met, (68, 877, 585, 985)), ("res", res, (617, 877, 1133, 985)),
    ("conc", conc, (70, 1047, 583, 1155)), ("ref", ref, (617, 1047, 1130, 1155))]:
    sizes[name] = fill(p, box, pad=10, lh=1.12, maxsize=16)
print(sizes)
im.save("banner_preenchido.png")
im.convert("RGB").save("banner_preenchido.jpg", quality=95)
print(im.size)

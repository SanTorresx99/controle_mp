# backend/logic/etiquetas.py

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter
import os
import time

ETIQUETA_DIR = "files/etiquetas"

# Ajuste das dimensões reais da etiqueta (largura 78mm x altura 34mm)
LABEL_WIDTH = 78 * mm
LABEL_HEIGHT = 34 * mm

def ajustar_tamanho_texto(canvas_obj, texto, max_largura, fonte="Helvetica", tamanho_inicial=10):
    tamanho = tamanho_inicial
    while canvas_obj.stringWidth(texto, fonte, tamanho) > max_largura and tamanho > 5:
        tamanho -= 1
    return tamanho

def gerar_etiqueta(volume: dict):
    os.makedirs(ETIQUETA_DIR, exist_ok=True)
    codigo_base = f"MP-{volume['numero_nf']}-{volume['id_produto']}"
    caminho_pdf = os.path.join(ETIQUETA_DIR, f"{codigo_base}.pdf")

    c = canvas.Canvas(caminho_pdf, pagesize=(LABEL_WIDTH, LABEL_HEIGHT))
    img_path = os.path.join(ETIQUETA_DIR, f"{volume['codigo_volume']}.png")
    Code128(volume['codigo_volume'], writer=ImageWriter()).write(open(img_path, 'wb'))

    produto_str = f"{volume['id_produto']} - {volume['produto']}"
    fornecedor_str = volume['fornecedor']

    font_prod = ajustar_tamanho_texto(c, produto_str, 70 * mm)
    font_forn = ajustar_tamanho_texto(c, fornecedor_str, 70 * mm)

    # Produto
    c.setFont("Helvetica-Bold", font_prod)
    c.drawString(5 * mm, 27 * mm, produto_str)

    # Fornecedor
    c.setFont("Helvetica", font_forn)
    c.drawString(5 * mm, 24 * mm, fornecedor_str)

    # Quantidade e Data alinhadas horizontalmente
    c.setFont("Helvetica", 8)
    c.drawString(5 * mm, 21 * mm, f"Qtd: {volume['quantidade']} {volume.get('unidade', '')}")
    c.drawRightString(LABEL_WIDTH - 5 * mm, 21 * mm, f"DT REC: {volume['data_recebimento']}")

    # Código de barras ajustado (largura aumentada em ~40% e posição mais abaixo)
    c.drawImage(
        img_path,
        3 * mm,             # posição X
        6 * mm,             # posição Y
        width=72 * mm,      # nova largura aumentada
        height=15 * mm,     # altura reduzida levemente
        preserveAspectRatio=True,
        mask='auto'
    )

    # Texto do código abaixo da imagem
    c.setFont("Helvetica", 9)
    c.drawCentredString(LABEL_WIDTH / 2, 2 * mm, volume['codigo_volume'])

    c.showPage()
    c.save()
    os.remove(img_path)
    return caminho_pdf

def gerar_etiquetas_em_lote(volumes: list):
    if not volumes:
        return None

    os.makedirs(ETIQUETA_DIR, exist_ok=True)
    codigo_base = f"MP-{volumes[0]['numero_nf']}-{volumes[0]['id_produto']}"
    caminho_pdf = os.path.join(ETIQUETA_DIR, f"{codigo_base}.pdf")
    c = canvas.Canvas(caminho_pdf, pagesize=(LABEL_WIDTH, LABEL_HEIGHT))

    for volume in volumes:
        img_path = os.path.join(ETIQUETA_DIR, f"{volume['codigo_volume']}.png")
        Code128(volume['codigo_volume'], writer=ImageWriter()).write(open(img_path, 'wb'))

        produto_str = f"{volume['id_produto']} - {volume['produto']}"
        fornecedor_str = volume['fornecedor']

        font_prod = ajustar_tamanho_texto(c, produto_str, 70 * mm)
        font_forn = ajustar_tamanho_texto(c, fornecedor_str, 70 * mm)

        # Produto
        c.setFont("Helvetica-Bold", font_prod)
        c.drawString(5 * mm, 27 * mm, produto_str)

        # Fornecedor
        c.setFont("Helvetica", font_forn)
        c.drawString(5 * mm, 24 * mm, fornecedor_str)

        # Quantidade e Data
        c.setFont("Helvetica", 8)
        c.drawString(5 * mm, 21 * mm, f"Qtd: {volume['quantidade']} {volume.get('unidade', '')}")
        c.drawRightString(LABEL_WIDTH - 5 * mm, 21 * mm, f"DT REC: {volume['data_recebimento']}")

        # Código de barras ajustado (largura aumentada em ~40% e posição mais abaixo)
        c.drawImage(
            img_path,
            3 * mm,             # posição X
            6 * mm,             # posição Y
            width=72 * mm,      # nova largura aumentada
            height=15 * mm,     # altura reduzida levemente
            preserveAspectRatio=True,
            mask='auto'
        )

        # Texto do código abaixo da imagem
        c.setFont("Helvetica", 9)
        c.drawCentredString(LABEL_WIDTH / 2, 2 * mm, volume['codigo_volume'])

        os.remove(img_path)
        c.showPage()

    c.save()
    return caminho_pdf

def limpar_etiquetas_antigas(dias: int = 2):
    if not os.path.exists(ETIQUETA_DIR):
        return

    agora = time.time()
    limite = dias * 86400

    for nome in os.listdir(ETIQUETA_DIR):
        caminho = os.path.join(ETIQUETA_DIR, nome)
        if caminho.endswith(".pdf") and os.path.isfile(caminho):
            if agora - os.path.getmtime(caminho) > limite:
                os.remove(caminho)
                print(f"[LIMPEZA] Etiqueta removida: {nome}")

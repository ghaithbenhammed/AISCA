from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime
import textwrap


# ============================================
# HEADER + FOOTER par page
# ============================================
def add_page_header_footer(c, width, height, page_num):
    # --- Header ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 35, "AISCA – Rapport d'Analyse de Compétences")

    c.setFont("Helvetica", 9)
    c.drawRightString(width - 40, height - 55, f"Date : {datetime.now().strftime('%d/%m/%Y')}")

    # --- Footer ---
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, 25, f"Page {page_num}")
    c.setFillColor(colors.black)


# ============================================
# WRAP UTILITAIRE (retour ligne auto)
# ============================================
def write_wrapped_text(c, text, x, y, max_chars=95, line_height=14):
    wrapped = textwrap.wrap(text, width=max_chars)
    for line in wrapped:
        if y < 70:  # Nouvelle page si nécessaire
            c.showPage()
            width, height = letter
            add_page_header_footer(c, width, height, 2)
            y = height - 100
        c.drawString(x, y, line)
        y -= line_height
    return y


# ============================================
# GENERATION DU PDF
# ============================================
def generate_pdf(output_path, scores, job, bio, plan, doughnut_img, bar_img):

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    page_num = 1

    add_page_header_footer(c, width, height, page_num)

    y = height - 110

    # ============================================
    # 1) METIER RECOMMANDÉ (BANDEAU)
    # ============================================
    c.setFillColor(colors.HexColor("#000000"))
    c.rect(40, y - 5, width - 80, 30, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width / 2, y + 5, f"🎯 Métier recommandé : {job}")

    c.setFillColor(colors.black)
    y -= 60

    # ============================================
    # 2) GRAPHES (DOUGHNUT + BAR)
    # ============================================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Visualisation des compétences :")
    y -= 15

    c.drawImage(ImageReader(doughnut_img), 40, y - 250, width=240, height=240)
    c.drawImage(ImageReader(bar_img), 310, y - 250, width=240, height=240)

    y -= 280

    # ============================================
    # 3) FORCES & FAIBLESSES
    # ============================================
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    strengths = [f"{k} : {v}%" for k, v in sorted_scores[:2]]
    weaknesses = [f"{k} : {v}%" for k, v in sorted_scores[-2:]]

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Points forts :")
    y -= 18
    c.setFont("Helvetica", 10)

    for s in strengths:
        y = write_wrapped_text(c, f"- {s}", 60, y)

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Points faibles :")
    y -= 18
    c.setFont("Helvetica", 10)

    for w in weaknesses:
        y = write_wrapped_text(c, f"- {w}", 60, y)

    # Nouvelle page si nécessaire
    if y < 120:
        c.showPage()
        page_num += 1
        add_page_header_footer(c, width, height, page_num)
        y = height - 100

    # ============================================
    # 4) BIO PROFESSIONNELLE
    # ============================================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Bio Professionnelle :")
    y -= 25
    c.setFont("Helvetica", 10)

    for paragraph in bio.split("\n"):
        y = write_wrapped_text(c, paragraph, 40, y)

    y -= 20

    # ============================================
    # 5) PLAN D’APPRENTISSAGE
    # ============================================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Plan de Progression :")
    y -= 25
    c.setFont("Helvetica", 10)

    for paragraph in plan.split("\n"):
        y = write_wrapped_text(c, paragraph, 40, y)

    c.save()

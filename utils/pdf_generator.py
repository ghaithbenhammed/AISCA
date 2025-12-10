from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

def generate_pdf(output_path, scores, job, bio, plan, strengths, weaknesses, doughnut_img, bar_img):

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # =========================
    # HEADER
    # =========================
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 50, "AISCA – Rapport d'Analyse de Compétences")

    c.setFont("Helvetica", 10)
    c.drawString(40, height - 65, f"Date : {datetime.now().strftime('%d/%m/%Y')}")

    y = height - 110

    # =========================
    # MÉTIER RECOMMANDÉ
    # =========================
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"🎯 Métier recommandé : {job}")
    y -= 40

    # =========================
    # GRAPHIQUE DOUGHNUT
    # =========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Répartition des compétences :")
    y -= 10

    c.drawImage(ImageReader(doughnut_img), 40, y - 250, width=250, height=250)

    # =========================
    # GRAPHIQUE BAR
    # =========================
    c.drawImage(ImageReader(bar_img), 310, y - 250, width=250, height=250)

    y -= 300

    # =========================
    # FORCES
    # =========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Forces :")
    c.setFont("Helvetica", 11)
    for s in strengths:
        y -= 15
        c.drawString(60, y, f"- {s}")

    y -= 25

    # =========================
    # FAIBLESSES
    # =========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Faiblesses :")
    c.setFont("Helvetica", 11)
    for w in weaknesses:
        y -= 15
        c.drawString(60, y, f"- {w}")

    y -= 40

    # =========================
    # BIO COURTE
    # =========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Bio Professionnelle :")
    y -= 20

    bio_text = c.beginText(40, y)
    bio_text.setFont("Helvetica", 10)
    for line in bio.split("\n"):
        bio_text.textLine(line)
    c.drawText(bio_text)

    y = bio_text.getY() - 30

    # =========================
    # PLAN SYNTHÉTIQUE
    # =========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Plan de progression :")
    y -= 20

    plan_text = c.beginText(40, y)
    plan_text.setFont("Helvetica", 10)
    for line in plan.split("\n"):
        plan_text.textLine(line)
    c.drawText(plan_text)

    c.save()

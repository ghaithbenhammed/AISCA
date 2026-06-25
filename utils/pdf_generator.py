from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime
import textwrap

PAGE_WIDTH, PAGE_HEIGHT = letter


# ============================================================
# HEADER / FOOTER
# ============================================================

def add_header_footer(c, page):

    # Header
    c.setStrokeColor(colors.lightgrey)
    c.line(40, PAGE_HEIGHT - 60, PAGE_WIDTH - 40, PAGE_HEIGHT - 60)

    c.setFont("Helvetica-Bold", 17)
    c.drawString(40, PAGE_HEIGHT - 40,
                 "AISCA - Analyse Sémantique des Compétences")

    c.setFont("Helvetica", 9)

    c.drawRightString(
        PAGE_WIDTH - 40,
        PAGE_HEIGHT - 42,
        datetime.now().strftime("%d/%m/%Y")
    )

    # Footer
    c.setStrokeColor(colors.lightgrey)
    c.line(40, 40, PAGE_WIDTH - 40, 40)

    c.setFont("Helvetica", 9)

    c.setFillColor(colors.grey)

    c.drawCentredString(
        PAGE_WIDTH / 2,
        25,
        f"Page {page}"
    )

    c.setFillColor(colors.black)


# ============================================================
# TITRE DE SECTION
# ============================================================

def section_title(c, title, y):

    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 14)

    c.drawString(40, y, title)

    c.setStrokeColor(colors.black)

    c.line(40, y - 5, PAGE_WIDTH - 40, y - 5)

    return y - 25


# ============================================================
# TEXTE MULTILIGNE
# ============================================================

def draw_paragraph(c, text, x, y,
                   width=90,
                   line_height=14):

    lines = textwrap.wrap(text, width)

    for line in lines:

        if y < 70:

            c.showPage()

            add_header_footer(c, 2)

            y = PAGE_HEIGHT - 70

        c.drawString(x, y, line)

        y -= line_height

    return y


# ============================================================
# PAGE DE GARDE
# ============================================================

def cover_page(c, job):

    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 28)

    c.drawCentredString(

        PAGE_WIDTH / 2,

        PAGE_HEIGHT - 120,

        "AISCA"

    )

    c.setFont("Helvetica", 18)

    c.drawCentredString(

        PAGE_WIDTH / 2,

        PAGE_HEIGHT - 155,

        "Analyse Sémantique des Compétences"

    )

    c.setStrokeColor(colors.black)

    c.line(

        120,

        PAGE_HEIGHT - 175,

        PAGE_WIDTH - 120,

        PAGE_HEIGHT - 175

    )

    c.setFont("Helvetica-Bold", 16)

    c.drawCentredString(

        PAGE_WIDTH / 2,

        PAGE_HEIGHT - 250,

        "Rapport Professionnel"

    )

    c.setFont("Helvetica", 13)

    c.drawCentredString(

        PAGE_WIDTH / 2,

        PAGE_HEIGHT - 330,

        f"Métier recommandé : {job}"

    )

    c.setFont("Helvetica", 12)

    c.drawCentredString(

        PAGE_WIDTH / 2,

        PAGE_HEIGHT - 360,

        datetime.now().strftime("%d/%m/%Y")

    )

    c.setFont("Helvetica-Oblique", 11)

    c.drawCentredString(

        PAGE_WIDTH / 2,

        90,

        "Projet IA Générative - AISCA"

    )

    c.showPage()
# ============================================================
# GENERATION DU RAPPORT
# ============================================================

def generate_pdf(
    output_path,
    scores,
    job,
    bio,
    plan,
    radar_img,
    jobs_img
):

    c = canvas.Canvas(output_path, pagesize=letter)

    # =======================================================
    # PAGE DE GARDE
    # =======================================================

    cover_page(c, job)

    page = 2

    add_header_footer(c, page)

    y = PAGE_HEIGHT - 90

    # =======================================================
    # SCORE GLOBAL
    # =======================================================

    y = section_title(c, "Résumé des résultats", y)

    global_score = int(sum(scores.values()) / len(scores))

    c.setFont("Helvetica", 11)

    c.drawString(
        50,
        y,
        f"Score global du profil : {global_score}%"
    )

    y -= 30

    c.drawString(
        50,
        y,
        f"Métier recommandé : {job}"
    )

    y -= 40

    # =======================================================
    # RADAR
    # =======================================================

    y = section_title(
        c,
        "Radar des compétences",
        y
    )

    if radar_img:

        c.drawImage(
            ImageReader(radar_img),
            60,
            y - 220,
            width=220,
            height=220,
            preserveAspectRatio=True
        )

    # =======================================================
    # TOP METIERS
    # =======================================================

    if jobs_img:

        c.drawImage(
            ImageReader(jobs_img),
            320,
            y - 220,
            width=220,
            height=220,
            preserveAspectRatio=True
        )

    y -= 250

    # =======================================================
    # SCORES DETAILLES
    # =======================================================

    y = section_title(
        c,
        "Scores par domaine",
        y
    )

    c.setFont(
        "Helvetica",
        10
    )

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for domaine, score in sorted_scores:

        c.drawString(
            60,
            y,
            f"{domaine}"
        )

        c.drawRightString(
            PAGE_WIDTH-60,
            y,
            f"{score}%"
        )

        y -= 18

    y -= 15

    # =======================================================
    # FORCES
    # =======================================================

    y = section_title(
        c,
        "Points forts",
        y
    )

    c.setFont(
        "Helvetica",
        10
    )

    for domaine, score in sorted_scores[:2]:

        c.drawString(
            60,
            y,
            f"• {domaine} ({score}%)"
        )

        y -= 18

    y -= 15

    # =======================================================
    # AXES D'AMELIORATION
    # =======================================================

    y = section_title(
        c,
        "Axes d'amélioration",
        y
    )

    c.setFont(
        "Helvetica",
        10
    )

    for domaine, score in sorted_scores[-2:]:

        c.drawString(
            60,
            y,
            f"• {domaine} ({score}%)"
        )

        y -= 18

    # =======================================================
    # NOUVELLE PAGE
    # =======================================================

    c.showPage()

    page += 1

    add_header_footer(c, page)

    y = PAGE_HEIGHT - 90
    # =======================================================
    # BIO PROFESSIONNELLE
    # =======================================================

    y = section_title(
        c,
        "Bio professionnelle générée par l'IA",
        y
    )

    c.setFont("Helvetica", 10)

    for ligne in bio.split("\n"):

        ligne = ligne.strip()

        if ligne:

            y = draw_paragraph(
                c,
                ligne,
                50,
                y
            )

            y -= 5

    y -= 15

    # =======================================================
    # PLAN D'APPRENTISSAGE
    # =======================================================

    y = section_title(
        c,
        "Plan d'apprentissage personnalisé",
        y
    )

    c.setFont("Helvetica", 10)

    for ligne in plan.split("\n"):

        ligne = ligne.strip()

        if ligne:

            y = draw_paragraph(
                c,
                ligne,
                50,
                y
            )

            y -= 5

    # =======================================================
    # SI BESOIN -> NOUVELLE PAGE
    # =======================================================

    if y < 120:

        c.showPage()

        page += 1

        add_header_footer(c, page)

        y = PAGE_HEIGHT - 90

    # =======================================================
    # CONCLUSION
    # =======================================================

    y -= 20

    y = section_title(
        c,
        "Conclusion",
        y
    )

    conclusion = f"""
Cette analyse a été réalisée automatiquement par AISCA
à partir des réponses du questionnaire.

L'analyse sémantique SBERT a permis d'identifier les
compétences dominantes du profil et d'estimer leur
adéquation avec différents métiers de la Data et de l'IA.

Le métier présentant la meilleure correspondance est :

{job}

Les recommandations générées par l'IA ont pour objectif
de guider le candidat dans son évolution professionnelle
et dans le développement de ses compétences.
"""

    c.setFont("Helvetica", 10)

    y = draw_paragraph(
        c,
        conclusion,
        50,
        y
    )

    # =======================================================
    # SIGNATURE
    # =======================================================

    y -= 40

    c.setStrokeColor(colors.grey)

    c.line(
        50,
        y,
        PAGE_WIDTH - 50,
        y
    )

    y -= 25

    c.setFont(
        "Helvetica-Oblique",
        10
    )

    c.drawCentredString(
        PAGE_WIDTH / 2,
        y,
        "Rapport généré automatiquement par AISCA"
    )

    y -= 15

    c.drawCentredString(
        PAGE_WIDTH / 2,
        y,
        "Analyse Sémantique des Compétences & Recommandation de Métiers"
    )

    y -= 15

    c.drawCentredString(
        PAGE_WIDTH / 2,
        y,
        f"Date de génération : {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    # =======================================================
    # SAUVEGARDE
    # =======================================================

    c.save()
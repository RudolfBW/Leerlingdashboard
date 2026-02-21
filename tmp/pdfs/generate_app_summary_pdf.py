from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUTPUT_PATH = "output/pdf/app_summary_overgangsdashboard.pdf"


def heading(text, styles):
    return Paragraph(text, styles["section"])


def bullet_list(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["body"])) for item in items],
        bulletType="bullet",
        bulletFontName="Helvetica",
        bulletFontSize=8,
        leftIndent=12,
        bulletOffsetY=1,
        spaceBefore=1,
        spaceAfter=1,
    )


def build_pdf(path):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="App Summary - Overgangsdashboard",
        author="Codex",
    )

    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155"),
            spaceAfter=7,
        ),
        "section": ParagraphStyle(
            "section",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=colors.HexColor("#0b3a53"),
            spaceBefore=4,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#111827"),
            spaceAfter=1,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#475569"),
            spaceBefore=4,
        ),
    }

    feature_items = [
        "Uploads local Excel files (`.xlsx`) and parses the first worksheet in-browser using SheetJS.",
        "Builds student records from rows using `Leerlingnaam`/`Leerlingnummer`, `Studie`, `Klas`, and `Mentor` fields.",
        "Computes promotion status per student with year-specific rules (`G1` to `G5`) and shows green/orange/red outcomes.",
        "Supports filtering by year, class, mentor, and optional student-number search.",
        "Shows live counters for promoted, discussed, not promoted, and total displayed.",
        "Exports the currently filtered results as a semicolon-separated CSV download.",
    ]

    architecture_items = [
        "UI layer: one static page (`index.html`) with inline CSS and JavaScript; no build step found.",
        "External services: Google Fonts CDN and SheetJS CDN script (`xlsx.full.min.js`).",
        "Data ingestion: user selects `.xlsx` file, browser `FileReader` loads it, SheetJS converts rows to JSON.",
        "Processing: JavaScript normalizes grades, groups/filter records, and runs status functions (`statusG1`, `statusG2orG3`, `statusG4`, `statusG5`).",
        "Presentation/output: DOM table and counters update in real time; CSV export uses `Blob` and temporary object URL.",
        "Backend/API/database/authentication: Not found in repo.",
    ]

    run_items = [
        "Open `/Users/rudolfburggraaf/Documents/GitHub/Project Jan Wessels/index.html` in a modern browser.",
        "Click `Upload leerlingbestand (.xlsx)` and select a valid Excel file (example file exists: `kleine dataset.xlsx`).",
        "Choose `leerjaar` first, then optional `klas` and/or `mentor`; optionally search by student number.",
        "Use `Download CSV` if you want the filtered results as a file.",
        "Install/setup commands or production deployment instructions: Not found in repo.",
    ]

    story = []
    story.append(Paragraph("App Summary: Overgangsdashboard", styles["title"]))
    story.append(Paragraph("Evidence source: repo files only (`index.html`, sample data files).", styles["subtitle"]))

    story.append(heading("What it is", styles))
    story.append(
        Paragraph(
            "A single-page web dashboard for viewing student promotion outcomes from an uploaded Excel file. "
            "It classifies each student into promoted, discussed, or not promoted using built-in grade rules.",
            styles["body"],
        )
    )

    story.append(heading("Who it is for", styles))
    who_table = Table(
        [
            [
                Paragraph("Primary persona", styles["body"]),
                Paragraph(
                    "School staff handling transition decisions (likely mentors/year coordinators), inferred from UI terms like `Klas`, `Mentor`, and `Leerjaar`.",
                    styles["body"],
                ),
            ],
            [
                Paragraph("Explicit persona documentation", styles["body"]),
                Paragraph("Not found in repo.", styles["body"]),
            ],
        ],
        colWidths=[48 * mm, 130 * mm],
        hAlign="LEFT",
    )
    who_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(who_table)

    story.append(heading("What it does", styles))
    story.append(bullet_list(feature_items, styles))

    story.append(heading("How it works (repo-evidence architecture)", styles))
    story.append(bullet_list(architecture_items, styles))

    story.append(heading("How to run (minimal)", styles))
    story.append(bullet_list(run_items, styles))
    story.append(
        Paragraph(
            "MacBook quick start: open Finder, go to `/Users/rudolfburggraaf/Documents/GitHub/Project Jan Wessels`, "
            "then open `index.html` with Safari or Chrome (right-click -> Open With). If browser security blocks local files, "
            "run `python3 -m http.server 8000` in that folder and open `http://localhost:8000`.",
            styles["body"],
        )
    )

    story.append(
        Paragraph(
            "Note: this summary is constrained to code and files present in the repo; missing documentation is marked explicitly.",
            styles["small"],
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf(OUTPUT_PATH)
    print(OUTPUT_PATH)

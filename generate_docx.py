import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    """Set the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def generate_report():
    doc = Document()
    
    # Configure page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette (Indigo/Slate scheme)
    COLOR_PRIMARY = RGBColor(79, 70, 229)   # Indigo #4f46e5
    COLOR_SECONDARY = RGBColor(15, 23, 42)  # Slate-900 #0f172a
    COLOR_TEXT = RGBColor(51, 65, 85)       # Slate-700 #334155
    COLOR_MUTED = RGBColor(100, 116, 139)   # Slate-500 #64748b

    # Style Helpers
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(24)
        run = p.add_run(text)
        run.font.name = 'Trebuchet MS'
        run.font.size = Pt(28)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(36)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_MUTED
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Trebuchet MS'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Trebuchet MS'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_body_text(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_bullet_item(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_code_block(filepath):
        # Fetch file content
        if not os.path.exists(filepath):
            return
        
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        table = doc.add_table(rows=1, cols=1)
        table.autofit = False
        table.columns[0].width = Inches(6.5)
        
        cell = table.cell(0, 0)
        set_cell_background(cell, "F1F5F9")  # Slate-100 background
        
        p = cell.paragraphs[0]
        p.paragraph_format.left_indent = Inches(0.1)
        p.paragraph_format.right_indent = Inches(0.1)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        
        run = p.add_run(code)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate-900 code text

    # --- Title Page Content ---
    add_title("✦ Syntactic Intelligence AI Assistant")
    add_subtitle("Complete Technical Report & Project Documentation\nMajor Project: Prompt Engineering | Powered by Llama-3.1 NIM API")

    # --- Section 1: Introduction & Goals ---
    add_heading_1("1. Project Goals & Learning Objectives")
    add_body_text(
        "The primary goal of the Syntactic Intelligence project is to design and implement a web-based AI assistant "
        "incorporating prompt design variance, output evaluation, and user feedback logs. This project aims to enhance "
        "students' capabilities to formulate systemic prompts that inspire structured thinking, logical evaluation, and "
        "entrepreneurial creativity."
    )
    add_body_text("The assistant is configured to perform three distinct tasks based on Llama-3.1-8B-Instruct LLM responses:")
    add_bullet_item("Answer Questions: Factual Q&A distilled into concise summaries or detailed explanations.")
    add_bullet_item("Summarize Text: Distill long articles or documents while preserving nuance.")
    add_bullet_item("Generate Creative Content: Brainstorm and write stories or poems based on specific input parameters.")

    # --- Section 2: System Architecture ---
    add_heading_1("2. System Architecture & Component Design")
    add_body_text(
        "The project is structured under a flat, light-corporate design metaphor (without glassmorphism) using "
        "Tailwind CSS for maximum structural density and clean border separations."
    )
    add_heading_2("2.1 Backend Pipeline (Flask & NVIDIA NIM API)")
    add_body_text(
        "The app server (app.py) leverages the requests client to connect directly with the NVIDIA NIM chat completion "
        "endpoint. Environment variables (.env) isolate sensitive API credentials. The backend maintains nine prompt templates "
        "mapped to selectable dropdown values."
    )
    add_heading_2("2.2 Thread-Safe Feedback Mechanism")
    add_body_text(
        "A local CSV-based database logger aggregates thumbs up/down user rating inputs. Write operations are guarded "
        "by threading.Lock() primitives in app.py to prevent file collision issues in multi-user local configurations."
    )

    # --- Section 3: Source Code & Implementation Details ---
    add_heading_1("3. Source Code Documentation")
    
    add_heading_2("3.1 Backend Application (app.py)")
    add_body_text("The primary Flask logic mapping routers, prompts, and Llama API configurations:")
    add_code_block("app.py")

    add_heading_2("3.2 Main Frontend Template (templates/index.html)")
    add_body_text("Tailwind-styled main workspace rendering tabs, dynamic prompt structures, and rate submission scripts:")
    add_code_block("templates/index.html")

    add_heading_2("3.3 Analytics Summary Page (templates/feedback_summary.html)")
    add_body_text("Aggregation metrics visualizer plotting overall satisfaction and detailed prompt evaluations:")
    add_code_block("templates/feedback_summary.html")

    add_heading_2("3.4 Project Environment Configuration (.env)")
    add_body_text("Key/URL credential definitions (omitting sensitive keys for git repository pushing):")
    add_code_block(".env")

    # Save Document
    doc.save("AI_Assistant_Technical_Report.docx")
    print("Report generated successfully.")

if __name__ == "__main__":
    generate_report()

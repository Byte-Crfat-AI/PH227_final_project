from PyPDF2 import PdfReader

pdf_file = "handbook_physics_2024-2025_1.pdf"
reader = PdfReader(pdf_file)
pdf_text = ""

for page in reader.pages:
    pdf_text += page.extract_text()
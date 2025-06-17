from docx import Document
from docx.enum.text import WD_BREAK

def replace_text_in_docx(doc: Document, data: dict):
  for paragraph in doc.paragraphs:
    for key, value in data.items():
      for run in paragraph.runs:
        run.text = run.text.replace(f"<{key}>", str(value))
  for table in doc.tables:
    for row in table.rows:
      for cell in row.cells:
        for key, value in data.items():
          cell.text = cell.text.replace(f"<{key}>", str(value))

def insert_page_break_after_paragraph(doc: Document, search_text):
  for paragraph in doc.paragraphs:
    if search_text in paragraph.text:
      run = paragraph.add_run()
      run.add_break(WD_BREAK.PAGE)

def insert_page_break_before_paragraph(doc: Document, search_text: str):
  count = 0
  for i, paragraph in enumerate(doc.paragraphs):
    if search_text in paragraph.text:
      count += 1
      if count == 1:
        continue
      prior_paragraph = doc.paragraphs[i - 1] if i > 0 else None
      if prior_paragraph:
        run = prior_paragraph.add_run()
        run.add_break(WD_BREAK.PAGE)
import pdfkit
import os
from io import BytesIO
import subprocess
import PyPDF2
import tempfile

def html2pdf(titulo, html_path, pdf_path, header_path, footer_path, orientation='Portrait'):
    """
    Convertir HTML a PDF utilizando pdfkit, que es un envoltorio de wkhtmltopdf.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    templates_directory = os.path.abspath(os.path.join(current_directory, '..', 'templates'))

    header_p = os.path.join(templates_directory, 'renderheader.html')
    footer_p = os.path.join(templates_directory, 'renderfooter.html')

    options = {
        'page-size': 'Letter',
        'margin-top': '1.2in',
        'margin-right': '0.6in',
        'margin-bottom': '0.50in',
        'margin-left': '0.6in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,  
        'header-spacing': '3',
        'header-html': header_path,
        'header-center': titulo,
        '--header-font-name': 'Times New Roman', 
        '--header-font-size': '12',
        'footer-center': 'Pág [page] de [topage]',  
        'footer-html': footer_path,
        'footer-font-size': '9',
        'orientation': orientation,        
    }

    if isinstance(pdf_path, BytesIO):
        with open(html_path) as f:
            pdf_bytes = pdfkit.from_file(f, False, options=options)
        pdf_path.write(pdf_bytes)
    elif isinstance(pdf_path, (str, os.PathLike)):
        with open(html_path) as f: 
            pdfkit.from_file(f, pdf_path, options=options)

def docx2pdf(docx_path):
    """
    Convertir un archivo DOCX a PDF utilizando libreoffice
    """
    subprocess.run([
        'C:\Program Files\LibreOffice\program\soffice.exe', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(docx_path), docx_path
      ], check=True)

def merge_pdfs(pdf_list):
    """
    Une una lista de archivos PDF en un solo PDF temporal y retorna su ruta.
    """
    pdf_merger = PyPDF2.PdfMerger()

    try:
        for pdf in pdf_list:
            pdf_merger.append(pdf)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf_merger.write(temp_file.name)
        pdf_merger.close()
        
        return temp_file.name # Ruta del archivo temporal generado

    except Exception as e:
        pdf_merger.close()
        raise RuntimeError(f"Error al unir los PDFs: {e}")
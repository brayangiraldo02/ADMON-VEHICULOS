import pdfkit
import os
from io import BytesIO

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

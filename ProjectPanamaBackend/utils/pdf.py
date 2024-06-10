import pdfkit
import os

def html2pdf(titulo, html_path, pdf_path, footer_path):
    """
    Convertir HTML a PDF utilizando pdfkit, que es un envoltorio de wkhtmltopdf.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    templates_directory = os.path.abspath(os.path.join(current_directory, '..', 'templates'))

    header_path = os.path.join(templates_directory, 'header.html')
    footer_p = os.path.join(templates_directory, 'footer.html')

    print("Header path:", header_path)
    print("Footer path:", footer_p)
    options = {
        'page-size': 'Letter',
        'margin-top': '1.2in',
        'margin-right': '0.6in',
        'margin-bottom': '0.50in',
        'margin-left': '0.6in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'footer-center': '[page]',  # Agrega el número de página en la esquina superior derecha
        'header-html': header_path,
        'header-center': titulo,
        '--header-font-name': 'Times New Roman', 
        '--header-font-size': '14',
        'footer-html': footer_p,
        'header-spacing': '3',
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)

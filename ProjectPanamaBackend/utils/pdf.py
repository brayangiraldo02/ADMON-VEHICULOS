import pdfkit

def html2pdf(titulo, html_path, pdf_path, footer_path):
    """
    Convertir HTML a PDF utilizando pdfkit, que es un envoltorio de wkhtmltopdf.
    """
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
        'header-html': '../templates/header.html',
        'header-center': titulo,
        '--header-font-name': 'Times New Roman', 
        '--header-font-size': '14',
        'footer-html': '../templates/footer.html',
        'header-spacing': '3',
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)

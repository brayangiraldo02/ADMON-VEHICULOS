import pdfkit

config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

def generar_pdf(html_content):
    pdfkit.from_string(html_content, 'C:/Programas/python/backend/meta/Frontend/form1/output10.pdf', configuration=config, options={'enable-local-file-access': ''})
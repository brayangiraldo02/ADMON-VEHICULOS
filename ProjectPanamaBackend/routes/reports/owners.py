from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.propietarios import Propietarios
from schemas.reports import *
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

templateJinja = Jinja2Templates(directory="templates")

ownersReports_router = APIRouter()

@ownersReports_router.get('/directorio-propietarios')
async def get_propietarios_detalles():
    db = session()
    try:
        propietarios_detalles = db.query(
            Propietarios.ESTADO.label('propietario_estado'),
            Propietarios.CODIGO.label('propietario_codigo'),
            Propietarios.NOMBRE.label('propietario_nombre'),
            Propietarios.CIUDAD.label('propietario_ciudad'),
            Propietarios.DIRECCION.label('propietario_direccion'),
            Propietarios.TELEFONO.label('propietario_telefono'),
            Propietarios.CELULAR.label('propietario_celular'),
            Propietarios.CORREO.label('propietario_correo'),
        )  .all()
        
        # Convertir los resultados en un formato JSON
        propietarios_detalles_list = []
        for resultado in propietarios_detalles:
            propietario_detalle = {
                'propietario_estado': resultado.propietario_estado,
                'propietario_codigo': resultado.propietario_codigo,
                'propietario_nombre': resultado.propietario_nombre,
                'propietario_ciudad': resultado.propietario_ciudad,
                'propietario_direccion': resultado.propietario_direccion,
                'propietario_telefono': resultado.propietario_telefono,
                'propietario_celular': resultado.propietario_celular,
                'propietario_correo': resultado.propietario_correo
            }
            propietarios_detalles_list.append(propietario_detalle)
    
        data = agrupar_empresas_por_estado(propietarios_detalles_list)

        # Datos de la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        usuario = "admin" 
        titulo = 'Directorio Propietarios'

        # Inicializar el diccionario data_view con información común
        data_view = {
            "fecha": fecha,
            "hora": hora_actual
        }

        for estado, info in data.items():
            if isinstance(info, dict):
                estado_nombre = info.pop('nombre_estado', 'Sin nombre')
                data_view[estado] = {
                    "nombre_estado": estado_nombre,
                    "empresas": []
                }
                for empresa_codigo, empresa_info in info.items():
                    if isinstance(empresa_info, dict):
                        empresa = {
                            "codigo_empresa": empresa_info.get("propietario_codigo", ""),
                            "nombre": empresa_info.get("propietario_nombre", ""),
                            "ciudad": empresa_info.get("propietario_ciudad", ""),
                            "direccion": empresa_info.get("propietario_direccion", ""),
                            "telefono": empresa_info.get("propietario_telefono", ""),
                            "celular": empresa_info.get("propietario_celular", ""),
                            "correo": empresa_info.get("propietario_correo", ""),
                        }
                        data_view[estado]["empresas"].append(empresa)
        
        data_view["usuario"] = usuario

        headers = {
            "Content-Disposition": "inline; directorio-propietarios.pdf"
        }  

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "DirectorioPropietarios.html"
        header_file = "header.html"
        footer_file = "footer.html"
        template = template_env.get_template(template_file)
        header = template_env.get_template(header_file)
        footer = template_env.get_template(footer_file)
        output_text = template.render(data_view=data_view)
        output_header = header.render(data_view=data_view)
        output_footer = footer.render(data_view=data_view)

        html_path = f'./templates/renderDirectorioPropietarios.html'
        header_path = f'./templates/renderheader.html'
        footer_path = f'./templates/renderfooter.html'
        html_file = open(html_path, 'w')
        header_file = open(header_path, 'w')
        html_footer = open(footer_path, 'w') 
        html_file.write(output_text)
        header_file.write(output_header)
        html_footer.write(output_footer) 
        html_file.close()
        header_file.close()
        html_footer.close()
        pdf_path = 'propietarios-detalles.pdf'
        html2pdf(titulo, html_path, pdf_path, header_path=header_path, footer_path=footer_path)

        response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/propietarios-detalles.pdf', headers=headers)
        
        return response

        #return JSONResponse(content=jsonable_encoder(data))
    finally:
        db.close()
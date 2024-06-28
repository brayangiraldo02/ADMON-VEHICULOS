from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.conductores import Conductores
from schemas.reports import *
from middlewares.JWTBearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

drivers_router = APIRouter()

@drivers_router.get("/drivers", tags=["Drivers"], dependencies=[Depends(JWTBearer())])
async def get_drivers():
  db = session()
  try:
    drivers = db.query(Conductores.CODIGO, Conductores.UND_NRO, Conductores.UND_PRE, Conductores.NOMBRE, Conductores.CEDULA, Conductores.TELEFONO, Conductores.FEC_INGRES, Conductores.CUO_DIARIA, Conductores.NROENTREGA, Conductores.NROENTPAGO, Conductores.NROENTSDO, Conductores.LICEN_VCE, Conductores.CONTACTO, Conductores.TEL_CONTAC, Conductores.PAR_CONTAC, Conductores.CONTACTO1, Conductores.TEL_CONTA1, Conductores.PAR_CONTA1).all()

    drivers_list = [
      {
        'codigo': driver.CODIGO,
        'unidad': driver.UND_NRO + ' - ' + driver.UND_PRE,
        'nombre': driver.NOMBRE,
        'cedula': driver.CEDULA,
        'telefono': driver.TELEFONO,
        'fecha_ingreso': driver.FEC_INGRES,
        'cuota_diaria': driver.CUO_DIARIA,
        'nro_entrega': driver.NROENTREGA,
        'nro_pago': driver.NROENTPAGO,
        'nro_saldo': driver.NROENTSDO,
        'vce_licen': driver.LICEN_VCE,
        'contacto': driver.CONTACTO + ' - ' + driver.TEL_CONTAC + ' - ' + driver.PAR_CONTAC,
        'contacto1': driver.CONTACTO1 + ' - ' + driver.TEL_CONTA1 + ' - ' + driver.PAR_CONTA1
      }
      for driver in drivers
    ]
    return JSONResponse(content=jsonable_encoder(drivers_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

@drivers_router.get('/directorio-conductores')
async def get_conductores_detalles():
    db = session()
    try:
        conductores_detalles = db.query(
            Conductores.ESTADO.label('conductor_estado'),
            Conductores.CODIGO.label('conductor_codigo'),
            Conductores.NOMBRE.label('conductor_nombre'),
            Conductores.CEDULA.label('conductor_cedula'),
            Conductores.CIUDAD.label('conductor_ciudad'),
            Conductores.DIRECCION.label('conductor_direccion'),
            Conductores.TELEFONO.label('conductor_telefono'),
            Conductores.CELULAR.label('conductor_celular'),
        )   .all()
        
        # Convertir los resultados en un formato JSON
        conductores_detalles_list = []
        for resultado in conductores_detalles:
            conductor_detalle = {
                'conductor_estado': resultado.conductor_estado,
                'conductor_codigo': resultado.conductor_codigo,
                'conductor_nombre': resultado.conductor_nombre,
                'conductor_cedula': resultado.conductor_cedula,
                'conductor_ciudad': resultado.conductor_ciudad,
                'conductor_direccion': resultado.conductor_direccion,
                'conductor_telefono': resultado.conductor_telefono,
                'conductor_celular': resultado.conductor_celular,
            }
            conductores_detalles_list.append(conductor_detalle)
    
        data = agrupar_conductores_por_estado(conductores_detalles_list)

        # Datos de la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        usuario = "admin"
        titulo = 'Directorio Conductores'

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
                    "conductores": []
                }
                for conductor_codigo, conductor_info in info.items():
                    if isinstance(conductor_info, dict):
                        conductor = {  
                            "codigo_conductor": conductor_info.get("conductor_codigo", ""),
                            "nombre": conductor_info.get("conductor_nombre", ""),
                            "cedula": conductor_info.get("conductor_cedula", ""),
                            "ciudad": conductor_info.get("conductor_ciudad", ""),
                            "direccion": conductor_info.get("conductor_direccion", ""),
                            "telefono": conductor_info.get("conductor_telefono", ""),
                            "celular": conductor_info.get("conductor_celular", ""),
                        }
                        data_view[estado]["conductores"].append(conductor)

        data_view["usuario"] = usuario

        headers = {
            "Content-Disposition": "inline; detalles-conductores.pdf"
        }  

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "DirectorioConductores.html"
        header_file = "header.html"
        footer_file = "footer.html"
        template = template_env.get_template(template_file)
        header = template_env.get_template(header_file)
        footer = template_env.get_template(footer_file)
        output_text = template.render(data_view=data_view)
        output_header = header.render(data_view=data_view)
        output_footer = footer.render(data_view=data_view)

        html_path = f'./templates/renderDirectorioConductores.html'
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
        pdf_path = 'Conductores-detalles.pdf'
        html2pdf(titulo, html_path, pdf_path, header_path=header_path, footer_path=footer_path)

        response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/Conductores-detalles.pdf', headers=headers)
        
        return response

        #return JSONResponse(content=jsonable_encoder(data))
    finally:
        db.close()
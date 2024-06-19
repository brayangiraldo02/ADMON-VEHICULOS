from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.conductores import Conductores
from schemas.reports import *
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

templateJinja = Jinja2Templates(directory="templates")

feespaidReports_router = APIRouter()


@feespaidReports_router.post('/informe-cuotas-pagas', response_class=FileResponse)
async def get_vehiculos_detalles(infoReports: infoReports):
    db = session()
    try:
        vehiculos_detalles = db.query(
            Propietarios.CODIGO.label('propietario_codigo'),
            Propietarios.NOMBRE.label('propietario_nombre'),
            Conductores.CODIGO.label('conductor_codigo'),
            Conductores.NOMBRE.label('conductor_nombre'),
            Conductores.FEC_INGRES.label('conductor_fecha_ingreso'),
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Conductores.UND_PRE.label('conductor_und_pre'),
            Estados.CODIGO.label('estado_codigo'),
            Estados.NOMBRE.label('estado_nombre'),
            Conductores.CUO_DIARIA.label('conductor_vlr_cuo_diaria'),
            Conductores.NROENTREGA.label('conductor_nro_cuotas'),
            Conductores.NROENTPAGO.label('conductor_nro_cuotas_pagas'),
            Conductores.NROENTSDO.label('conductor_nro_ent_sdo'),   
        )   .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO) \
            .join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO) \
            .all()            
        
        # Convertir los resultados en un formato JSON
        vehiculos_detalles_list = []
        for resultado in vehiculos_detalles:
            vehiculo_detalle = {
                'propietario_codigo': resultado.propietario_codigo,
                'propietario_nombre': resultado.propietario_nombre,
                'conductor_codigo': resultado.conductor_codigo,
                'conductor_nombre': resultado.conductor_nombre,
                'conductor_fecha_ingreso': resultado.conductor_fecha_ingreso,
                'vehiculo_numero': resultado.vehiculo_numero,
                'conductor_und_pre': resultado.conductor_und_pre,
                'estado_codigo': resultado.estado_codigo,
                'estado_nombre': resultado.estado_nombre,
                'conductor_vlr_cuo_diaria': resultado.conductor_vlr_cuo_diaria,
                'conductor_nro_cuotas': resultado.conductor_nro_cuotas,
                'conductor_nro_cuotas_pagas': resultado.conductor_nro_cuotas_pagas,
                'conductor_nro_ent_sdo': resultado.conductor_nro_ent_sdo
            }
            vehiculos_detalles_list.append(vehiculo_detalle)

        codigos_estados_deseados = infoReports.estados
    
        data = cuotas_pagas(vehiculos_detalles_list, codigos_estados_deseados)

        claves_deseadas = infoReports.empresas

        # Crear un nuevo diccionario con los datos de las claves deseadas
        datos = {clave: data.get(clave, {}) for clave in claves_deseadas}

        # Datos de la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        usuario = infoReports.usuario 
        titulo = 'Informe Cuotas Pagas de conductores'

        # Inicializar el diccionario data_view con información común
        data_view = {
            "fecha": fecha,
            "hora": hora_actual
        }

        # Iterar sobre las empresas y vehículos
        total = 0
        for empresa, info in datos.items(): 
            if isinstance(info, dict):
                data_view[empresa] = {
                    "codigo_empresa": info.get("propietario_codigo", 0),
                    "nombre_empresa": info.get("propietario_nombre", 0),
                    "empty": info.get("empty", 0)
                }
                consecutivo = 1
                for vehiculo, vehiculo_info in info.items():
                    if isinstance(vehiculo_info, dict):
                        data_view[vehiculo] = {
                            "consecutivo": consecutivo,
                            "codigo_empresa": info.get("propietario_codigo", 0),
                            "codigo_conductor": vehiculo_info.get("conductor_codigo", 0),
                            "nombre": vehiculo_info.get("conductor_nombre", 0),
                            "fecha_ingreso": vehiculo_info.get("conductor_fecha_ingreso", 0),
                            "numero": vehiculo_info.get("vehiculo_numero", 0),
                            "prestado": vehiculo_info.get("conductor_und_pre", 0),
                            "estado": vehiculo_info.get("estado_nombre", 0),
                            "valor": vehiculo_info.get("conductor_vlr_cuo_diaria", 0),
                            "num_cuotas": vehiculo_info.get("conductor_nro_cuotas", 0),
                            "num_cuotas_pagas": vehiculo_info.get("conductor_nro_cuotas_pagas", 0),
                            "num_cuotas_pendientes": vehiculo_info.get("conductor_nro_ent_sdo", 0),
                        }
                        consecutivo += 1
                        total += 1
                    else:
                        pass
        
        data_view["total"] = total
        data_view["usuario"] = usuario

        headers = {
            "Content-Disposition": "inline; informe-cuotas-pagas.pdf"
        }  

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "InformeCuotas.html"
        header_file = "header.html"
        footer_file = "footer.html"
        template = template_env.get_template(template_file)
        header = template_env.get_template(header_file)
        footer = template_env.get_template(footer_file)
        output_text = template.render(data_view=data_view)
        output_header = header.render(data_view=data_view)
        output_footer = footer.render(data_view=data_view)

        html_path = f'./templates/renderInformeCuotas.html'
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
        pdf_path = 'informe-cuotas-pagas.pdf'
        html2pdf(titulo, html_path, pdf_path, header_path=header_path, footer_path=footer_path)

        response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/informe-cuotas-pagas.pdf', headers=headers)
        
        return response

        #return JSONResponse(content=jsonable_encoder(datos))
    finally:
        db.close()

#-----------------------------------------------------------------------------------------
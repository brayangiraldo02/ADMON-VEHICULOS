from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.infoempresas import InfoEmpresas
from config.dbconnection import session
from models.estados import Estados
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.conductores import Conductores
from schemas.reports import *
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime
import pytz

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

templateJinja = Jinja2Templates(directory="templates")

feespaidReports_router = APIRouter()


@feespaidReports_router.post('/informe-cuotas-pagas/', response_class=FileResponse)
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
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.DOC_RESCIV.label('vehiculo_nro_poliza'),
            Vehiculos.FEC_RESCIV.label('vehiculo_fec_poliza'),
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
            # Format vehiculo_fec_poliza
            formatted_fec_poliza = None
            # Check if it's a datetime object and has a valid year
            if isinstance(resultado.vehiculo_fec_poliza, datetime) and resultado.vehiculo_fec_poliza.year > 1:
                try:
                    formatted_fec_poliza = resultado.vehiculo_fec_poliza.strftime('%Y-%m-%d')
                except ValueError: # Handle potential invalid date values
                    formatted_fec_poliza = None

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
                'vehiculo_nro_cupo': resultado.vehiculo_nro_cupo,
                'vehiculo_nro_poliza': resultado.vehiculo_nro_poliza,
                'vehiculo_fec_poliza': formatted_fec_poliza if formatted_fec_poliza else "",
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

        id_owner = claves_deseadas[0]

        info_owner = db.query(
            Propietarios.EMPRESA.label('codigo_empresa'),
            Propietarios.NOMBRE.label('propietario_nombre'),
        ).filter(Propietarios.CODIGO == id_owner).first()

        info_empresa = db.query(
            InfoEmpresas.NOMBRE,
            InfoEmpresas.NIT,
            InfoEmpresas.LOGO
        ) \
        .filter(InfoEmpresas.ID == info_owner.codigo_empresa).first()
        
        # Datos de la fecha y hora actual
        # Define la zona horaria de Ciudad de Panamá
        panama_timezone = pytz.timezone('America/Panama')
        # Obtén la hora actual en la zona horaria de Ciudad de Panamá
        now_in_panama = datetime.now(panama_timezone)
        # Formatea la fecha y la hora según lo requerido
        fecha = now_in_panama.strftime("%d/%m/%Y")
        hora_actual = now_in_panama.strftime("%I:%M:%S %p")
        usuario = infoReports.usuario 
        titulo = 'Informe Cuotas Pagas de conductores'

        # Inicializar el diccionario data_view con información común
        data_view = {
            "fecha": fecha,
            "hora": hora_actual,
            "nombre_empresa": info_empresa.NOMBRE,
            "nit_empresa": info_empresa.NIT,
            "logo_empresa": info_empresa.LOGO,
        }

        # Iterar sobre las empresas y vehículos
        total = 0
        # Ordenar las empresas alfabéticamente
        empresas_ordenadas = sorted(datos.items(), key=lambda x: x[1].get('propietario_nombre', ''))
        
        for empresa, info in empresas_ordenadas:
            if isinstance(info, dict):
                data_view[empresa] = {
                    "codigo_empresa": info.get("propietario_codigo", 0),
                    "nombre_empresa": info.get("propietario_nombre", 0),
                    "empty": info.get("empty", 0)
                }
                
                # Recopilar vehículos y ordenarlos por número
                vehiculos_ordenados = []
                for vehiculo, vehiculo_info in info.items():
                    if isinstance(vehiculo_info, dict) and 'vehiculo_numero' in vehiculo_info:
                        vehiculos_ordenados.append((vehiculo, vehiculo_info))
                
                # Ordenar la lista de vehículos por su número
                vehiculos_ordenados.sort(key=lambda x: x[1]['vehiculo_numero'])
                
                # Procesar los vehículos ordenados
                consecutivo = 1
                for vehiculo, vehiculo_info in vehiculos_ordenados:
                    data_view[vehiculo] = {
                        "consecutivo": consecutivo,
                        "codigo_empresa": info.get("propietario_codigo", 0),
                        "codigo_conductor": vehiculo_info.get("conductor_codigo", 0),
                        "nombre": vehiculo_info.get("conductor_nombre", 0),
                        "fecha_ingreso": vehiculo_info.get("conductor_fecha_ingreso") or "",
                        "numero": vehiculo_info.get("vehiculo_numero", 0),
                        "prestado": vehiculo_info.get("conductor_und_pre", 0),
                        "estado": vehiculo_info.get("estado_nombre", 0),
                        "nro_cupo": vehiculo_info.get("vehiculo_nro_cupo", 0),
                        "nro_poliza": vehiculo_info.get("vehiculo_nro_poliza", 0),
                        "fec_poliza": vehiculo_info.get("vehiculo_fec_poliza") or "",
                        "valor": vehiculo_info.get("conductor_vlr_cuo_diaria", 0),
                        "num_cuotas": vehiculo_info.get("conductor_nro_cuotas", 0),
                        "num_cuotas_pagas": vehiculo_info.get("conductor_nro_cuotas_pagas", 0),
                        "num_cuotas_pendientes": vehiculo_info.get("conductor_nro_ent_sdo", 0),
                    }
                    consecutivo += 1
                    total += 1
        
        data_view["total"] = total
        data_view["usuario"] = usuario

        headers = {
            "Content-Disposition": "inline; informe-cuotas-pagas.pdf"
        }  

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "InformeCuotas.html"
        header_file = "headerV2.html"
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
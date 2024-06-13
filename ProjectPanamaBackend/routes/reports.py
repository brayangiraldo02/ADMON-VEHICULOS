from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.conductores import Conductores
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

templateJinja = Jinja2Templates(directory="templates")

reports_router = APIRouter()

@reports_router.get('/estado-vehiculos-resumen', response_class=FileResponse)
async def get_conteo_vehiculos_estados():
  db = session()
  try:
    conteo_vehiculos_estados = db.query(Estados.CODIGO, Estados.NOMBRE, Vehiculos.NUMERO) \
    .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
    .all()
    vehiculos_estados_list = [{'codigo': vehiculo.CODIGO, 'nombre': vehiculo.NOMBRE, 'numero': vehiculo.NUMERO} for vehiculo in conteo_vehiculos_estados]
    data = fun_conteo_vehiculos_estados(vehiculos_estados_list)
    data = data.get("conteo_placas")
    # Datos de la fecha y hora actual
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    usuario = "admin" 
    titulo = 'Informe Por Estados General'

    # Inicializar el diccionario data_view con información común
    data_view = {
        "fecha": fecha,
        "hora": hora_actual
    }

    # Activos
    data_view["cant_activo"] = data.get("ACTIVO", 0)
    data_view["cant_backup"] = data.get("BACUPK", 0)
    data_view["cant_activo_backup"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0)
    data_view["cant_chap_parado"] = data.get("CHAPISTERIA PARADO", 0)
    data_view["cant_chap_trabajando"] = data.get("CHAPISTERIA TRABAJANDO", 0)
    data_view["cant_custodia"] = data.get("CUSTODIA", 0)
    data_view["cant_detenido"] = data.get("DETENIDO", 0)
    data_view["cant_esp_operador"] = data.get("ESPERANDO OPERADOR", 0)
    data_view["cant_mecanica_mantenimiento"] = data.get("MECANICA MANTENIMIENTO", 0)
    data_view["cant_mecanica_parado"] = data.get("MECANICA PARADOS", 0)
    data_view["cant_otros"] = data.get("OTROS", 0)
    data_view["cant_vehiculos_pendientes_arraijan"] = data.get("VEHICULOS PENDIENTES ARRAIJAN", 0)
    # Otros Estados
    data_view["cant_traspasados"] = data.get("» CARROS TRASPASADOS", 0)
    data_view["cant_fin_contrato"] = data.get("» CULMINACION DE CONTRATO", 0)
    data_view["cant_en_tramite"] = data.get("» EN TRAMITE", 0)
    data_view["cant_fuera_circulacion"] = data.get("» Fuera de Circulacion", 0)
    data_view["cant_inactivos"] = data.get("» INACTIVOS", 0)
    data_view["cant_perdida_total"] = data.get("» PERDIDA TOTAL", 0)
    data_view["cant_retirado_empresa"] = data.get("» RETIRADO DE LA EMPRESA", 0)
    data_view["cant_sin_calificar"] = data.get("» SIN CLASIFICAR", 0)
    data_view["cant_vendidos"] = data.get("» VENDIDO", 0)
    data_view["cant_para_venta"] = data.get("» Vehiculos Para la Venta", 0)
    # Totales

    data_view["total_activos"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0) + data.get("CHAPISTERIA PARADO", 0) + data.get("CHAPISTERIA TRABAJANDO", 0) + data.get("CUSTODIA", 0) + data.get("DETENIDO", 0) + data.get("ESPERANDO OPERADOR", 0) + data.get("MECANICA MANTENIMIENTO", 0) + data.get("MECANICA PARADOS", 0) + data.get("OTROS", 0) + data.get("VEHICULOS PENDIENTES ARRAIJAN", 0)

    data_view["total_parados"] = data.get("» CARROS TRASPASADOS", 0) + data.get("» CULMINACION DE CONTRATO", 0) + data.get("» EN TRAMITE", 0) + data.get("» Fuera de Circulacion", 0) + data.get("» INACTIVOS", 0) + data.get("» PERDIDA TOTAL", 0) + data.get("» RETIRADO DE LA EMPRESA", 0) + data.get("» SIN CLASIFICAR", 0) + data.get("» VENDIDO", 0) + data.get("» Vehiculos Para la Venta", 0)

    data_view["total_vehiculos"] = data_view["total_activos"] + data_view["total_parados"]

    data_view["promedio_activos"] = round((data_view["cant_activo_backup"] / data_view["total_activos"] * 100), 2)

    data_view["promedio_parados"] = round((100 - data_view["promedio_activos"]), 2)

    headers = {
        "Content-Disposition": "inline; estado-vehiculos-resumen.pdf"
    }  

    data_view["usuario"] = usuario

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "form1.html"
    header_file = "header1.html"
    footer_file = "footer1.html"
    template = template_env.get_template(template_file)
    header = template_env.get_template(header_file)
    footer = template_env.get_template(footer_file)
    output_text = template.render(data_view) 
    output_header = header.render(data_view)
    output_footer = footer.render(data_view)

    html_path = f'./templates/renderform1.html'
    header_path = f'./templates/renderheader1.html'
    footer_path = f'./templates/renderfooter1.html'
    html_file = open(html_path, 'w')
    header_file = open(header_path, 'w')
    html_footer = open(footer_path, 'w')
    html_file.write(output_text)
    header_file.write(output_header)
    html_footer.write(output_footer)
    html_file.close()
    header_file.close()
    html_footer.close()
    pdf_path = 'estado-vehiculos-resumen.pdf'
    html2pdf(titulo,html_path, pdf_path, header_path=header_path, footer_path=footer_path)

    response =  FileResponse(pdf_path, media_type='application/pdf', filename='templates/estado-vehiculos-resumen.pdf', headers=headers)
    #response = JSONResponse(content=jsonable_encoder(data))

    return response
  finally:
    db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/estado-vehiculos-resumen-empresa/{id}', response_class=FileResponse)
async def get_conteo_propietarios_vehiculos_estados(id: int):
    db = session()
    try:
        conteo_propietarios_vehiculos_estados = db.query(
            Propietarios.CODIGO.label('propietario_codigo'), 
            Propietarios.NOMBRE.label('propietario_nombre'), 
            Estados.CODIGO.label('estado_codigo'),
            Estados.NOMBRE.label('estado_nombre'), 
            Vehiculos.NUMERO.label('vehiculo_numero')
        ) \
        .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
        .join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO) \
        .filter(Propietarios.CODIGO == id) \
        .all()

        vehiculos_estados_propietarios_list = [] 
        for resultado in conteo_propietarios_vehiculos_estados:
            propietarios_vehiculos_estados = {
                'propietario_codigo': resultado.propietario_codigo,
                'propietario_nombre': resultado.propietario_nombre,
                'estado_codigo': resultado.estado_codigo,
                'estado_nombre': resultado.estado_nombre,
                'vehiculo_numero': resultado.vehiculo_numero
            }
            vehiculos_estados_propietarios_list.append(propietarios_vehiculos_estados)

        data = obtener_conteo_por_propietario(vehiculos_estados_propietarios_list)
        data = data.get("conteo_por_empresa")
        data = data.get(str(id))  # Usa el id directamente

        # Datos de la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        usuario = "admin" 
        titulo = 'Informe Por Estados General'

        # Inicializar el diccionario data_view con información común
        data_view = {
            "fecha": fecha,
            "hora": hora_actual,
            "codigo_empresa": id
        }
        
        data_view["empresa"] = data.get("nombre_empresa", 0)
        data_view["cant_activo"] = data.get("ACTIVO", 0)
        data_view["cant_backup"] = data.get("BACUPK", 0)
        data_view["cant_activo_backup"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0)
        data_view["cant_chap_parado"] = data.get("CHAPISTERIA PARADO", 0)
        data_view["cant_chap_trabajando"] = data.get("CHAPISTERIA TRABAJANDO", 0)
        data_view["cant_custodia"] = data.get("CUSTODIA", 0)
        data_view["cant_detenido"] = data.get("DETENIDO", 0)
        data_view["cant_esp_operador"] = data.get("ESPERANDO OPERADOR", 0)
        data_view["cant_mecanica_mantenimiento"] = data.get("MECANICA MANTENIMIENTO", 0)
        data_view["cant_mecanica_parado"] = data.get("MECANICA PARADOS", 0)
        data_view["cant_otros"] = data.get("OTROS", 0)
        data_view["cant_vehiculos_pendientes_arraijan"] = data.get("VEHICULOS PENDIENTES ARRAIJAN", 0)
        data_view["cant_traspasados"] = data.get("» CARROS TRASPASADOS", 0)
        data_view["cant_fin_contrato"] = data.get("» CULMINACION DE CONTRATO", 0)
        data_view["cant_en_tramite"] = data.get("» EN TRAMITE", 0)
        data_view["cant_fuera_circulacion"] = data.get("» Fuera de Circulacion", 0)
        data_view["cant_inactivos"] = data.get("» INACTIVOS", 0)
        data_view["cant_perdida_total"] = data.get("» PERDIDA TOTAL", 0)
        data_view["cant_retirado_empresa"] = data.get("» RETIRADO DE LA EMPRESA", 0)
        data_view["cant_sin_calificar"] = data.get("» SIN CLASIFICAR", 0)
        data_view["cant_vendidos"] = data.get("» VENDIDO", 0)
        data_view["cant_para_venta"] = data.get("» Vehiculos Para la Venta", 0)
        data_view["total_activos"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0) + data.get("CHAPISTERIA PARADO", 0) + data.get("CHAPISTERIA TRABAJANDO", 0) + data.get("CUSTODIA", 0) + data.get("DETENIDO", 0) + data.get("ESPERANDO OPERADOR", 0) + data.get("MECANICA MANTENIMIENTO", 0) + data.get("MECANICA PARADOS", 0) + data.get("OTROS", 0) + data.get("VEHICULOS PENDIENTES ARRAIJAN", 0)
        data_view["total_parados"] = data.get("» CARROS TRASPASADOS", 0) + data.get("» CULMINACION DE CONTRATO", 0) + data.get("» EN TRAMITE", 0) + data.get("» Fuera de Circulacion", 0) + data.get("» INACTIVOS", 0) + data.get("» PERDIDA TOTAL", 0) + data.get("» RETIRADO DE LA EMPRESA", 0) + data.get("» SIN CLASIFICAR", 0) + data.get("» VENDIDO", 0) + data.get("» Vehiculos Para la Venta", 0)
        data_view["total_vehiculos"] = data_view["total_activos"] + data_view["total_parados"]
        if data_view["total_activos"] == 0:
            data_view["promedio_activos"] = 0
        else:
           data_view["promedio_activos"] = round((data_view["cant_activo_backup"] / data_view["total_activos"] * 100), 2)
        data_view["promedio_parados"] = round((100 - data_view["promedio_activos"]), 2) 

        titulo = 'Informe Por Estados General'
        usuario = 'Usuario de Prueba'

        data_view["usuario"] = usuario

        headers = {
            "Content-Disposition": "inline; estado-vehiculos-resumen-empresa.pdf"
        }  

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "form1.html"
        header_file = "header1.html"
        footer_file = "footer1.html"
        template = template_env.get_template(template_file)
        header = template_env.get_template(header_file)
        footer = template_env.get_template(footer_file)
        output_text = template.render(data_view) 
        output_header = header.render(data_view)
        output_footer = footer.render(data_view)

        html_path = f'./templates/renderform1.html'
        header_path = f'./templates/renderheader1.html'
        footer_path = f'./templates/renderfooter1.html'
        html_file = open(html_path, 'w')
        header_file = open(header_path, 'w')
        html_footer = open(footer_path, 'w')
        html_file.write(output_text)
        header_file.write(output_header)
        html_footer.write(output_footer)
        html_file.close()
        header_file.close()
        html_footer.close()
        pdf_path = 'estado-vehiculos-resumen.pdf'
        html2pdf(titulo,html_path, pdf_path, header_path=header_path, footer_path=footer_path)

        response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/estado-vehiculos-resumen-empresa.pdf', headers=headers)

        return response
    finally:
        db.close()
#-----------------------------------------------------------------------------------------


@reports_router.get('/informe-estados-detallado', response_class=FileResponse)
async def get_conteo_vehiculos_estados_numeros():
  db = session()
  try:
    conteo_propietarios_vehiculos_estados = db.query(
        Estados.CODIGO.label('estado_codigo'),
        Estados.NOMBRE.label('estado_nombre'),
        Vehiculos.NUMERO.label('vehiculo_numero')
    ).join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO).all()

    vehiculos_estados_list = []
    for resultado in conteo_propietarios_vehiculos_estados:
        vehiculos_estados = {
            'estado_codigo': resultado.estado_codigo,
            'estado_nombre': resultado.estado_nombre,
            'vehiculo_numero': resultado.vehiculo_numero
        }
        vehiculos_estados_list.append(vehiculos_estados)
    data = obtener_numeros_por_estado(vehiculos_estados_list)
    data = data.get("numeros_por_estado")
    # Datos de la fecha y hora actual
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora_actual = datetime.now().strftime("%H:%M:%S")

    # Inicializar el diccionario data_view con información común
    data_view = {
        "fecha": fecha,
        "hora": hora_actual
    }
    # Activos
    data_view["cant_activo"] = len(data.get("ACTIVO", []))
    data_view["activos"] = data.get("ACTIVO", [])
    data_view["cant_backup"] = len(data.get("BACUPK", []))
    data_view["backup"] = data.get("BACUPK", [])
    data_view["cant_activo_backup"] = len(data.get("ACTIVO", [])) + len(data.get("BACUPK", []))
    data_view["cant_chap_parado"] = len(data.get("CHAPISTERIA PARADO", []))
    data_view["chap_parado"] = data.get("CHAPISTERIA PARADO", [])
    data_view["cant_chap_trabajando"] = len(data.get("CHAPISTERIA TRABAJANDO", []))
    data_view["chap_trabajando"] = data.get("CHAPISTERIA TRABAJANDO", [])
    data_view["cant_custodia"] = len(data.get("CUSTODIA", []))
    data_view["custodia"] = data.get("CUSTODIA", [])
    data_view["cant_detenido"] = len(data.get("DETENIDO", []))
    data_view["detenido"] = data.get("DETENIDO", [])
    data_view["cant_esp_operador"] = len(data.get("ESPERANDO OPERADOR", []))
    data_view["esp_operador"] = data.get("ESPERANDO OPERADOR", [])
    data_view["cant_mecanica_mantenimiento"] = len(data.get("MECANICA MANTENIMIENTO", []))
    data_view["mecanica_mantenimiento"] = data.get("MECANICA MANTENIMIENTO", [])
    data_view["cant_mecanica_parado"] = len(data.get("MECANICA PARADOS", []))
    data_view["mecanica_parado"] = data.get("MECANICA PARADOS", [])
    data_view["cant_otros"] = len(data.get("OTROS", []))
    data_view["otros"] = data.get("OTROS", [])
    data_view["cant_vehiculos_pendientes_arraijan"] = len(data.get("VEHICULOS PENDIENTES ARRAIJAN", []))
    data_view["vehiculos_pendientes_arraijan"] = data.get("VEHICULOS PENDIENTES ARRAIJAN", [])
    # Otros Estados
    data_view["cant_traspasados"] = len(data.get("» CARROS TRASPASADOS", []))
    data_view["traspasados"] = data.get("» CARROS TRASPASADOS", [])
    data_view["cant_fin_contrato"] = len(data.get("» CULMINACION DE CONTRATO", []))
    data_view["fin_contrato"] = data.get("» CULMINACION DE CONTRATO", [])
    data_view["cant_en_tramite"] = len(data.get("» EN TRAMITE", []))
    data_view["en_tramite"] = data.get("» EN TRAMITE", [])
    data_view["cant_fuera_circulacion"] = len(data.get("» Fuera de Circulacion", []))
    data_view["fuera_circulacion"] = data.get("» Fuera de Circulacion", [])
    data_view["cant_inactivos"] = len(data.get("» INACTIVOS", []))
    data_view["inactivos"] = data.get("» INACTIVOS", [])
    data_view["cant_perdida_total"] = len(data.get("» PERDIDA TOTAL", []))
    data_view["perdida_total"] = data.get("» PERDIDA TOTAL", [])
    data_view["cant_retirado_empresa"] = len(data.get("» RETIRADO DE LA EMPRESA", []))
    data_view["retirado_empresa"] = data.get("» RETIRADO DE LA EMPRESA", [])
    data_view["cant_sin_calificar"] = len(data.get("» SIN CLASIFICAR", []))
    data_view["sin_calificar"] = data.get("» SIN CLASIFICAR", [])
    data_view["cant_vendidos"] = len(data.get("» VENDIDO", []))
    data_view["vendidos"] = data.get("» VENDIDO", [])
    data_view["cant_para_venta"] = len(data.get("» Vehiculos Para la Venta", []))
    data_view["para_venta"] = data.get("» Vehiculos Para la Venta", [])
    # Totales

    data_view["total_activos"] = len(data.get("ACTIVO", [])) + len(data.get("BACUPK", [])) + len(data.get("CHAPISTERIA PARADO", [])) + len(data.get("CHAPISTERIA TRABAJANDO", [])) + len(data.get("CUSTODIA", [])) + len(data.get("DETENIDO", [])) + len(data.get("ESPERANDO OPERADOR", [])) + len(data.get("MECANICA MANTENIMIENTO", [])) + len(data.get("MECANICA PARADOS", [])) + len(data.get("OTROS", [])) + len(data.get("VEHICULOS PENDIENTES ARRAIJAN", []))

    data_view["total_parados"] = len(data.get("» CARROS TRASPASADOS", [])) + len(data.get("» CULMINACION DE CONTRATO", [])) + len(data.get("» EN TRAMITE", [])) + len(data.get("» Fuera de Circulacion", [])) + len(data.get("» INACTIVOS", [])) + len(data.get("» PERDIDA TOTAL", [])) + len(data.get("» RETIRADO DE LA EMPRESA", [])) + len(data.get("» SIN CLASIFICAR", [])) + len(data.get("» VENDIDO", [])) + len(data.get("» Vehiculos Para la Venta", []))

    data_view["total_vehiculos"] = data_view["total_activos"] + data_view["total_parados"]

    data_view["promedio_activos"] = round((data_view["cant_activo_backup"] / data_view["total_activos"] * 100), 2)

    data_view["promedio_parados"] = round((100 - data_view["promedio_activos"]), 2)

    headers = {
        "Content-Disposition": "inline; estado-vehiculos-numeros.pdf"
    }  

    titulo = 'Informe Por Estados Detallado'
    usuario = 'Usuario de Prueba'

    data_view["usuario"] = usuario

    headers = {
        "Content-Disposition": "inline; informe-estados-detallado.pdf"
    }  

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "form2.html"
    header_file = "header1.html"
    footer_file = "footer1.html"
    template = template_env.get_template(template_file)
    header = template_env.get_template(header_file)
    footer = template_env.get_template(footer_file)
    output_text = template.render(data_view) 
    output_header = header.render(data_view)
    output_footer = footer.render(data_view)

    html_path = f'./templates/renderform2.html'
    header_path = f'./templates/renderheader1.html'
    footer_path = f'./templates/renderfooter1.html'
    html_file = open(html_path, 'w')
    header_file = open(header_path, 'w')
    html_footer = open(footer_path, 'w')
    html_file.write(output_text)
    header_file.write(output_header)
    html_footer.write(output_footer)
    html_file.close()
    header_file.close()
    html_footer.close()
    pdf_path = 'informe-estados-detallado.pdf'
    html2pdf(titulo,html_path, pdf_path, header_path=header_path, footer_path=footer_path)

    response =  FileResponse(pdf_path, media_type='application/pdf', filename='templates/informe-estados-detallado.pdf', headers=headers)

    return response
    #return JSONResponse(content=jsonable_encoder(data))
  finally:
    db.close()

# -----------------------------------------------------------------------------------------

@reports_router.get('/informe-estados-detallado-empresa/{id}', response_class=FileResponse)
async def get_conteo_propietarios_vehiculos_estados_numeros(id: int):
  db = session()
  try:
    conteo_propietarios_vehiculos_estados = db.query(
        Propietarios.CODIGO.label('propietario_codigo'),
        Propietarios.NOMBRE.label('propietario_nombre'),
        Estados.CODIGO.label('estado_codigo'),
        Estados.NOMBRE.label('estado_nombre'),
        Vehiculos.NUMERO.label('vehiculo_numero')
    ).join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO).join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO).filter(Propietarios.CODIGO == id).all()

    vehiculos_estados_propietarios_list = []
    for resultado in conteo_propietarios_vehiculos_estados:
        propietarios_vehiculos_estados = {
            'propietario_codigo': resultado.propietario_codigo,
            'propietario_nombre': resultado.propietario_nombre,
            'estado_codigo': resultado.estado_codigo,
            'estado_nombre': resultado.estado_nombre,
            'vehiculo_numero': resultado.vehiculo_numero
        }
        vehiculos_estados_propietarios_list.append(propietarios_vehiculos_estados)
    data = obtener_numeros_por_propietario(vehiculos_estados_propietarios_list)
    data = data.get("numeros_por_propietario")
    data = data.get(str(id))  
    # Datos de la fecha y hora actual
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora_actual = datetime.now().strftime("%H:%M:%S")

    # Inicializar el diccionario data_view con información común
    data_view = {
        "fecha": fecha,
        "hora": hora_actual, 
        "codigo_empresa": id
    }
    data_view["empresa"] = data.get("nombre_empresa", 0)
    # Activos
    data_view["cant_activo"] = len(data.get("ACTIVO", []))
    data_view["activos"] = data.get("ACTIVO", [])
    data_view["cant_backup"] = len(data.get("BACUPK", []))
    data_view["backup"] = data.get("BACUPK", [])
    data_view["cant_activo_backup"] = len(data.get("ACTIVO", [])) + len(data.get("BACUPK", []))
    data_view["cant_chap_parado"] = len(data.get("CHAPISTERIA PARADO", []))
    data_view["chap_parado"] = data.get("CHAPISTERIA PARADO", [])
    data_view["cant_chap_trabajando"] = len(data.get("CHAPISTERIA TRABAJANDO", []))
    data_view["chap_trabajando"] = data.get("CHAPISTERIA TRABAJANDO", [])
    data_view["cant_custodia"] = len(data.get("CUSTODIA", []))
    data_view["custodia"] = data.get("CUSTODIA", [])
    data_view["cant_detenido"] = len(data.get("DETENIDO", []))
    data_view["detenido"] = data.get("DETENIDO", [])
    data_view["cant_esp_operador"] = len(data.get("ESPERANDO OPERADOR", []))
    data_view["esp_operador"] = data.get("ESPERANDO OPERADOR", [])
    data_view["cant_mecanica_mantenimiento"] = len(data.get("MECANICA MANTENIMIENTO", []))
    data_view["mecanica_mantenimiento"] = data.get("MECANICA MANTENIMIENTO", [])
    data_view["cant_mecanica_parado"] = len(data.get("MECANICA PARADOS", []))
    data_view["mecanica_parado"] = data.get("MECANICA PARADOS", [])
    data_view["cant_otros"] = len(data.get("OTROS", []))
    data_view["otros"] = data.get("OTROS", [])
    data_view["cant_vehiculos_pendientes_arraijan"] = len(data.get("VEHICULOS PENDIENTES ARRAIJAN", []))
    data_view["vehiculos_pendientes_arraijan"] = data.get("VEHICULOS PENDIENTES ARRAIJAN", [])
    # Otros Estados
    data_view["cant_traspasados"] = len(data.get("» CARROS TRASPASADOS", []))
    data_view["traspasados"] = data.get("» CARROS TRASPASADOS", [])
    data_view["cant_fin_contrato"] = len(data.get("» CULMINACION DE CONTRATO", []))
    data_view["fin_contrato"] = data.get("» CULMINACION DE CONTRATO", [])
    data_view["cant_en_tramite"] = len(data.get("» EN TRAMITE", []))
    data_view["en_tramite"] = data.get("» EN TRAMITE", [])
    data_view["cant_fuera_circulacion"] = len(data.get("» Fuera de Circulacion", []))
    data_view["fuera_circulacion"] = data.get("» Fuera de Circulacion", [])
    data_view["cant_inactivos"] = len(data.get("» INACTIVOS", []))
    data_view["inactivos"] = data.get("» INACTIVOS", [])
    data_view["cant_perdida_total"] = len(data.get("» PERDIDA TOTAL", []))
    data_view["perdida_total"] = data.get("» PERDIDA TOTAL", [])
    data_view["cant_retirado_empresa"] = len(data.get("» RETIRADO DE LA EMPRESA", []))
    data_view["retirado_empresa"] = data.get("» RETIRADO DE LA EMPRESA", [])
    data_view["cant_sin_calificar"] = len(data.get("» SIN CLASIFICAR", []))
    data_view["sin_calificar"] = data.get("» SIN CLASIFICAR", [])
    data_view["cant_vendidos"] = len(data.get("» VENDIDO", []))
    data_view["vendidos"] = data.get("» VENDIDO", [])
    data_view["cant_para_venta"] = len(data.get("» Vehiculos Para la Venta", []))
    data_view["para_venta"] = data.get("» Vehiculos Para la Venta", [])
    # Totales

    data_view["total_activos"] = len(data.get("ACTIVO", [])) + len(data.get("BACUPK", [])) + len(data.get("CHAPISTERIA PARADO", [])) + len(data.get("CHAPISTERIA TRABAJANDO", [])) + len(data.get("CUSTODIA", [])) + len(data.get("DETENIDO", [])) + len(data.get("ESPERANDO OPERADOR", [])) + len(data.get("MECANICA MANTENIMIENTO", [])) + len(data.get("MECANICA PARADOS", [])) + len(data.get("OTROS", [])) + len(data.get("VEHICULOS PENDIENTES ARRAIJAN", []))

    data_view["total_parados"] = len(data.get("» CARROS TRASPASADOS", [])) + len(data.get("» CULMINACION DE CONTRATO", [])) + len(data.get("» EN TRAMITE", [])) + len(data.get("» Fuera de Circulacion", [])) + len(data.get("» INACTIVOS", [])) + len(data.get("» PERDIDA TOTAL", [])) + len(data.get("» RETIRADO DE LA EMPRESA", [])) + len(data.get("» SIN CLASIFICAR", [])) + len(data.get("» VENDIDO", [])) + len(data.get("» Vehiculos Para la Venta", []))

    data_view["total_vehiculos"] = data_view["total_activos"] + data_view["total_parados"]

    if data_view["total_activos"] == 0:
            data_view["promedio_activos"] = 0
    else:
        data_view["promedio_activos"] = round((data_view["cant_activo_backup"] / data_view["total_activos"] * 100), 2)
    data_view["promedio_parados"] = round((100 - data_view["promedio_activos"]), 2)

    titulo = 'Informe Por Estados Detallado'
    usuario = 'Usuario de Prueba'

    data_view["usuario"] = usuario

    headers = {
        "Content-Disposition": "inline; informe-estados-detallado-empresa.pdf"
    }  

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "form2.html"
    header_file = "header1.html"
    footer_file = "footer1.html"
    template = template_env.get_template(template_file)
    header = template_env.get_template(header_file)
    footer = template_env.get_template(footer_file)
    output_text = template.render(data_view) 
    output_header = header.render(data_view)
    output_footer = footer.render(data_view)

    html_path = f'./templates/renderform2.html'
    header_path = f'./templates/renderheader1.html'
    footer_path = f'./templates/renderfooter1.html'
    html_file = open(html_path, 'w')
    header_file = open(header_path, 'w')
    html_footer = open(footer_path, 'w')
    html_file.write(output_text)
    header_file.write(output_header)
    html_footer.write(output_footer)
    html_file.close()
    header_file.close()
    html_footer.close()
    pdf_path = 'informe-estados-detallado-empresa.pdf'
    html2pdf(titulo,html_path, pdf_path, header_path=header_path, footer_path=footer_path)

    response =  FileResponse(pdf_path, media_type='application/pdf', filename='templates/informe-estados-detallado-empresa.pdf', headers=headers)

    return response
    #return JSONResponse(content=jsonable_encoder(data))
  finally:
    db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/relacion-vehiculos-propietario')
async def get_vehiculos_detalles():
    db = session()
    try:
        vehiculos_detalles = db.query(
            Propietarios.CODIGO.label('propietario_codigo'),
            Propietarios.NOMBRE.label('propietario_nombre'),
            Estados.CODIGO.label('estado_codigo'),
            Estados.NOMBRE.label('estado_nombre'),
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.NOMMARCA.label('vehiculo_marca'),
            Vehiculos.MODELO.label('vehiculo_modelo'),
            Vehiculos.LINEA.label('vehiculo_linea'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.MOTORNRO.label('vehiculo_motor'),
            Vehiculos.CHASISNRO.label('vehiculo_chasis'),
            Conductores.NROENTREGA.label('conductor_nro_entrega'),
            Conductores.CUO_DIARIA.label('conductor_cuo_diaria'),
            Conductores.NROENTSDO.label('conductor_nro_ent_sdo'),
            Conductores.CODIGO.label('conductor_codigo'),
            Conductores.NOMBRE.label('conductor_nombre'),
            Conductores.CEDULA.label('conductor_cedula'),
            Conductores.TELEFONO.label('conductor_telefono')
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
                'estado_codigo': resultado.estado_codigo,
                'estado_nombre': resultado.estado_nombre,
                'vehiculo_numero': resultado.vehiculo_numero,
                'vehiculo_placa': resultado.vehiculo_placa,
                'vehiculo_marca': resultado.vehiculo_marca,
                'vehiculo_modelo': resultado.vehiculo_modelo,
                'vehiculo_linea': resultado.vehiculo_linea,
                'vehiculo_nro_cupo': resultado.vehiculo_nro_cupo,
                'vehiculo_motor': resultado.vehiculo_motor,
                'vehiculo_chasis': resultado.vehiculo_chasis,
                'conductor_nro_entrega': resultado.conductor_nro_entrega,
                'conductor_cuo_diaria': resultado.conductor_cuo_diaria,
                'conductor_nro_ent_sdo': resultado.conductor_nro_ent_sdo,
                'conductor_codigo': resultado.conductor_codigo,
                'conductor_nombre': resultado.conductor_nombre,
                'conductor_cedula': resultado.conductor_cedula,
                'conductor_telefono': resultado.conductor_telefono
            }
            vehiculos_detalles_list.append(vehiculo_detalle)

        codigos_estados_deseados = []

        data = obtener_conductores_por_propietario(vehiculos_detalles_list, codigos_estados_deseados)

        claves_deseadas = ["1", "13", "17", "26", "36"]

        datos = {clave: data.get(clave, {}) for clave in claves_deseadas}

        # Datos de la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        usuario = "admin" 
        titulo = 'Relación Vehículos por Propietario'

        data_view = {
            "fecha": fecha,
            "hora": hora_actual
        }

        # Iterar sobre las empresas y vehículos
        total = 0
        for empresa, info in datos.items():
            if isinstance(info, dict):
                # Agregar información de la empresa
                data_view[empresa] = {
                    "codigo_empresa": info.get("propietario_codigo", 0),
                    "nombre_empresa": info.get("propietario_nombre", 0),
                    "empty": info.get("empty", 0),
                    "estados": {}  # Aquí almacenaremos los vehículos organizados por estado
                }
                for estado, estado_info in info.get("estados", {}).items():
                    if isinstance(estado_info, dict):
                        data_view[empresa]["estados"][estado] = []  # Lista para almacenar vehículos por estado
                        consecutivo = 1
                        for vehiculo, vehiculo_info in estado_info.items():
                            if isinstance(vehiculo_info, dict):
                                # Agregar información del vehículo
                                data_view[empresa]["estados"][estado].append({
                                    "consecutivo": consecutivo,
                                    "unidad": vehiculo_info.get("vehiculo_numero", 0),
                                    "placa": vehiculo_info.get("vehiculo_placa", 0),
                                    "marca": vehiculo_info.get("vehiculo_marca", 0),
                                    "modelo": vehiculo_info.get("vehiculo_modelo", 0),
                                    "linea": vehiculo_info.get("vehiculo_linea", 0),
                                    "nro_cupo": vehiculo_info.get("vehiculo_nro_cupo", 0),
                                    "motor": vehiculo_info.get("vehiculo_motor", 0),
                                    "chasis": vehiculo_info.get("vehiculo_chasis", 0),
                                    "nro_entrega": vehiculo_info.get("conductor_nro_entrega", 0),
                                    "cuota_diaria": vehiculo_info.get("conductor_cuo_diaria", 0),
                                    "nro_ent_sdo": vehiculo_info.get("conductor_nro_ent_sdo", 0),
                                    "codigo_conductor": vehiculo_info.get("conductor_codigo", 0),
                                    "nombre": vehiculo_info.get("conductor_nombre", 0),
                                    "cedula": vehiculo_info.get("conductor_cedula", 0),
                                    "telefono": vehiculo_info.get("conductor_telefono", 0),
                                })
                                consecutivo += 1
                                total += 1
                                
        data_view["total"] = total
        data_view["usuario"] = usuario

        headers = {
            "Content-Disposition": "inline; relacion-vehiculos-propietario.pdf"
        }  

        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "RelacionVehiculos.html"
        header_file = "header.html"
        footer_file = "footer.html"
        template = template_env.get_template(template_file)
        header = template_env.get_template(header_file)
        footer = template_env.get_template(footer_file)
        output_text = template.render(data_view=data_view)
        output_header = header.render(data_view=data_view)
        output_footer = footer.render(data_view=data_view)

        html_path = f'./templates/renderRelacionVehiculos.html'
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
        pdf_path = 'relacion-vehiculos-propietario.pdf'
        html2pdf(titulo, html_path, pdf_path, header_path=header_path, footer_path=footer_path)

        response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/relacion-vehiculos-propietario.pdf', headers=headers) 
        
        return response
    
        #return JSONResponse(content=jsonable_encoder(datos))
    finally:
        db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/conductores-detalles-propietario')
async def get_vehiculos_detalles():
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

        codigos_estados_deseados = []
    
        data = cuotas_pagas(vehiculos_detalles_list, codigos_estados_deseados)

        claves_deseadas = ["1", "13", "17", "26", "36"]

        # Crear un nuevo diccionario con los datos de las claves deseadas
        datos = {clave: data.get(clave, {}) for clave in claves_deseadas}

        # Datos de la fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        usuario = "admin" 
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

@reports_router.get('/directorio-propietarios')
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
            "Content-Disposition": "inline; informe-cuotas-pagas.pdf"
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
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
fecha_hora_actual = datetime.now()
fecha_actual = fecha_hora_actual.date()
fecha = fecha_actual.strftime("%d/%m/%Y")
hora = fecha_hora_actual.time()  
hora_actual = hora.strftime("%H:%M")

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
    data_view = {"fecha": fecha, "hora": hora_actual, "empresa": "WORLD TAXI ADMINISTRACION, S.A."}
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

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "form1.html"
    template = template_env.get_template(template_file)
    output_text = template.render(data_view) 

    html_path = f'./templates/output.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()
    pdf_path = 'estado-vehiculos-resumen.pdf'
    html2pdf(html_path, pdf_path)

    response =  FileResponse(pdf_path, media_type='application/pdf', filename='templates/estado-vehiculos-resumen.pdf', headers=headers)
    #response = JSONResponse(content=jsonable_encoder(data))

    return response
  finally:
    db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/estado-vehiculos-resumen-empresa', response_class=FileResponse)
async def get_conteo_propietarios_vehiculos_estados():
  db = session()
  try:
    conteo_propietarios_vehiculos_estados = db.query(Propietarios.CODIGO.label('propietario_codigo'), Propietarios.ABREVIADO.label('propietario_abreviado'), Estados.CODIGO.label('estado_codigo'),Estados.NOMBRE.label('estado_nombre'), Vehiculos.NUMERO.label('vehiculo_numero') )\
    .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
    .join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO) \
    .all()
    vehiculos_estados_propietarios_list = [] 
    for resultado in conteo_propietarios_vehiculos_estados:
      propietarios_vehiculos_estados = {
        'propietario_codigo': resultado.propietario_codigo,
        'propietario_abreviado': resultado.propietario_abreviado,
        'estado_codigo': resultado.estado_codigo,
        'estado_nombre': resultado.estado_nombre,
        'vehiculo_numero': resultado.vehiculo_numero
      }
      vehiculos_estados_propietarios_list.append(propietarios_vehiculos_estados)
    data = obtener_conteo_por_propietario(vehiculos_estados_propietarios_list)
    data = data.get("conteo_por_empresa")
    data = data.get("26") 
    data_view = {"fecha": fecha, "hora": hora_actual}
    data_view["empresa"] = data.get("nombre_empresa", 0)
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
        "Content-Disposition": "inline; estado-vehiculos-resumen-empresa.pdf"
    }  

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "form1.html"
    template = template_env.get_template(template_file)
    output_text = template.render(data_view) 

    html_path = f'./templates/output.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()
    pdf_path = 'estado-vehiculos-resumen-empresa.pdf'
    html2pdf(html_path, pdf_path)

    response =  FileResponse(pdf_path, media_type='application/pdf', filename='templates/estado-vehiculos-resumen-empresa.pdf', headers=headers)

    return response
  finally:
    db.close()

#-----------------------------------------------------------------------------------------


@reports_router.get('/conteo-vehiculos-estados-numeros', response_class=FileResponse)
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
    data_view = {"fecha": fecha, "hora": hora_actual, "empresa": "WORLD TAXI ADMINISTRACION, S.A."}
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
    """ data_view["cant_vehiculos_pendientes_arraijan"] = len(data.get("VEHICULOS PENDIENTES ARRAIJAN", []))
    data_view["vehiculos_pendientes_arraijan"] = data.get("VEHICULOS PENDIENTES ARRAIJAN", []) """
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

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "form2.html"
    template = template_env.get_template(template_file)
    output_text = template.render(data_view) 

    html_path = f'./templates/output2.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()
    pdf_path = 'estado-vehiculos-numeros.pdf'
    html2pdf(html_path, pdf_path)

    response =  FileResponse(pdf_path, media_type='application/pdf', filename='templates/estado-vehiculos-numeros.pdf', headers=headers)

    return response
    #return JSONResponse(content=jsonable_encoder(data))
  finally:
    db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/conteo-propietarios-vehiculos-estados-numeros')
async def get_conteo_propietarios_vehiculos_estados_numeros():
  db = session()
  try:
    conteo_propietarios_vehiculos_estados = db.query(
        Propietarios.CODIGO.label('propietario_codigo'),
        Propietarios.ABREVIADO.label('propietario_abreviado'),
        Estados.CODIGO.label('estado_codigo'),
        Estados.NOMBRE.label('estado_nombre'),
        Vehiculos.NUMERO.label('vehiculo_numero')
    ).join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO).join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO).all()

    vehiculos_estados_propietarios_list = []
    for resultado in conteo_propietarios_vehiculos_estados:
        propietarios_vehiculos_estados = {
            'propietario_codigo': resultado.propietario_codigo,
            'propietario_abreviado': resultado.propietario_abreviado,
            'estado_codigo': resultado.estado_codigo,
            'estado_nombre': resultado.estado_nombre,
            'vehiculo_numero': resultado.vehiculo_numero
        }
        vehiculos_estados_propietarios_list.append(propietarios_vehiculos_estados)
    result = obtener_numeros_por_propietario(vehiculos_estados_propietarios_list)
    return JSONResponse(content=jsonable_encoder(result))
  finally:
    db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/vehiculos-detalles')
async def get_vehiculos_detalles():
    db = session()
    try:
        vehiculos_detalles = db.query(
            Propietarios.CODIGO.label('propietario_codigo'),
            Propietarios.ABREVIADO.label('propietario_abreviado'),
            Estados.CODIGO.label('estado_codigo'),
            Estados.NOMBRE.label('estado_nombre'),
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.NOMMARCA.label('vehiculo_marca'),
            Vehiculos.MODELO.label('vehiculo_modelo'),
            Vehiculos.LINEA.label('vehiculo_linea'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
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
            .filter(Estados.CODIGO == '01') \
            .all()
        
        # Convertir los resultados en un formato JSON
        vehiculos_detalles_list = []
        for resultado in vehiculos_detalles:
            vehiculo_detalle = {
                'propietario_codigo': resultado.propietario_codigo,
                'propietario_abreviado': resultado.propietario_abreviado,
                'estado_codigo': resultado.estado_codigo,
                'estado_nombre': resultado.estado_nombre,
                'vehiculo_numero': resultado.vehiculo_numero,
                'vehiculo_placa': resultado.vehiculo_placa,
                'vehiculo_marca': resultado.vehiculo_marca,
                'vehiculo_modelo': resultado.vehiculo_modelo,
                'vehiculo_linea': resultado.vehiculo_linea,
                'vehiculo_nro_cupo': resultado.vehiculo_nro_cupo,
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
        
        return JSONResponse(content=jsonable_encoder(vehiculos_detalles_list))
    finally:
        db.close()
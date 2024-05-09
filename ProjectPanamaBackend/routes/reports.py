from fastapi import APIRouter, Request
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
from fastapi.responses import HTMLResponse

templateJinja = Jinja2Templates(directory="templates")

reports_router = APIRouter()

@reports_router.get('/conteo-vehiculos-estados', response_class=HTMLResponse)
async def get_conteo_vehiculos_estados(request: Request):
  db = session()
  try:
    conteo_vehiculos_estados = db.query(Estados.CODIGO, Estados.NOMBRE, Vehiculos.PLACA) \
    .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
    .all()
    vehiculos_estados_list = [{'codigo': vehiculo.CODIGO, 'nombre': vehiculo.NOMBRE, 'placa': vehiculo.PLACA} for vehiculo in conteo_vehiculos_estados]
    data = fun_conteo_vehiculos_estados(vehiculos_estados_list)
    data = data.get("conteo_placas")
    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.date()
    hora = fecha_hora_actual.time()  
    hora_actual = hora.strftime("%H:%M")
    data_view = {"fecha": fecha_actual, "hora": hora_actual, "empresa": "WORLD TAXI ADMINISTRACION, S.A."}
    # Activos
    data_view["cant_activo"] = data.get("ACTIVO", 0)
    data_view["cant_backup"] = data.get("BACUPK", 0)
    data_view["cant_activo_backup"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0)
    data_view["cant_chap_parado"] = data.get("CHAPISTERIA PARADO", 0)
    data_view["cant_chap_trabajando"] = data.get("CHAPISTERIA TRABAJANDO", 0)
    data_view["cant_custodia"] = data.get("» CARROS TRASPASADOS", 0)
    data_view["cant_esp_operador"] = data.get("ESPERANDO OPERADOR", 0)
    data_view["cant_mecanica_parado"] = data.get("MECANICA PARADOS", 0)
    data_view["cant_otros"] = data.get("» SIN CLASIFICAR", 0)
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
    data_view["total_vehiculos"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0) + data.get("CHAPISTERIA PARADO", 0) + data.get("CHAPISTERIA TRABAJANDO", 0) + data.get("» CARROS TRASPASADOS", 0) + data.get("ESPERANDO OPERADOR", 0) + data.get("MECANICA PARADOS", 0) + data.get("» SIN CLASIFICAR", 0) + data.get("» CARROS TRASPASADOS", 0) + data.get("» CULMINACION DE CONTRATO", 0) + data.get("» EN TRAMITE", 0) + data.get("» Fuera de Circulacion", 0) + data.get("» INACTIVOS", 0) + data.get("» PERDIDA TOTAL", 0) + data.get("» RETIRADO DE LA EMPRESA", 0) + data.get("» SIN CLASIFICAR", 0) + data.get("» VENDIDO", 0) + data.get("» Vehiculos Para la Venta", 0)

    data_view["total_activos"] = data.get("ACTIVO", 0) + data.get("BACUPK", 0) + data.get("CHAPISTERIA PARADO", 0) + data.get("CHAPISTERIA TRABAJANDO", 0) + data.get("» CARROS TRASPASADOS", 0) + data.get("ESPERANDO OPERADOR", 0) + data.get("MECANICA PARADOS", 0) + data.get("» SIN CLASIFICAR", 0)

    data_view["total_parados"] = data.get("» CARROS TRASPASADOS", 0) + data.get("» CULMINACION DE CONTRATO", 0) + data.get("» EN TRAMITE", 0) + data.get("» Fuera de Circulacion", 0) + data.get("» INACTIVOS", 0) + data.get("» PERDIDA TOTAL", 0) + data.get("» RETIRADO DE LA EMPRESA", 0) + data.get("» SIN CLASIFICAR", 0) + data.get("» VENDIDO", 0) + data.get("» Vehiculos Para la Venta", 0)

    data_view["promedio_activos"] = round((data_view["total_activos"] / data_view["total_vehiculos"] * 100), 2)

    data_view["promedio_parados"] = round((data_view["total_parados"] / data_view["total_vehiculos"] * 100), 2)

    return templateJinja.TemplateResponse("form1.html", {"request": request, "data_vehiculos": data_view})
  finally:
    db.close()

#-----------------------------------------------------------------------------------------

@reports_router.get('/conteo-propietarios-vehiculos-estados')
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
    result = obtener_conteo_por_propietario(vehiculos_estados_propietarios_list) 
    return JSONResponse(content=jsonable_encoder(result))
  finally:
    db.close()

@reports_router.get('/conteo-propietarios-vehiculos-estados-numeros')
async def get_conteo_propietarios_vehiculos_estados_numeros():
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
    result = obtener_numeros_por_propietario(vehiculos_estados_propietarios_list)
    return JSONResponse(content=jsonable_encoder(result))
  finally:
    db.close()

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
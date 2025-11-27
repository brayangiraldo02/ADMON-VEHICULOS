from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.vehiculos import Vehiculos
from models.estados import Estados
from models.conductores import Conductores
from schemas.vehicles import VehicleUpdate, VehicleCreate
from models.centrales import Centrales
from models.cajarecaudos import CajaRecaudos
from models.propietarios import Propietarios
from models.cajarecaudoscontado import CajasRecaudosContado
from models.cartera import Cartera
from models.movienca import Movienca
from utils.reports import *
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

vehicles_router = APIRouter()

@vehicles_router.get("/vehicles/{company_code}/", tags=["Vehicles"])
async def get_vehicles(company_code: str):
  db = session()
  try:
    vehicles = db.query(Vehiculos.NUMERO, Vehiculos.PLACA, Vehiculos.PROPI_IDEN, Vehiculos.NRO_CUPO).filter(Vehiculos.EMPRESA == company_code).all()
    owners = db.query(Propietarios.CODIGO, Propietarios.NOMBRE).filter(Propietarios.EMPRESA == company_code).all()
    owners_dict = {owner.CODIGO: owner.NOMBRE for owner in owners}

    vehicles_list = [
      {
        'unidad': vehicle.NUMERO,
        'placa': vehicle.PLACA,
        'propietario': owners_dict.get(vehicle.PROPI_IDEN, "") + ' (' + vehicle.PROPI_IDEN + ')',
        'nro_cupo': vehicle.NRO_CUPO
      }
      for vehicle in vehicles
    ]
    return JSONResponse(content=jsonable_encoder(vehicles_list))
  except Exception as e:
    return JSONResponse(content={"message": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/vehicles/all/{company_code}/", tags=["Vehicles"])
async def get_vehicles(company_code: str):
  db = session()
  try:
    vehicles = db.query(
        Vehiculos.NUMERO.label('vehiculo_numero'),
        Vehiculos.CONSECUTIV.label('vehiculo_consecutivo'),
        Vehiculos.PLACA.label('vehiculo_placa'),
        Vehiculos.MODELO.label('vehiculo_modelo'),
        Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
        Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
        Vehiculos.MOTORNRO.label('vehiculo_motor'),
        Vehiculos.CHASISNRO.label('vehiculo_chasis'),
        Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
        Vehiculos.PROPI_IDEN.label('vehiculo_propietario_codigo'),
        Vehiculos.CENTRAL.label('vehiculo_central_codigo'),
        Vehiculos.NRO_LLAVES.label('vehiculo_nro_llaves'),
        Vehiculos.ESTADO.label('vehiculo_estado_codigo'),
        Vehiculos.CONDUCTOR.label('vehiculo_conductor_codigo'),
        Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
        Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
        Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
        Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
        Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
    ).filter(Vehiculos.EMPRESA == company_code,
        Vehiculos.PLACA != '',
        Vehiculos.PLACA.isnot(None)) \
    .all()

    conductores = db.query(
        Conductores.CODIGO,
        Conductores.NOMBRE
    ).filter(Conductores.EMPRESA == company_code).all()

    conductores_dict = {conductor.CODIGO: conductor.NOMBRE for conductor in conductores}

    estados = db.query(
        Estados.CODIGO,
        Estados.NOMBRE,
        Estados.SUMAR
    ).filter(Estados.EMPRESA == company_code).all()

    estados_dict = {estado.CODIGO: {'nombre': estado.NOMBRE, 'sumar': estado.SUMAR} for estado in estados}

    centrales = db.query(
        Centrales.CODIGO,
        Centrales.NOMBRE
    ).filter(Centrales.EMPRESA == company_code).all()

    centrales_dict = {central.CODIGO: central.NOMBRE for central in centrales}

    propietarios = db.query(
        Propietarios.CODIGO,
        Propietarios.NOMBRE
    ).filter(Propietarios.EMPRESA == company_code).all()

    propietarios_dict = {prop.CODIGO: prop.NOMBRE for prop in propietarios}

    vehicles_list = [
      {
        'unidad': vehicle.vehiculo_numero,
        'consecutivo': vehicle.vehiculo_consecutivo,
        'placa': vehicle.vehiculo_placa,
        'modelo': vehicle.vehiculo_modelo,
        'nro_cupo': vehicle.vehiculo_nro_cupo,
        'permiso': vehicle.vehiculo_permiso_nro,
        'motor': vehicle.vehiculo_motor,
        'chasis': vehicle.vehiculo_chasis,
        'matricula': vehicle.vehiculo_fec_matricula,
        'empresa': propietarios_dict.get(vehicle.vehiculo_propietario_codigo, ''),
        'central': centrales_dict.get(vehicle.vehiculo_central_codigo, ''),
        'conductor': conductores_dict.get(vehicle.vehiculo_conductor_codigo, ''),
        'estado': estados_dict.get(vehicle.vehiculo_estado_codigo, {}).get('sumar', ''),
        'nombre_estado': estados_dict.get(vehicle.vehiculo_estado_codigo, {}).get('nombre', ''),
        'vlr_cta': vehicle.vehiculo_cuota_diaria,
        'nro_ctas': vehicle.vehiculo_nro_Ctas,
        'panapass': vehicle.vehiculo_panapass,
        'clave': vehicle.vehiculo_panapass_pwd,
        'saldo': vehicle.vehiculo_saldo_panapass,
        'nro_llaves': vehicle.vehiculo_nro_llaves
      }
      for vehicle in vehicles
    ]
    return JSONResponse(content=jsonable_encoder(vehicles_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get('/directorio-vehiculos/{company_code}/', tags=["Vehicles"]) 
async def get_vehiculos_detalles(company_code: str):
    db = session()
    try:
        vehiculos_detalles = db.query(
            Estados.NOMBRE.label('vehiculo_estado_nombre'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.NUMERO.label('vehiculo_unidad'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
            Vehiculos.NOMMARCA.label('vehiculo_marca'),
            Vehiculos.LINEA.label('vehiculo_linea'),
            Vehiculos.MODELO.label('vehiculo_año'),
            Vehiculos.MOTORNRO.label('vehiculo_motor'),
            Vehiculos.CHASISNRO.label('vehiculo_chasis'),
            Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
            Vehiculos.PROPI_IDEN.label('vehiculo_empresa_codigo'),
            Centrales.NOMBRE.label('vehiculo_central'),
        )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Centrales, Centrales.CODIGO == Vehiculos.CENTRAL) \
            .filter(Vehiculos.EMPRESA == company_code) \
            .all()
        
        propietarios = db.query(
            Propietarios.CODIGO,
            Propietarios.NOMBRE
        ).filter(Propietarios.EMPRESA == company_code).all()

        propietarios_dict = {prop.CODIGO: prop.NOMBRE for prop in propietarios}
        
        vehiculos_detalles_list = []  
        for resultado in vehiculos_detalles:
            vehiculo_detalle = {
                'vehiculo_estado_nombre': resultado.vehiculo_estado_nombre,
                'vehiculo_placa': resultado.vehiculo_placa,
                'vehiculo_unidad': resultado.vehiculo_unidad,
                'vehiculo_nro_cupo': resultado.vehiculo_nro_cupo,
                'vehiculo_permiso_nro': resultado.vehiculo_permiso_nro,
                'vehiculo_marca': resultado.vehiculo_marca,
                'vehiculo_linea': resultado.vehiculo_linea,
                'vehiculo_año': resultado.vehiculo_año,
                'vehiculo_motor': resultado.vehiculo_motor,
                'vehiculo_chasis': resultado.vehiculo_chasis,
                'vehiculo_fec_matricula': resultado.vehiculo_fec_matricula,
                'vehiculo_empresa': propietarios_dict.get(resultado.vehiculo_empresa_codigo, 'Sin propietario'),
                'vehiculo_central': resultado.vehiculo_central,
            }
            vehiculos_detalles_list.append(vehiculo_detalle)

            data = agrupar_vehiculos_por_estado(vehiculos_detalles_list)
            
            # Datos de la fecha y hora actual
            # Define la zona horaria de Ciudad de Panamá
            panama_timezone = pytz.timezone('America/Panama')
            # Obtén la hora actual en la zona horaria de Ciudad de Panamá
            now_in_panama = datetime.now(panama_timezone)
            # Formatea la fecha y la hora según lo requerido
            fecha = now_in_panama.strftime("%d/%m/%Y")
            hora_actual = now_in_panama.strftime("%I:%M:%S %p")
            usuario = "admin"
            titulo = 'Directorio Vehiculos'

            def formatear_fecha(fecha_hora_str):
              # Verificar si la fecha es una cadena
              if isinstance(fecha_hora_str, str) and len(fecha_hora_str) >= 10:
                  # Tomar solo los primeros 10 caracteres que corresponden a la fecha
                  return fecha_hora_str[:10]
              else:
                  # En otros casos, devolver la cadena tal cual
                  return fecha_hora_str

            # Inicializar el diccionario data_view con información común
            data_view = {
                "fecha": fecha,
                "hora": hora_actual
            }

            for estado, info in data.items():
              if estado:  # Asegurarse de ignorar el estado vacío (estado "")
                  # Inicializar el diccionario para este estado
                  data_view[estado] = {
                      "nombre_estado": estado,
                      "vehiculos": []
                  }
                  for vehiculo_placa, vehiculo_info in info.items():
                      if isinstance(vehiculo_info, dict):
                          # Crear el diccionario del vehículo con la información relevante
                          vehiculo = {  
                              "unidad": vehiculo_info.get("vehiculo_unidad", ""),
                              "placa": vehiculo_info.get("vehiculo_placa", ""),
                              "nro_cupo": vehiculo_info.get("vehiculo_nro_cupo", ""),
                              "permiso": vehiculo_info.get("vehiculo_permiso_nro", ""),
                              "marca": vehiculo_info.get("vehiculo_marca", ""),
                              "linea": vehiculo_info.get("vehiculo_linea", ""),
                              "año": vehiculo_info.get("vehiculo_año", ""),
                              "motor": vehiculo_info.get("vehiculo_motor", ""),
                              "chasis": vehiculo_info.get("vehiculo_chasis", ""),
                              "fec_matricula": formatear_fecha(vehiculo_info.get("vehiculo_fec_matricula", "")),
                              "empresa": vehiculo_info.get("vehiculo_empresa", ""),
                              "central": vehiculo_info.get("vehiculo_central", ""),
                          }
                          # Agregar el vehículo a la lista de vehículos del estado
                          data_view[estado]["vehiculos"].append(vehiculo)

            data_view["usuario"] = usuario

            headers = {
              "Content-Disposition": "attachment; detalles-vehiculos.pdf"
            }  

            template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "DirectorioVehiculos.html"
        header_file = "header.html"
        footer_file = "footer.html"
        template = template_env.get_template(template_file)
        header = template_env.get_template(header_file)
        footer = template_env.get_template(footer_file)
        output_text = template.render(data_view=data_view)
        output_header = header.render(data_view=data_view)
        output_footer = footer.render(data_view=data_view)

        html_path = f'./templates/renderDirectorioVehiculos.html'
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
        pdf_path = 'Vehiculos-detalles.pdf'
        html2pdf(titulo, html_path, pdf_path, header_path=header_path, footer_path=footer_path)

        response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/Vehoculos-detalles.pdf', headers=headers)
        
        return response

        """ return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}) """
    finally:
        db.close()

#-------------------------------------------------------------------------------------------

# @vehicles_router.get("/vehicles/{vehicle_id}", tags=["Vehicles"])
# async def get_vehicle(vehicle_id: str):
#   db = session()
#   try:
#     vehicle = db.query(
#             Vehiculos.NUMERO.label('vehiculo_numero'),
#             Vehiculos.PLACA.label('vehiculo_placa'),
#             Vehiculos.MODELO.label('vehiculo_modelo'),
#             Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
#             Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
#             Vehiculos.MOTORNRO.label('vehiculo_motor'),
#             Vehiculos.CHASISNRO.label('vehiculo_chasis'),
#             Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
#             Vehiculos.EMPRESA.label('vehiculo_empresa'),
#             Conductores.NOMBRE.label('vehiculo_conductor'),
#             Estados.NOMBRE.label('vehiculo_estado'),
#             Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
#             Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
#             Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
#             Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
#             Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
#         )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
#             .join(Conductores, Conductores.CODIGO == Vehiculos.CONDUCTOR) \
#             .filter(Vehiculos.PLACA == vehicle_id) \
#             .first()

#     vehicle_info = {
#       'unidad': vehicle.vehiculo_numero,
#       'placa': vehicle.vehiculo_placa,
#       'modelo': vehicle.vehiculo_modelo,
#       'nro_cupo': vehicle.vehiculo_nro_cupo,
#       'permiso': vehicle.vehiculo_permiso_nro,
#       'motor': vehicle.vehiculo_motor,
#       'chasis': vehicle.vehiculo_chasis,
#       'matricula': vehicle.vehiculo_fec_matricula,
#       'empresa': vehicle.vehiculo_empresa,
#       'conductor': vehicle.vehiculo_conductor,
#       'estado': vehicle.vehiculo_estado,
#       'vlr_cta': vehicle.vehiculo_cuota_diaria,
#       'nro_ctas': vehicle.vehiculo_nro_Ctas,
#       'panapass': vehicle.vehiculo_panapass,
#       'clave': vehicle.vehiculo_panapass_pwd,
#       'saldo': vehicle.vehiculo_saldo_panapass
#     }
    
#     return JSONResponse(content=jsonable_encoder(vehicle_info))
#   except Exception as e:    
#     return JSONResponse(content={"error": str(e)})
#   finally:
#     db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/vehicle/{vehicle_id}/", tags=["Vehicles"])
async def get_vehicle_details(vehicle_id: str):
  db = session()
  try:
      vehicle = db.query(
          Vehiculos.NUMERO.label('vehiculo_numero'),
          Vehiculos.PLACA.label('vehiculo_placa'),
          Vehiculos.CONSECUTIV.label('vehiculo_consecutivo'),
          Vehiculos.MARCA.label('vehiculo_marca'),
          Vehiculos.LINEA.label('vehiculo_modelo'),
          Vehiculos.MODELO.label('vehiculo_fec_modelo'),
          Vehiculos.CILINDRAJE.label('vehiculo_cilindraje'),
          Vehiculos.PUERTAS.label('vehiculo_nro_puertas'),
          Vehiculos.LICETRANSI.label('vehiculo_licencia_nro'),
          Vehiculos.FEC_EXPEDI.label('vehiculo_licencia_fec'),
          Vehiculos.COLORES.label('vehiculo_color'),
          Vehiculos.SERVICIO.label('vehiculo_servicio'),
          Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
          Vehiculos.FEC_VENCIM.label('vehiculo_fec_vencimiento_matricula'),
          Vehiculos.FEC_IMPORT.label('vehiculo_fec_importacion'),
          Vehiculos.CLASEVEHIC.label('vehiculo_clase'),
          Vehiculos.TIPOCARROC.label('vehiculo_tipo'),
          Vehiculos.COMBUSTIBL.label('vehiculo_combustible'),
          Vehiculos.CAPACIDAD.label('vehiculo_capacidad'),
          Vehiculos.NE.label('vehiculo_ne'),
          Vehiculos.MOTORNRO.label('vehiculo_motor'),
          Vehiculos.MOTORREG.label('vehiculo_motor_reg'),
          Vehiculos.MOTORVIN.label('vehiculo_vin'),
          Vehiculos.SERIENRO.label('vehiculo_serie'),
          Vehiculos.SERIEREG.label('vehiculo_serie_reg'),
          Vehiculos.CHASISNRO.label('vehiculo_chasis'),
          Vehiculos.CHASISREG.label('vehiculo_chasis_reg'),
          Vehiculos.PROPI_IDEN.label('vehiculo_propietario'),
          Vehiculos.CTA_GASTO.label('vehiculo_cta_gasto'),
          Vehiculos.CENTRAL.label('vehiculo_central'),
          Vehiculos.FEC_CREADO.label('vehiculo_fec_creacion'),
          Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
          Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
          Vehiculos.PERMISOVCE.label('vehiculo_fec_vencimiento_permiso'),
          Vehiculos.BLINDAJE.label('vehiculo_blindaje'),
          Vehiculos.POTENCIAHP.label('vehiculo_potencia'),
          Vehiculos.DECLA_IMPO.label('vehiculo_dec_importacion'),
          Vehiculos.RESTR_MOBI.label('vehiculo_restriccion_movilidad'),
          Vehiculos.LIMI_PROPI.label('vehiculo_limit_propiedad'),
          Vehiculos.ORG_TRANSI.label('vehiculo_organismo_transito'),
          Vehiculos.COD_BARRAS.label('vehiculo_codigo_barras'),
          Vehiculos.LATERAL.label('vehiculo_lateral'),
          Vehiculos.KILOMETRAJ.label('vehiculo_kilometraje'),
          Vehiculos.MODALIDAD.label('vehiculo_modalidad'),
          Vehiculos.INFO_PANAP.label('vehiculo_consulta_panapass'),
          Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
          Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
          Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
          Vehiculos.DOC_PLAPAR.label('vehiculo_placa_particular'),
          Vehiculos.FEC_PLAPAR.label('vehiculo_placa_particular_vence'),
          Vehiculos.DOC_PLAPUB.label('vehiculo_placa_publica'),
          Vehiculos.FEC_PLAPUB.label('vehiculo_placa_publica_vence'),
          Vehiculos.DOC_RESCIV.label('vehiculo_poliza_responsabilidad_civil'),
          Vehiculos.FEC_RESCIV.label('vehiculo_poliza_responsabilidad_civil_vence'),
          Vehiculos.DOC_EXTING.label('vehiculo_extinguidor'),
          Vehiculos.FEC_EXTING.label('vehiculo_extinguidor_vence'),
          Vehiculos.DOC_CEROPE.label('vehiculo_certificado_operacion'),
          Vehiculos.FEC_CEROPE.label('vehiculo_certificado_operacion_fec'),
          Vehiculos.NROENTREGA.label('vehiculo_nro_total_cuotas'),
          Vehiculos.CUO_DIARIA.label('vehiculo_vlr_cuo_diaria'),
          Vehiculos.CTA_RENTA.label('vehiculo_renta_diaria'),
          Vehiculos.CTA_SINIES.label('vehiculo_ahorro_siniestro'),
          Vehiculos.PAGA_ADMON.label('vehiculo_cobro_admon'),
          Vehiculos.CUO_ADMON.label('vehiculo_admon'),
          Vehiculos.CUO_REPVEH.label('vehiculo_reposicion'),
          Vehiculos.CUO_MANTEN.label('vehiculo_mantenimiento'),
          Vehiculos.CUO_RENDIM.label('vehiculo_rendimientos_propietario'),
          Vehiculos.PAGO_LUN.label('vehiculo_pago_lunes'),
          Vehiculos.PAGO_MAR.label('vehiculo_pago_martes'),
          Vehiculos.PAGO_MIE.label('vehiculo_pago_miercoles'),
          Vehiculos.PAGO_JUE.label('vehiculo_pago_jueves'),
          Vehiculos.PAGO_VIE.label('vehiculo_pago_viernes'),
          Vehiculos.PAGO_SAB.label('vehiculo_pago_sabado'),
          Vehiculos.PAGO_DOM.label('vehiculo_pago_domingo'),
          Vehiculos.FORMAPAGO.label('vehiculo_forma_pago'),
          Vehiculos.MULTA.label('vehiculo_multa_pago'),
          Vehiculos.FEC_1PAGO.label('vehiculo_fec_primer_pago'),
          Vehiculos.FEC_ULTPAG.label('vehiculo_fec_ultimo_pago'),
          Vehiculos.VLR_ULTPAG.label('vehiculo_vlr_ultimo_pago'),
          Vehiculos.REC_ULTPAG.label('vehiculo_recibo'),
          Vehiculos.FEC_1MANTE.label('vehiculo_primer_mantenimiento'),
          Vehiculos.FEC_ULTMAN.label('vehiculo_ultimo_mantenimiento'),
          Vehiculos.CATEGORIA.label('vehiculo_categoria'),
          Vehiculos.tipo_llave.label('vehiculo_tipo_llave'),
          Vehiculos.NRO_LLAVES.label('vehiculo_posicion_llave'),
          Vehiculos.FEC_ESTADO.label('vehiculo_fec_estado'),
          Vehiculos.GRUPODIARI.label('vehiculo_plan_pago'),
          Vehiculos.PREND_APAG.label('vehiculo_prendido_apagado'),
          Vehiculos.PIQUERA.label('vehiculo_piquera'),
          Vehiculos.FEC_PIQUER.label('vehiculo_fec_inicio_piquera'),
          Vehiculos.FAC_COMPRA.label('vehiculo_factura_compra'),
          Vehiculos.FEC_COMPRA.label('vehiculo_fec_factura_compra'),
          Vehiculos.VLR_COMPRA.label('vehiculo_valor_compra'),
          Vehiculos.POLIZA.label('vehiculo_num_poliza'),
          Vehiculos.FEC_POLIZA.label('vehiculo_fec_poliza'),
          Vehiculos.OBSERVA.label('vehiculo_observaciones'),
          Vehiculos.LUN.label('vehiculo_picoyplaca_lunes'),
          Vehiculos.MAR.label('vehiculo_picoyplaca_martes'),
          Vehiculos.MIE.label('vehiculo_picoyplaca_miercoles'),
          Vehiculos.JUE.label('vehiculo_picoyplaca_jueves'),
          Vehiculos.VIE.label('vehiculo_picoyplaca_viernes'),
          Vehiculos.SAB.label('vehiculo_picoyplaca_sabado'),
          Vehiculos.DOM.label('vehiculo_picoyplaca_domingo'),
      )   .filter(Vehiculos.CONSECUTIV == vehicle_id) \
          .first()
      
      vehicle_info = {
          'vehiculo_numero': vehicle.vehiculo_numero,
          'vehiculo_placa': vehicle.vehiculo_placa,
          'vehiculo_consecutivo': vehicle.vehiculo_consecutivo,
          'vehiculo_marca': vehicle.vehiculo_marca,
          'vehiculo_modelo': vehicle.vehiculo_modelo,
          'vehiculo_fec_modelo': vehicle.vehiculo_fec_modelo,
          'vehiculo_cilindraje': vehicle.vehiculo_cilindraje,
          'vehiculo_nro_puertas': vehicle.vehiculo_nro_puertas,
          'vehiculo_licencia_nro': vehicle.vehiculo_licencia_nro,
          'vehiculo_licencia_fec': vehicle.vehiculo_licencia_fec,
          'vehiculo_color': vehicle.vehiculo_color,
          'vehiculo_servicio': vehicle.vehiculo_servicio,
          'vehiculo_fec_matricula': vehicle.vehiculo_fec_matricula,
          'vehiculo_fec_vencimiento_matricula': vehicle.vehiculo_fec_vencimiento_matricula,
          'vehiculo_fec_importacion': vehicle.vehiculo_fec_importacion,
          'vehiculo_clase': vehicle.vehiculo_clase,
          'vehiculo_tipo': vehicle.vehiculo_tipo,
          'vehiculo_combustible': vehicle.vehiculo_combustible,
          'vehiculo_capacidad': vehicle.vehiculo_capacidad,
          'vehiculo_ne': vehicle.vehiculo_ne,
          'vehiculo_motor': vehicle.vehiculo_motor,
          'vehiculo_motor_reg': vehicle.vehiculo_motor_reg,
          'vehiculo_vin': vehicle.vehiculo_vin,
          'vehiculo_serie': vehicle.vehiculo_serie,
          'vehiculo_serie_reg': vehicle.vehiculo_serie_reg,
          'vehiculo_chasis': vehicle.vehiculo_chasis,
          'vehiculo_chasis_reg': vehicle.vehiculo_chasis_reg,
          'vehiculo_propietario': vehicle.vehiculo_propietario,
          'vehiculo_cta_gasto': vehicle.vehiculo_cta_gasto,
          'vehiculo_central': vehicle.vehiculo_central,
          'vehiculo_fec_creacion': vehicle.vehiculo_fec_creacion,
          'vehiculo_nro_cupo': vehicle.vehiculo_nro_cupo,
          'vehiculo_permiso_nro': vehicle.vehiculo_permiso_nro,
          'vehiculo_fec_vencimiento_permiso': vehicle.vehiculo_fec_vencimiento_permiso,
          'vehiculo_blindaje': vehicle.vehiculo_blindaje,
          'vehiculo_potencia': vehicle.vehiculo_potencia,
          'vehiculo_dec_importacion': vehicle.vehiculo_dec_importacion,
          'vehiculo_restriccion_movilidad': vehicle.vehiculo_restriccion_movilidad,
          'vehiculo_limit_propiedad': vehicle.vehiculo_limit_propiedad,
          'vehiculo_organismo_transito': vehicle.vehiculo_organismo_transito, 
          'vehiculo_codigo_barras': vehicle.vehiculo_codigo_barras,
          'vehiculo_lateral': vehicle.vehiculo_lateral,
          'vehiculo_kilometraje': vehicle.vehiculo_kilometraje,
          'vehiculo_modalidad': vehicle.vehiculo_modalidad,
          'vehiculo_consulta_panapass': vehicle.vehiculo_consulta_panapass,
          'vehiculo_panapass': vehicle.vehiculo_panapass, 
          'vehiculo_panapass_pwd': vehicle.vehiculo_panapass_pwd,
          'vehiculo_saldo_panapass': vehicle.vehiculo_saldo_panapass,
          'vehiculo_placa_particular': vehicle.vehiculo_placa_particular,
          'vehiculo_placa_particular_vence': vehicle.vehiculo_placa_particular_vence,
          'vehiculo_placa_publica': vehicle.vehiculo_placa_publica,
          'vehiculo_placa_publica_vence': vehicle.vehiculo_placa_publica_vence,
          'vehiculo_poliza_responsabilidad_civil': vehicle.vehiculo_poliza_responsabilidad_civil,
          'vehiculo_poliza_responsabilidad_civil_vence': vehicle.vehiculo_poliza_responsabilidad_civil_vence,
          'vehiculo_extinguidor': vehicle.vehiculo_extinguidor,
          'vehiculo_extinguidor_vence': vehicle.vehiculo_extinguidor_vence,
          'vehiculo_certificado_operacion': vehicle.vehiculo_certificado_operacion,
          'vehiculo_certificado_operacion_fec': vehicle.vehiculo_certificado_operacion_fec,
          'vehiculo_nro_total_cuotas': vehicle.vehiculo_nro_total_cuotas,
          'vehiculo_vlr_cuo_diaria': vehicle.vehiculo_vlr_cuo_diaria,
          'vehiculo_renta_diaria': vehicle.vehiculo_renta_diaria,
          'vehiculo_ahorro_siniestro': vehicle.vehiculo_ahorro_siniestro,
          'vehiculo_cobro_admon': vehicle.vehiculo_cobro_admon,
          'vehiculo_admon': vehicle.vehiculo_admon,
          'vehiculo_reposicion': vehicle.vehiculo_reposicion,
          'vehiculo_mantenimiento': vehicle.vehiculo_mantenimiento,
          'vehiculo_rendimientos_propietario': vehicle.vehiculo_rendimientos_propietario,
          'vehiculo_pago_lunes': vehicle.vehiculo_pago_lunes,
          'vehiculo_pago_martes': vehicle.vehiculo_pago_martes,
          'vehiculo_pago_miercoles': vehicle.vehiculo_pago_miercoles,
          'vehiculo_pago_jueves': vehicle.vehiculo_pago_jueves,
          'vehiculo_pago_viernes': vehicle.vehiculo_pago_viernes,
          'vehiculo_pago_sabado': vehicle.vehiculo_pago_sabado,
          'vehiculo_pago_domingo': vehicle.vehiculo_pago_domingo,
          'vehiculo_forma_pago': vehicle.vehiculo_forma_pago,
          'vehiculo_multa_pago': vehicle.vehiculo_multa_pago,
          'vehiculo_fec_primer_pago': vehicle.vehiculo_fec_primer_pago,
          'vehiculo_fec_ultimo_pago': vehicle.vehiculo_fec_ultimo_pago,
          'vehiculo_vlr_ultimo_pago': vehicle.vehiculo_vlr_ultimo_pago,
          'vehiculo_recibo': vehicle.vehiculo_recibo,
          'vehiculo_primer_mantenimiento': vehicle.vehiculo_primer_mantenimiento,
          'vehiculo_ultimo_mantenimiento': vehicle.vehiculo_ultimo_mantenimiento,
          'vehiculo_categoria': vehicle.vehiculo_categoria,
          'vehiculo_tipo_llave': vehicle.vehiculo_tipo_llave,
          'vehiculo_posicion_llave': vehicle.vehiculo_posicion_llave,
          'vehiculo_fec_estado': vehicle.vehiculo_fec_estado,
          'vehiculo_plan_pago': vehicle.vehiculo_plan_pago,
          'vehiculo_prendido_apagado': vehicle.vehiculo_prendido_apagado,
          'vehiculo_piquera': vehicle.vehiculo_piquera,
          'vehiculo_fec_inicio_piquera': vehicle.vehiculo_fec_inicio_piquera,
          'vehiculo_factura_compra': vehicle.vehiculo_factura_compra,
          'vehiculo_fec_factura_compra': vehicle.vehiculo_fec_factura_compra,
          'vehiculo_valor_compra': vehicle.vehiculo_valor_compra,
          'vehiculo_num_poliza': vehicle.vehiculo_num_poliza,
          'vehiculo_fec_poliza': vehicle.vehiculo_fec_poliza,
          'vehiculo_observaciones': vehicle.vehiculo_observaciones,
          'vehiculo_picoyplaca_lunes': vehicle.vehiculo_picoyplaca_lunes,
          'vehiculo_picoyplaca_martes': vehicle.vehiculo_picoyplaca_martes,
          'vehiculo_picoyplaca_miercoles': vehicle.vehiculo_picoyplaca_miercoles,
          'vehiculo_picoyplaca_jueves': vehicle.vehiculo_picoyplaca_jueves,
          'vehiculo_picoyplaca_viernes': vehicle.vehiculo_picoyplaca_viernes,
          'vehiculo_picoyplaca_sabado': vehicle.vehiculo_picoyplaca_sabado,
          'vehiculo_picoyplaca_domingo': vehicle.vehiculo_picoyplaca_domingo,
      }

      return JSONResponse(content=jsonable_encoder(vehicle_info))
  except Exception as e:
      return JSONResponse(content={"error": str(e)})
  finally:
      db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.post("/vehicles/", response_model=VehicleCreate, tags=["Vehicles"])
def create_vehicle(vehicle: VehicleCreate):
    db = session()
    try:
        panama_timezone = pytz.timezone('America/Panama')
        now_in_panama = datetime.now(panama_timezone)
        fecha = now_in_panama.strftime("%Y-%m-%d %H:%M:%S")
        
        new_vehicle = Vehiculos(
            BLINDAJE=vehicle.vehiculo_blindaje,
            CAPACIDAD=vehicle.vehiculo_capacidad,
            CENTRAL=vehicle.vehiculo_central,
            CHASISNRO=vehicle.vehiculo_chasis,
            CHASISREG=vehicle.vehiculo_chasis_reg,
            CILINDRAJE=vehicle.vehiculo_cilindraje,
            CLASEVEHIC=vehicle.vehiculo_clase,
            COD_BARRAS=vehicle.vehiculo_codigo_barras,
            COLORES=vehicle.vehiculo_color,
            COMBUSTIBL=vehicle.vehiculo_combustible,
            CONSECUTIV=vehicle.vehiculo_consecutivo,
            CTA_GASTO=vehicle.vehiculo_cta_gasto,
            DECLA_IMPO=vehicle.vehiculo_dec_importacion,
            FEC_IMPORT=vehicle.vehiculo_fec_importacion,
            FEC_MATRIC=vehicle.vehiculo_fec_matricula,
            MODELO=vehicle.vehiculo_fec_modelo,
            FEC_VENCIM=vehicle.vehiculo_fec_vencimiento_matricula,
            PERMISOVCE=vehicle.vehiculo_fec_vencimiento_permiso,
            KILOMETRAJ=vehicle.vehiculo_kilometraje,
            LATERAL=vehicle.vehiculo_lateral,
            LICETRANSI=vehicle.vehiculo_licencia_nro,
            FEC_EXPEDI=vehicle.vehiculo_licencia_fec,
            LIMI_PROPI=vehicle.vehiculo_limit_propiedad,
            NOMMARCA=vehicle.vehiculo_marca,
            MODALIDAD=vehicle.vehiculo_modalidad,
            LINEA=vehicle.vehiculo_modelo,
            MOTORNRO=vehicle.vehiculo_motor,
            MOTORREG=vehicle.vehiculo_motor_reg,
            NE=vehicle.vehiculo_ne,
            NRO_CUPO=vehicle.vehiculo_nro_cupo,
            PUERTAS=vehicle.vehiculo_nro_puertas,
            NUMERO=vehicle.vehiculo_numero,
            ORG_TRANSI=vehicle.vehiculo_organismo_transito,
            PANAPASSNU=vehicle.vehiculo_panapass,
            PANAPASSPW=vehicle.vehiculo_panapass_pwd,
            PERMISONRO=vehicle.vehiculo_permiso_nro,
            PLACA=vehicle.vehiculo_placa,
            POTENCIAHP=vehicle.vehiculo_potencia,
            PROPI_IDEN=vehicle.vehiculo_propietario,
            RESTR_MOBI=vehicle.vehiculo_restriccion_movilidad,
            SERIENRO=vehicle.vehiculo_serie,
            SERIEREG=vehicle.vehiculo_serie_reg,
            SERVICIO=vehicle.vehiculo_servicio,
            TIPOCARROC=vehicle.vehiculo_tipo,
            MOTORVIN=vehicle.vehiculo_vin,
            FEC_CREADO=fecha,

            GPS_FEC=vehicle.vehiculo_fec_gps,
            FEC_SOAT=vehicle.vehiculo_fec_soat,
            FEC_AMBIEN=vehicle.vehiculo_fec_ambient,
            FEC_SEGCON=vehicle.vehiculo_fec_segcon,
            FEC_TAROPE=vehicle.vehiculo_fec_tarope,
            FEC_RESCIV=vehicle.vehiculo_fec_resciv,
            FEC_RESCI2=vehicle.vehiculo_fec_resci2,
            FEC_EXTING=vehicle.vehiculo_fec_exting,
            FEC_TECNOM=vehicle.vehiculo_fec_tecnomec,
            FEC_PLAPUB=vehicle.vehiculo_fec_plapub,
            FEC_CEROPE=vehicle.vehiculo_fec_cerope,
            FEC_1PAGO=vehicle.vehiculo_fec_1pago,
            FEC_ULTPAG=vehicle.vehiculo_fec_ultpag,
            FEC_1MANTE=vehicle.vehiculo_fec_1mante,
            FEC_ULTMAN=vehicle.vehiculo_fec_ultman,
            FEC_PIQUER=vehicle.vehiculo_fec_piquera,
            FEC_ESTADO=vehicle.vehiculo_fec_estado,
            FEC_SINIES=vehicle.vehiculo_fec_sinies,
            FEC_ESTAD2=vehicle.vehiculo_fec_estad2,
            FEC_ESTAD3=vehicle.vehiculo_fec_estad3,
            FEC_ESTAD4=vehicle.vehiculo_fec_estad4,
            FEC_COMPRA=vehicle.vehiculo_fec_compra,
            FEC_POLIZA=vehicle.vehiculo_fec_poliza,
        )

        db.add(new_vehicle)
        db.commit()

        return JSONResponse(content={"message": "Vehicle created successfully"})
    except Exception as e:
        # Log para capturar la excepción
        print("Error al crear el vehículo: ", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.put("/vehicle/{vehicle_id}/", response_model = VehicleUpdate, tags=["Vehicles"])
def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate):
  db = session()
  try:
    data = db.query(Vehiculos).filter(Vehiculos.CONSECUTIV == vehicle_id).first()
   
    if not data:
      return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)
    
    data.PLACA = vehicle.vehiculo_placa
    data.NUMERO = vehicle.vehiculo_numero
    data.MARCA = vehicle.vehiculo_marca
    data.LINEA = vehicle.vehiculo_modelo
    data.MODELO = vehicle.vehiculo_fec_modelo
    data.CILINDRAJE = vehicle.vehiculo_cilindraje
    data.PUERTAS = vehicle.vehiculo_nro_puertas
    data.LICETRANSI = vehicle.vehiculo_licencia_nro
    data.FEC_EXPEDI = vehicle.vehiculo_licencia_fec
    data.COLORES = vehicle.vehiculo_color
    data.SERVICIO = vehicle.vehiculo_servicio
    data.FEC_MATRIC = vehicle.vehiculo_fec_matricula
    data.FEC_VENCIM = vehicle.vehiculo_fec_vencimiento_matricula
    data.FEC_IMPORT = vehicle.vehiculo_fec_importacion
    data.CLASEVEHIC = vehicle.vehiculo_clase
    data.TIPOCARROC = vehicle.vehiculo_tipo
    data.COMBUSTIBL = vehicle.vehiculo_combustible
    data.CAPACIDAD = vehicle.vehiculo_capacidad
    data.NE = vehicle.vehiculo_ne
    data.MOTORVIN = vehicle.vehiculo_vin
    data.MOTORNRO = vehicle.vehiculo_motor
    data.MOTORREG = vehicle.vehiculo_motor_reg
    data.SERIENRO = vehicle.vehiculo_serie
    data.SERIEREG = vehicle.vehiculo_serie_reg
    data.CHASISNRO = vehicle.vehiculo_chasis
    data.CHASISREG = vehicle.vehiculo_chasis_reg
    data.PROPI_IDEN = vehicle.vehiculo_propietario
    data.CTA_GASTO = vehicle.vehiculo_cta_gasto
    data.CENTRAL = vehicle.vehiculo_central
    data.NRO_CUPO = vehicle.vehiculo_nro_cupo
    data.PERMISONRO = vehicle.vehiculo_permiso_nro
    data.PERMISOVCE = vehicle.vehiculo_fec_vencimiento_permiso
    data.BLINDAJE = vehicle.vehiculo_blindaje
    data.POTENCIAHP = vehicle.vehiculo_potencia
    data.DECLA_IMPO = vehicle.vehiculo_dec_importacion
    data.RESTR_MOBI = vehicle.vehiculo_restriccion_movilidad
    data.LIMI_PROPI = vehicle.vehiculo_limit_propiedad
    data.ORG_TRANSI = vehicle.vehiculo_organismo_transito
    data.COD_BARRAS = vehicle.vehiculo_codigo_barras
    data.LATERAL = vehicle.vehiculo_lateral
    data.KILOMETRAJ = vehicle.vehiculo_kilometraje
    data.MODALIDAD = vehicle.vehiculo_modalidad
    data.INFO_PANAP = vehicle.vehiculo_consulta_panapass
    data.PANAPASSNU = vehicle.vehiculo_panapass
    data.PANAPASSPW = vehicle.vehiculo_panapass_pwd

    db.commit()

    return JSONResponse(content={"message": "Vehicle updated successfully"}, status_code=200)
  except Exception as e:
    return JSONResponse(content={"error": str(e)}, status_code=500)
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.delete("/vehicle/{vehicle_id}/", tags=["Vehicles"])
async def verify_vehicle_delete(vehicle_id: str):
    db = session()
    try:
        vehicle = db.query(
            CajaRecaudos.NUMERO.label('cajarecaudos'),
            CajasRecaudosContado.NUMERO.label('cajarecaudoscontado'),
            Cartera.UNIDAD.label('cartera'),
            Movienca.UNIDAD.label('movienca')
        ).select_from(Vehiculos).outerjoin(
            CajaRecaudos, Vehiculos.NUMERO == CajaRecaudos.NUMERO
        ).outerjoin(
            CajasRecaudosContado, Vehiculos.NUMERO == CajasRecaudosContado.NUMERO
        ).outerjoin(
            Cartera, Vehiculos.NUMERO == Cartera.UNIDAD
        ).outerjoin(
            Movienca, Vehiculos.NUMERO == Movienca.UNIDAD
        ).filter(
            Vehiculos.CONSECUTIV == vehicle_id
        ).first()

        if not vehicle:
            return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)

        vehicle_conditions = {
            'cajarecaudos': vehicle.cajarecaudos,
            'cajarecaudoscontado': vehicle.cajarecaudoscontado,
            'cartera': vehicle.cartera,
            'movienca': vehicle.movienca
        }

        if any(vehicle_conditions.values()):
            return JSONResponse(content={"message": "Vehicle can't be deleted"})

        # If there are no records in other tables, delete the vehicle
        db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_id).delete()
        db.commit()
        return JSONResponse(content={"message": "Vehicle deleted successfully"})

    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": str(e)})
    finally:
        db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/verify-vehicle-delete/{vehicle_id}/", tags=["Vehicles"])
async def verify_vehicle_delete(vehicle_id: str):
  db = session()
  try: 
    vehicle = db.query(
          CajaRecaudos.NUMERO.label('cajarecaudos'),
          CajasRecaudosContado.NUMERO.label('cajarecaudoscontado'),
          Cartera.UNIDAD.label('cartera'),
          Movienca.UNIDAD.label('movienca')
        ).select_from(Vehiculos).outerjoin(
            CajaRecaudos, Vehiculos.NUMERO == CajaRecaudos.NUMERO
        ).outerjoin(
            CajasRecaudosContado, Vehiculos.NUMERO == CajasRecaudosContado.NUMERO
        ).outerjoin(
            Cartera, Vehiculos.NUMERO == Cartera.UNIDAD
        ).outerjoin(
            Movienca, Vehiculos.NUMERO == Movienca.UNIDAD
        ).filter(
            Vehiculos.CONSECUTIV == vehicle_id
        ).first()

    if not vehicle:
      return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)
    vehicle_conditions = {
      'cajarecaudos': bool(vehicle.cajarecaudos),
      'cajarecaudoscontado': bool(vehicle.cajarecaudoscontado),
      'cartera': bool(vehicle.cartera),
      'movienca': bool(vehicle.movienca)
    }
    return JSONResponse(content=jsonable_encoder(vehicle_conditions))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/vehicle-codes/", tags=["Vehicles"])
async def get_vehicle_codes():
    db = session()
    try:
        vehicles = db.query(Vehiculos.CONSECUTIV, Vehiculos.NUMERO).all()
        vehicle_codes = [{'vehiculo_consecutivo': vehicle.CONSECUTIV, 'vehiculo_numero': vehicle.NUMERO} for vehicle in vehicles]
        return JSONResponse(content=jsonable_encoder(vehicle_codes))
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/vehicles-by-state/{company_code}/{state_code}/", tags=["Vehicles"])
async def get_vehicles_by_state(company_code: str, state_code: str):
    db = session()
    try:
        vehicles = db.query(Vehiculos).filter(
            Vehiculos.EMPRESA == company_code,
            Vehiculos.ESTADO == state_code
        ).all()

        if not vehicles:
            return JSONResponse(content={"message": "No hay vehículos disponibles para la empresa y estado dados"}, status_code=404)

        response = [{'vehicle_number': vehicle.NUMERO, 'vehicle_plate': vehicle.PLACA} for vehicle in vehicles]

        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        db.close()
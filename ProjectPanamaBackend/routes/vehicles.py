from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.vehiculos import Vehiculos
from models.estados import Estados
from models.conductores import Conductores
from schemas.vehicles import VehicleUpdate, VehicleCreate
from models.centrales import Centrales
from models.cajarecaudos import CajaRecaudos
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

@vehicles_router.get("/vehicles", tags=["Vehicles"])
async def get_vehicles():
  db = session()
  try:
    vehicles = db.query(Vehiculos.NUMERO, Vehiculos.PLACA).all()

    vehicles_list = [
      {
        'unidad': vehicle.vehiculo_numero,
        'placa': vehicle.vehiculo_placa
      }
      for vehicle in vehicles
    ]
    return JSONResponse(content=jsonable_encoder(vehicles_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/vehicles/all", tags=["Vehicles"])
async def get_vehicles():
  db = session()
  try:
    vehicles = db.query(
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.MODELO.label('vehiculo_modelo'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
            Vehiculos.MOTORNRO.label('vehiculo_motor'),
            Vehiculos.CHASISNRO.label('vehiculo_chasis'),
            Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
            Vehiculos.EMPRESA.label('vehiculo_empresa'),
            Centrales.NOMBRE.label('vehiculo_central'),
            Vehiculos.NRO_LLAVES.label('vehiculo_nro_llaves'),
            Conductores.NOMBRE.label('vehiculo_conductor'),
            Estados.ESTADO.label('vehiculo_estado'),
            Estados.NOMBRE.label('vehiculo_nombre_estado'),
            Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
            Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
            Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
            Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
            Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
        )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Conductores, Conductores.CODIGO == Vehiculos.CONDUCTOR) \
            .join(Centrales, Centrales.CODIGO == Vehiculos.CENTRAL) \
            .all()

    vehicles_list = [
      {
        'unidad': vehicle.vehiculo_numero,
        'placa': vehicle.vehiculo_placa,
        'modelo': vehicle.vehiculo_modelo,
        'nro_cupo': vehicle.vehiculo_nro_cupo,
        'permiso': vehicle.vehiculo_permiso_nro,
        'motor': vehicle.vehiculo_motor,
        'chasis': vehicle.vehiculo_chasis,
        'matricula': vehicle.vehiculo_fec_matricula,
        'empresa': vehicle.vehiculo_empresa,
        'central': vehicle.vehiculo_central,
        'conductor': vehicle.vehiculo_conductor,
        'estado': vehicle.vehiculo_estado,
        'nombre_estado': vehicle.vehiculo_nombre_estado,
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

@vehicles_router.get('/directorio-vehiculos', tags=["Vehicles"]) 
async def get_vehiculos_detalles():
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
            Vehiculos.EMPRESA.label('vehiculo_empresa'),
            Centrales.NOMBRE.label('vehiculo_central'),
        )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Centrales, Centrales.CODIGO == Vehiculos.CENTRAL) \
            .all()
        
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
                'vehiculo_empresa': resultado.vehiculo_empresa,
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
              "Content-Disposition": "inline; detalles-vehiculos.pdf"
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

@vehicles_router.get("/vehicles/{vehicle_id}", tags=["Vehicles"])
async def get_vehicle(vehicle_id: int):
  db = session()
  try:
    vehicle = db.query(
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.MODELO.label('vehiculo_modelo'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
            Vehiculos.MOTORNRO.label('vehiculo_motor'),
            Vehiculos.CHASISNRO.label('vehiculo_chasis'),
            Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
            Vehiculos.EMPRESA.label('vehiculo_empresa'),
            Conductores.NOMBRE.label('vehiculo_conductor'),
            Estados.NOMBRE.label('vehiculo_estado'),
            Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
            Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
            Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
            Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
            Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
        )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Conductores, Conductores.CODIGO == Vehiculos.CONDUCTOR) \
            .filter(Vehiculos.PLACA == vehicle_id) \
            .first()

    vehicle_info = {
      'unidad': vehicle.vehiculo_numero,
      'placa': vehicle.vehiculo_placa,
      'modelo': vehicle.vehiculo_modelo,
      'nro_cupo': vehicle.vehiculo_nro_cupo,
      'permiso': vehicle.vehiculo_permiso_nro,
      'motor': vehicle.vehiculo_motor,
      'chasis': vehicle.vehiculo_chasis,
      'matricula': vehicle.vehiculo_fec_matricula,
      'empresa': vehicle.vehiculo_empresa,
      'conductor': vehicle.vehiculo_conductor,
      'estado': vehicle.vehiculo_estado,
      'vlr_cta': vehicle.vehiculo_cuota_diaria,
      'nro_ctas': vehicle.vehiculo_nro_Ctas,
      'panapass': vehicle.vehiculo_panapass,
      'clave': vehicle.vehiculo_panapass_pwd,
      'saldo': vehicle.vehiculo_saldo_panapass
    }
    
    return JSONResponse(content=jsonable_encoder(vehicle_info))
  except Exception as e:    
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.post("/vehicle-create", response_model=VehicleCreate, tags=["Vehicles"])
def create_vehicle(vehicle: VehicleCreate):
    db = session()
    try:
        panama_timezone = pytz.timezone('America/Panama')
        now_in_panama = datetime.now(panama_timezone)
        fecha = now_in_panama.strftime("%Y-%m-%d %H:%M:%S")
        
        new_vehicle = Vehiculos(
            NUMERO=vehicle.vehiculo_numero,
            PLACA=vehicle.vehiculo_placa,
            CONSECUTIV=vehicle.vehiculo_consecutivo,
            MARCA=vehicle.vehiculo_marca,
            LINEA=vehicle.vehiculo_modelo,
            MODELO=vehicle.vehiculo_año,
            CILINDRAJE=vehicle.vehiculo_cilindraje,
            PUERTAS=vehicle.vehiculo_nro_puertas,
            LICETRANSI=vehicle.vehiculo_licencia_nro,
            FEC_EXPEDI=vehicle.vehiculo_licencia_fec,
            COLORES=vehicle.vehiculo_color,
            SERVICIO=vehicle.vehiculo_servicio,
            FEC_MATRIC=vehicle.vehiculo_fec_matricula,
            FEC_VENCIM=vehicle.vehiculo_fec_vencimiento_matricula,
            FEC_IMPORT=vehicle.vehiculo_fec_importacion,
            CLASEVEHIC=vehicle.vehicul_clase,
            TIPOCARROC=vehicle.vehiculo_tipo,
            COMBUSTIBL=vehicle.vehiculo_combustible,
            CAPACIDAD=vehicle.vehiculo_capacidad,
            NE=vehicle.vehiculo_ne,
            MOTORNRO=vehicle.vehiculo_motor,
            MOTORREG=vehicle.vehiculo_motor_reg,
            MOTORVIN=vehicle.vehiculo_vin,
            SERIENRO=vehicle.vehiculo_serie,
            SERIEREG=vehicle.vehiculo_serie_reg,
            CHASISNRO=vehicle.vehiculo_chasis,
            CHASISREG=vehicle.vehiculo_chasis_reg,
            PROPI_IDEN=vehicle.vehiculo_propietario,
            CTA_GASTO=vehicle.vehiculo_cta_gasto,
            CENTRAL=vehicle.vehiculo_central,
            FEC_CREADO=fecha,
            NRO_CUPO=vehicle.vehiculo_nro_cupo,
            PERMISONRO=vehicle.vehiculo_permiso_nro,
            PERMISOVCE=vehicle.vehiculo_fec_vencimiento_permiso,
            BLINDAJE=vehicle.vehiculo_blindaje,
            POTENCIAHP=vehicle.vehiculo_potencia,
            DECLA_IMPO=vehicle.vehiculo_dec_importacion,
            RESTR_MOBI=vehicle.vehiculo_restriccion_movilidad,
            LIMI_PROPI=vehicle.vehiculo_limit_propiedad,
            ORG_TRANSI=vehicle.vehiculo_organismo_transito,
            COD_BARRAS=vehicle.vehiculo_codigo_barras,
            LATERAL=vehicle.vehiculo_lateral,
            KILOMETRAJ=vehicle.vehiculo_kilometraje,
            MODALIDAD=vehicle.vehiculo_modalidad,
            INFO_PANAP=vehicle.vehiculo_consulta_panapass,
            PANAPASSNU=vehicle.vehiculo_panapass,
            PANAPASSPW=vehicle.vehiculo_panapass_pwd,
            DOC_PLAPAR = vehicle.vehiculo_placa_particular,  
            FEC_PLAPAR = vehicle.vehiculo_placa_particular_vence,
            DOC_PLAPUB = vehicle.vehiculo_placa_publica,
            FEC_PLAPUB = vehicle.vehiculo_placa_publica_vence,
            DOC_RESCIV = vehicle.vehiculo_poliza_responsabilidad_civil,
            FEC_RESCIV = vehicle.vehiculo_poliza_responsabilidad_civil_vence,
            DOC_EXTING = vehicle.vehiculo_extinguidor,
            FEC_EXTING = vehicle.vehiculo_extinguidor_vence,
            DOC_CEROPE = vehicle.vehiculo_certificado_operacion,
            FEC_CEROPE = vehicle.vehiculo_certificado_operacion_fec,
            NROENTREGA = vehicle.vehiculo_nro_total_cuotas,
            CUO_DIARIA = vehicle.vehiculo_vlr_cuo_diaria,
            CTA_RENTA = vehicle.vehiculo_renta_diaria,
            CTA_SINIES = vehicle.vehiculo_ahorro_siniestro,
            PAGA_ADMON = vehicle.vehiculo_cobro_admon,
            CUO_ADMON = vehicle.vehiculo_admon,
            CUO_REPVEH = vehicle.vehiculo_reposicion,
            CUO_MANTEN = vehicle.vehiculo_mantenimiento,
            CUO_RENDIM = vehicle.vehiculo_rendimientos_propietario,
            PAGO_LUN = vehicle.vehiculo_lunes,
            PAGO_MAR = vehicle.vehiculo_martes,
            PAGO_MIE = vehicle.vehiculo_miercoles,
            PAGO_JUE = vehicle.vehiculo_jueves,
            PAGO_VIE = vehicle.vehiculo_viernes,
            PAGO_SAB = vehicle.vehiculo_sabado,
            PAGO_DOM = vehicle.vehiculo_domingo,
            FORMAPAGO = vehicle.vehiculo_pago,
            MULTA = vehicle.vehiculo_multa_pago,
            FEC_1PAGO = vehicle.vehiculo_fec_primer_pago,
            FEC_ULTPAG = vehicle.vehiculo_fec_ultimo_pago,
            VLR_ULTPAG = vehicle.vehiculo_vlr_ultimo_pago,
            REC_ULTPAG = vehicle.vehiculo_recibo,
            FEC_1MANTE = vehicle.vehiculo_primer_mantenimiento,
            FEC_ULTMAN = vehicle.vehiculo_ultimo_mantenimiento,
            CATEGORIA = vehicle.vehiculo_categoria,
            tipo_llave = vehicle.vehiculo_tipo_llave,
            NRO_LLAVES = vehicle.vehiculo_posicion_llave,
            FEC_ESTADO = vehicle.vehiculo_fec_estado,
            GRUPODIARI = vehicle.vehiculo_plan_pago,
            PREND_APAG = vehicle.vehiculo_prendido_apagado,
            PIQUERA = vehicle.vehiculo_piquera,
            FEC_PIQUER = vehicle.vehiculo_fec_inicio_piquera,
            FAC_COMPRA = vehicle.vehiculo_factura_compra,
            FEC_COMPRA = vehicle.vehiculo_fec_factura_compra,
            VLR_COMPRA = vehicle.vehiculo_valor_compra,
            POLIZA = vehicle.vehiculo_num_poliza,
            FEC_POLIZA = vehicle.vehiculo_fec_poliza,
            OBSERVA = vehicle.vehiculo_observaciones,
            LUN = vehicle.vehiculo_picoyplaca_lunes,
            MAR = vehicle.vehiculo_picoyplaca_martes,
            MIE = vehicle.vehiculo_picoyplaca_miercoles,
            JUE = vehicle.vehiculo_picoyplaca_jueves,
            VIE = vehicle.vehiculo_picoyplaca_viernes,
            SAB = vehicle.vehiculo_picoyplaca_sabado,
            DOM = vehicle.vehiculo_picoyplaca_domingo,
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

@vehicles_router.post("/vehicle/{vehicle_id}", response_model = VehicleUpdate, tags=["Vehicles"])
def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate):
  db = session()
  try:
    data = db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_id).first()
    if not data:
      return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)
    data.NUMERO = vehicle.vehiculo_numero
    data.PLACA = vehicle.vehiculo_placa
    data.CONSECUTIV = vehicle.vehiculo_consecutivo
    data.MARCA = vehicle.vehiculo_marca
    data.LINEA = vehicle.vehiculo_modelo
    data.MODELO = vehicle.vehiculo_año
    data.CILINDRAJE = vehicle.vehiculo_cilindraje
    data.PUERTAS = vehicle.vehiculo_nro_puertas
    data.LICETRANSI = vehicle.vehiculo_licencia_nro
    data.FEC_EXPEDI = vehicle.vehiculo_licencia_fec
    data.COLORES = vehicle.vehiculo_color
    data.SERVICIO = vehicle.vehiculo_servicio
    data.FEC_MATRIC = vehicle.vehiculo_fec_matricula
    data.FEC_VENCIM = vehicle.vehiculo_fec_vencimiento_matricula
    data.FEC_IMPORT = vehicle.vehiculo_fec_importacion
    data.CLASEVEHIC = vehicle.vehicul_clase
    data.TIPOCARROC = vehicle.vehiculo_tipo
    data.COMBUSTIBL = vehicle.vehiculo_combustible
    data.CAPACIDAD = vehicle.vehiculo_capacidad
    data.NE = vehicle.vehiculo_ne
    data.MOTORNRO = vehicle.vehiculo_motor
    data.MOTORREG = vehicle.vehiculo_motor_reg
    data.MOTORVIN = vehicle.vehiculo_vin
    data.SERIENRO = vehicle.vehiculo_serie
    data.SERIEREG = vehicle.vehiculo_serie_reg
    data.CHASISNRO = vehicle.vehiculo_chasis
    data.CHASISREG = vehicle.vehiculo_chasis_reg
    data.PROPI_IDEN = vehicle.vehiculo_propietario
    data.CTA_GASTO = vehicle.vehiculo_cta_gasto
    data.CENTRAL = vehicle.vehiculo_central
    data.FEC_CREADO = vehicle.vehiculo_fec_creacion
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
    data.DOC_PLAPAR = vehicle.vehiculo_placa_particular  
    data.FEC_PLAPAR = vehicle.vehiculo_placa_particular_vence
    data.DOC_PLAPUB = vehicle.vehiculo_placa_publica
    data.FEC_PLAPUB = vehicle.vehiculo_placa_publica_vence
    data.DOC_RESCIV = vehicle.vehiculo_poliza_responsabilidad_civil
    data.FEC_RESCIV = vehicle.vehiculo_poliza_responsabilidad_civil_vence
    data.DOC_EXTING = vehicle.vehiculo_extinguidor
    data.FEC_EXTING = vehicle.vehiculo_extinguidor_vence
    data.DOC_CEROPE = vehicle.vehiculo_certificado_operacion
    data.FEC_CEROPE = vehicle.vehiculo_certificado_operacion_fec
    data.NROENTREGA = vehicle.vehiculo_nro_total_cuotas
    data.CUO_DIARIA = vehicle.vehiculo_vlr_cuo_diaria
    data.CTA_RENTA = vehicle.vehiculo_renta_diaria
    data.CTA_SINIES = vehicle.vehiculo_ahorro_siniestro
    data.PAGA_ADMON = vehicle.vehiculo_cobro_admon
    data.CUO_ADMON = vehicle.vehiculo_admon
    data.CUO_REPVEH = vehicle.vehiculo_reposicion
    data.CUO_MANTEN = vehicle.vehiculo_mantenimiento
    data.CUO_RENDIM = vehicle.vehiculo_rendimientos_propietario
    data.PAGO_LUN = vehicle.vehiculo_lunes
    data.PAGO_MAR = vehicle.vehiculo_martes
    data.PAGO_MIE = vehicle.vehiculo_miercoles
    data.PAGO_JUE = vehicle.vehiculo_jueves
    data.PAGO_VIE = vehicle.vehiculo_viernes
    data.PAGO_SAB = vehicle.vehiculo_sabado
    data.PAGO_DOM = vehicle.vehiculo_domingo
    data.FORMAPAGO = vehicle.vehiculo_pago
    data.MULTA = vehicle.vehiculo_multa_pago
    data.FEC_1PAGO = vehicle.vehiculo_fec_primer_pago
    data.FEC_ULTPAG = vehicle.vehiculo_fec_ultimo_pago
    data.VLR_ULTPAG = vehicle.vehiculo_vlr_ultimo_pago
    data.REC_ULTPAG = vehicle.vehiculo_recibo
    data.FEC_1MANTE = vehicle.vehiculo_primer_mantenimiento
    data.FEC_ULTMAN = vehicle.vehiculo_ultimo_mantenimiento
    data.CATEGORIA = vehicle.vehiculo_categoria
    data.tipo_llave = vehicle.vehiculo_tipo_llave
    data.NRO_LLAVES = vehicle.vehiculo_posicion_llave
    data.FEC_ESTADO = vehicle.vehiculo_fec_estado
    data.GRUPODIARI = vehicle.vehiculo_plan_pago
    data.PREND_APAG = vehicle.vehiculo_prendido_apagado
    data.PIQUERA = vehicle.vehiculo_piquera
    data.FEC_PIQUER = vehicle.vehiculo_fec_inicio_piquera
    data.FAC_COMPRA = vehicle.vehiculo_factura_compra
    data.FEC_COMPRA = vehicle.vehiculo_fec_factura_compra
    data.VLR_COMPRA = vehicle.vehiculo_valor_compra
    data.POLIZA = vehicle.vehiculo_num_poliza
    data.FEC_POLIZA = vehicle.vehiculo_fec_poliza
    data.OBSERVA = vehicle.vehiculo_observaciones
    data.LUN = vehicle.vehiculo_picoyplaca_lunes
    data.MAR = vehicle.vehiculo_picoyplaca_martes
    data.MIE = vehicle.vehiculo_picoyplaca_miercoles
    data.JUE = vehicle.vehiculo_picoyplaca_jueves
    data.VIE = vehicle.vehiculo_picoyplaca_viernes
    data.SAB = vehicle.vehiculo_picoyplaca_sabado
    data.DOM = vehicle.vehiculo_picoyplaca_domingo
    db.commit()

    return JSONResponse(content={"message": "Vehicle updated successfully"})
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.delete("/vehicle-delete/{vehicle_id}", tags=["Vehicles"])
async def verify_vehicle_delete(vehicle_id: int):
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
            Vehiculos.NUMERO == vehicle_id
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

@vehicles_router.get("/verify-vehicle-delete/{vehicle_id}", tags=["Vehicles"])
async def verify_vehicle_delete(vehicle_id: int):
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
            Vehiculos.NUMERO == vehicle_id
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
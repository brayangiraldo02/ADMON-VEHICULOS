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
            Conductores.NOMBRE.label('vehiculo_conductor'),
            Estados.NOMBRE.label('vehiculo_estado'),
            Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
            Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
            Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
            Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
            Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
        )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Conductores, Conductores.CODIGO == Vehiculos.CONDUCTOR) \
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
        'conductor': vehicle.vehiculo_conductor,
        'estado': vehicle.vehiculo_estado,
        'vlr_cta': vehicle.vehiculo_cuota_diaria,
        'nro_ctas': vehicle.vehiculo_nro_Ctas,
        'panapass': vehicle.vehiculo_panapass,
        'clave': vehicle.vehiculo_panapass_pwd,
        'saldo': vehicle.vehiculo_saldo_panapass
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
            # LICENCIA_FEC=vehicle.vehiculo_licencia_fec,
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
            PANAPASSPW=vehicle.vehiculo_panapass_pwd
        )
        db.add(new_vehicle)
        db.commit()

        return JSONResponse(content={"message": "Vehicle created successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.post("/vehicle/{owner_id}", response_model = VehicleUpdate, tags=["Vehicles"])
def update_vehicle(owner_id: str, vehicle: VehicleUpdate):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == owner_id).first()
    if not vehicle:
      return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)
    vehicle.NUMERO = vehicle.vehiculo_numero
    vehicle.PLACA = vehicle.vehiculo_placa
    vehicle.CONSECUTIV = vehicle.vehiculo_consecutivo
    vehicle.MARCA = vehicle.vehiculo_marca
    vehicle.LINEA = vehicle.vehiculo_modelo
    vehicle.MODELO = vehicle.vehiculo_año
    vehicle.CILINDRAJE = vehicle.vehiculo_cilindraje
    vehicle.PUERTAS = vehicle.vehiculo_nro_puertas
    vehicle.LICETRANSI = vehicle.vehiculo_licencia_nro
    # vehicle.LICENCIA_FEC = vehicle.vehiculo_licencia_fec
    vehicle.COLORES = vehicle.vehiculo_color
    vehicle.SERVICIO = vehicle.vehiculo_servicio
    vehicle.FEC_MATRIC = vehicle.vehiculo_fec_matricula
    vehicle.FEC_VENCIM = vehicle.vehiculo_fec_vencimiento_matricula
    vehicle.FEC_IMPORT = vehicle.vehiculo_fec_importacion
    vehicle.CLASEVEHIC = vehicle.vehicul_clase
    vehicle.TIPOCARROC = vehicle.vehiculo_tipo
    vehicle.COMBUSTIBL = vehicle.vehiculo_combustible
    vehicle.CAPACIDAD = vehicle.vehiculo_capacidad
    vehicle.NE = vehicle.vehiculo_ne
    vehicle.MOTORNRO = vehicle.vehiculo_motor
    vehicle.MOTORREG = vehicle.vehiculo_motor_reg
    vehicle.MOTORVIN = vehicle.vehiculo_vin
    vehicle.SERIENRO = vehicle.vehiculo_serie
    vehicle.SERIEREG = vehicle.vehiculo_serie_reg
    vehicle.CHASISNRO = vehicle.vehiculo_chasis
    vehicle.CHASISREG = vehicle.vehiculo_chasis_reg
    vehicle.PROPI_IDEN = vehicle.vehiculo_propietario
    vehicle.CTA_GASTO = vehicle.vehiculo_cta_gasto
    vehicle.CENTRAL = vehicle.vehiculo_central
    vehicle.FEC_CREADO = vehicle.vehiculo_fecha_creacion
    vehicle.NRO_CUPO = vehicle.vehiculo_nro_cupo
    vehicle.PERMISONRO = vehicle.vehiculo_permiso_nro
    vehicle.PERMISOVCE = vehicle.vehiculo_fec_vencimiento_permiso
    vehicle.BLINDAJE = vehicle.vehiculo_blindaje
    vehicle.POTENCIAHP = vehicle.vehiculo_potencia
    vehicle.DECLA_IMPO = vehicle.vehiculo_dec_importacion
    vehicle.RESTR_MOBI = vehicle.vehiculo_restriccion_movilidad
    vehicle.LIMI_PROPI = vehicle.vehiculo_limit_propiedad
    vehicle.ORG_TRANSI = vehicle.veh
    vehicle.COD_BARRAS = vehicle.vehiculo_codigo_barras
    vehicle.LATERAL = vehicle.vehiculo_lateral
    vehicle.KILOMETRAJ = vehicle.vehiculo_kilometraje
    vehicle.MODALIDAD = vehicle.vehiculo_modalidad
    vehicle.INFO_PANAP = vehicle.vehiculo_consulta_panapass
    vehicle.PANAPASSNU = vehicle.vehiculo_panapass
    vehicle.PANAPASSPW = vehicle.vehiculo_panapass_pwd    
    db.commit()

    return JSONResponse(content={"message": "Vehicle updated successfully"})
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#-------------------------------------------------------------------------------------------

@vehicles_router.get("/vehicle-delete/{vehicle_id}", tags=["Vehicles"])
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
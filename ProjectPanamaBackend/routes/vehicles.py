from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.vehiculos import Vehiculos
from models.estados import Estados
from models.conductores import Conductores
from models.centrales import Centrales
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

@vehicles_router.get('/directorio-vehiculos') 
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
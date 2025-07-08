from fastapi.responses import FileResponse, JSONResponse
import jinja2
from config.dbconnection import session
from models.propietarios import Propietarios
from models.conductores import Conductores
from models.vehiculos import Vehiculos
from models.inspecciones import Inspecciones
from models.tiposinspeccion import TiposInspeccion
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile, File, BackgroundTasks
import os
import shutil
from typing import List
from collections import defaultdict
from datetime import datetime
import pytz
from utils.pdf import html2pdf
import tempfile

async def owners_data(company_code: str):
  db = session()
  try:
    owners = db.query(Propietarios).filter(Propietarios.EMPRESA == company_code, Propietarios.CODIGO != "").all()
    if not owners:
      return JSONResponse(content={"message": "Owner not found"}, status_code=404)

    result = []

    for owner in owners:
      owner_data = {
        "codigo_propietario": owner.CODIGO,
        "nombre_propietario": owner.NOMBRE,
        "conductores": [],
        "vehiculos": []
      }

      # Obtener vehículos de ese propietario
      vehicles = db.query(Vehiculos).filter(Vehiculos.PROPI_IDEN == owner.CODIGO, Vehiculos.PLACA != "", Vehiculos.NUMERO != "").all()

      for vehicle in vehicles:
        owner_data["vehiculos"].append({
          "placa_vehiculo": vehicle.PLACA,
          "numero_unidad": vehicle.NUMERO,
          "codigo_conductor": vehicle.CONDUCTOR,
          "marca": vehicle.NOMMARCA,
          "linea": vehicle.LINEA
        })

        # Obtener conductor relacionado al vehículo
        drivers = db.query(Conductores).filter(Conductores.CODIGO == vehicle.CONDUCTOR, Conductores.CODIGO != "").all()

        for driver in drivers:
          if driver and driver.CODIGO not in owner_data["conductores"]:
            owner_data["conductores"].append({
              "codigo_conductor": driver.CODIGO,
              "numero_unidad": driver.UND_NRO,
              "nombre_conductor": driver.NOMBRE,
              "cedula": driver.CEDULA
            })

      result.append(owner_data)

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def vehicles_data(company_code: str):
  db = session()
  try:
    vehicles = db.query(Vehiculos).filter(Vehiculos.EMPRESA == company_code, Vehiculos.PLACA != "", Vehiculos.NUMERO != "").all()
    if not vehicles:
      return JSONResponse(content={"message": "Vehicles not found"}, status_code=404)

    result = []

    for vehicle in vehicles:
      result.append({
        "placa_vehiculo": vehicle.PLACA,
        "numero_unidad": vehicle.NUMERO,
        "codigo_conductor": vehicle.CONDUCTOR,
        "codigo_propietario": vehicle.PROPI_IDEN,
        "marca": vehicle.NOMMARCA,
        "linea": vehicle.LINEA,
        "modelo": vehicle.MODELO
      })

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def drivers_data(company_code: str):
  db = session()
  try:
    drivers = db.query(Conductores.CODIGO, Conductores.UND_NRO, Conductores.NOMBRE,
                       Conductores.CEDULA, Vehiculos.PROPI_IDEN
                      ).outerjoin(
                        Vehiculos, Conductores.CODIGO == Vehiculos.CONDUCTOR
                      ).filter(
                        Conductores.EMPRESA == company_code, 
                        Conductores.CODIGO != ""
                      ).all()
    
    if not drivers:
      return JSONResponse(content={"message": "Drivers not found"}, status_code=404)

    result = []

    for driver in drivers:
      result.append({
        "codigo_conductor": driver.CODIGO,
        "numero_unidad": driver.UND_NRO,
        "nombre_conductor": driver.NOMBRE,
        "cedula": driver.CEDULA,
        "codigo_propietario": driver.PROPI_IDEN or ""
      })

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def inspections_info(data, company_code: str):
  db = session()
  try:
    filters = [
        Inspecciones.FECHA >= data.fechaInicial,
        Inspecciones.FECHA <= data.fechaFinal,
    ]

    # Filtrar inspecciones por propietario, conductor y vehículo
    if data.propietario != '':
        filters.append(Inspecciones.PROPI_IDEN == data.propietario)
    
    if data.vehiculo != '':
        filters.append(Inspecciones.UNIDAD == data.vehiculo)
    
    if data.conductor != '':
        filters.append(Inspecciones.CONDUCTOR == data.conductor)

    inspections = db.query(Inspecciones).filter(*filters).all()

    inspections_types = db.query(TiposInspeccion).filter(TiposInspeccion.EMPRESA == company_code).all()

    inspections_dict = {inspection.CODIGO: inspection.NOMBRE for inspection in inspections_types}

    inspections_data = []

    for inspection in inspections:
      inspections_data.append({
        "id": inspection.ID,
        "fecha_hora": inspection.FECHA.strftime('%d-%m-%Y') + ' ' + inspection.HORA.strftime('%H:%M') if inspection.FECHA and inspection.HORA else None,
        "tipo_inspeccion": inspections_dict.get(inspection.TIPO_INSPEC, ""),
        "descripcion": inspection.DESCRIPCION,
        "unidad": inspection.UNIDAD,
        "placa": inspection.PLACA,
        "nombre_usuario": inspection.USUARIO,
        "acciones": ""
      })

    if not inspections_data:
      return JSONResponse(content={"message": "No inspections found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(inspections_data), status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

#! Cambiar por el directorio que es
upload_directory = "uploads"


async def upload_image(vehicle_number: str, image: UploadFile = File(...)):
  try:
    vehicle_number_path = os.path.join(upload_directory, vehicle_number, "fotos")
    os.makedirs(vehicle_number_path, exist_ok=True)

    file_path = os.path.join(vehicle_number_path, image.filename)
    
    with open(file_path, "wb") as buffer:
      shutil.copyfileobj(image.file, buffer)

    file_path = file_path.replace("\\", "/")  # Normalize path for JSON response

    return JSONResponse(content={ "file_path": file_path}, status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)

#-----------------------------------------------------------------------------------------------
async def report_inspections(data, company_code: str):
  db = session()
  try:
    filters = [
        Inspecciones.FECHA >= data.fechaInicial,
        Inspecciones.FECHA <= data.fechaFinal,
    ]

    # Filtrar inspecciones por propietario, conductor y vehículo
    if data.propietario != '':
        filters.append(Inspecciones.PROPI_IDEN == data.propietario)
    
    if data.vehiculo != '':
        filters.append(Inspecciones.UNIDAD == data.vehiculo)
    
    if data.conductor != '':
        filters.append(Inspecciones.CONDUCTOR == data.conductor)

    inspections = db.query(Inspecciones).filter(*filters).all()

    if not inspections:
      return JSONResponse(content={"message": "No inspections found"}, status_code=404)

    inspections_types = db.query(TiposInspeccion).filter(TiposInspeccion.EMPRESA == company_code).all()

    inspections_dict = {inspection.CODIGO: inspection.NOMBRE for inspection in inspections_types}

    owners_dict = defaultdict(list)

    for inspection in inspections:
      inspections_data ={
        "id": inspection.ID,
        "fecha_hora": inspection.FECHA.strftime('%d-%m-%Y') + ' ' + inspection.HORA.strftime('%H:%M') if inspection.FECHA and inspection.HORA else None,
        "tipo_inspeccion": inspections_dict.get(inspection.TIPO_INSPEC, "").title(),
        "descripcion": inspection.DESCRIPCION,
        "unidad": inspection.UNIDAD,
        "placa": inspection.PLACA,
        "nombre_usuario": inspection.USUARIO,
        "propietario": inspection.PROPI_IDEN,
        "acciones": ""
      }
      owners_dict[inspection.PROPI_IDEN].append(inspections_data)

    result = []
    for owner_code, inspections in owners_dict.items():
      owner = db.query(Propietarios).filter(Propietarios.CODIGO == owner_code).first()
      if owner:
        result.append({
          "codigo_propietario": owner.CODIGO,
          "nombre_propietario": owner.NOMBRE,
          "cantidad_inspecciones": len(inspections),
          "inspecciones": inspections
        })


    #Total de inspecciones sumando la cantidad de inspecciones por propietario
    total_inspecciones = sum(len(inspections) for inspections in owners_dict.values())

    # Datos de la fecha y hora actual
    # Define la zona horaria de Ciudad de Panamá
    panama_timezone = pytz.timezone('America/Panama')
    # Obtén la hora actual en la zona horaria de Ciudad de Panamá
    now_in_panama = datetime.now(panama_timezone)
    # Formatea la fecha y la hora según lo requerido
    fecha = now_in_panama.strftime("%d/%m/%Y")
    hora_actual = now_in_panama.strftime("%I:%M:%S %p")

    titulo = 'Reporte de inspecciones'
    data_view = {
      'inspections': result,
      'fechas': {
            "fecha_inicial": datetime.strptime(data.fechaInicial, "%Y-%m-%d").strftime("%d/%m/%Y"),
            "fecha_final": datetime.strptime(data.fechaFinal, "%Y-%m-%d").strftime("%d/%m/%Y")
        },
      'total_inspecciones': total_inspecciones,
      'fecha': fecha,
      'hora': hora_actual,
      'usuario': data.usuario if data.usuario else "",
      'titulo': titulo
    }

    headers = {
      "Content-Disposition": "attachment; filename=reporte-inspecciones.pdf"
    }

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    header_file = "header.html"
    footer_file = "footer.html"
    template = template_env.get_template("ReporteInspecciones.html")
    header = template_env.get_template(header_file)
    footer = template_env.get_template(footer_file)
    output_text = template.render(data_view=data_view)
    output_header = header.render(data_view=data_view)
    output_footer = footer.render(data_view=data_view)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='latin-1') as html_file:
      html_path = html_file.name
      html_file.write(output_text)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='latin-1') as header_file:
      header_path = header_file.name
      header_file.write(output_header)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='latin-1') as footer_file:
      footer_path = footer_file.name
      footer_file.write(output_footer)
    pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name

    html2pdf(titulo, html_path, pdf_path, header_path=header_path, footer_path=footer_path)

    background_tasks = BackgroundTasks()
    background_tasks.add_task(os.remove, html_path)
    background_tasks.add_task(os.remove, header_path)
    background_tasks.add_task(os.remove, footer_path)
    background_tasks.add_task(os.remove, pdf_path)

    response = FileResponse(
        pdf_path, 
        media_type='application/pdf', 
        filename='templates/reporte-inspecciones.pdf', 
        headers=headers,
        background=background_tasks
      )

    return response
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.propietarios import Propietarios
from models.conductores import Conductores
from models.vehiculos import Vehiculos
from models.inspecciones import Inspecciones
from fastapi.encoders import jsonable_encoder

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
        "marca": vehicle.NOMMARCA,
        "linea": vehicle.LINEA
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
    drivers = db.query(Conductores).filter(Conductores.EMPRESA == company_code, Conductores.CODIGO != "").all()
    if not drivers:
      return JSONResponse(content={"message": "Drivers not found"}, status_code=404)

    result = []

    for driver in drivers:
      result.append({
        "codigo_conductor": driver.CODIGO,
        "numero_unidad": driver.UND_NRO,
        "nombre_conductor": driver.NOMBRE,
        "cedula": driver.CEDULA
      })

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def inspections_info(data):
  db = session()
  try:
    filters = [
        Inspecciones.FECHA >= data.primeraFecha,
        Inspecciones.FECHA <= data.ultimaFecha
    ]

    # Filtrar inspecciones por propietario, conductor y vehículo
    if data.propietario != '0':
        filters.append(Inspecciones.PROPI_IDEN == data.propietario)
    
    if data.vehiculo != '0':
        filters.append(Inspecciones.UNIDAD == data.vehiculo)
    
    if data.conductor != '0':
        filters.append(Inspecciones.CONDUCTOR == data.conductor)

    inspections = db.query(Inspecciones).filter(*filters).all()

    inspections_data = []

    for inspection in inspections:
      inspections_data.append({
        "id": inspection.ID,
        "fecha_hora": inspection.FECHA.strftime('%d-%m-%Y') + ' ' + inspection.HORA.strftime('%H:%M') if inspection.FECHA and inspection.HORA else None,
        "tipo_inspeccion": inspection.TIPO_INSPEC,
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
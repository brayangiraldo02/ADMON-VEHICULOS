from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.propietarios import Propietarios
from models.vehiculos import Vehiculos
from models.conductores import Conductores
from models.estados import Estados
from schemas.owners import PropietarioUpdate, PropietarioCreate, RepresentantePropietario
from models.centrales import Centrales
from models.permisosusuario import PermisosUsuario
from middlewares.JWTBearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from datetime import datetime
owners_router = APIRouter()

# PETICIÓN DE LISTA DE PROPIETARIOS A LA BASE DE DATOS 
# ---------------------------------------------------------------------------------------------------------------
@owners_router.get("/owners", tags=["Owners"])
async def get_owners():
  db = session()
  try:
    owners = db.query(Propietarios.CODIGO, Propietarios.NOMBRE).all()
    owners_list = [{'id': owner.CODIGO, 'name': owner.NOMBRE} for owner in owners]
    return JSONResponse(content=jsonable_encoder(owners_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
# ---------------------------------------------------------------------------------------------------------------

@owners_router.get("/owners/all", tags=["Owners"])
async def get_all_owners():
  db = session()
  try:
    owners = db.query(
      Propietarios.CODIGO.label('codigo'),
      Propietarios.NOMBRE.label('nombre_propietario'),
      Propietarios.RUC.label('ruc'),
      Propietarios.TELEFONO.label('telefono'),
      Propietarios.CELULAR.label('celular'),
      Propietarios.REPRESENTA.label('representante'),
      Centrales.NOMBRE.label('central'),
      PermisosUsuario.NOMBRE.label('auditor'),
      Propietarios.GRUPO.label('cnt'),
      Propietarios.DESCUENTO.label('dcto'),
      Propietarios.ESTADO.label('estado')
    ).join(
      PermisosUsuario, Propietarios.USUARIO == PermisosUsuario.CODIGO
    ).join(
      Centrales, Propietarios.CENTRAL == Centrales.CODIGO
    ).all()

    owners_list = []
    for owner in owners:
      if owner.estado == 1:
        estado = 'Activo'
      elif owner.estado == 2:
        estado = 'Suspendido'
      elif owner.estado == 3:
        estado = 'Retirado'
      else:
        estado = 'Desconocido'

      owner_list = {
        'codigo': owner.codigo,
        'nombre_propietario': owner.nombre_propietario,
        'ruc': owner.ruc,
        'telefono': owner.telefono,
        'celular': owner.celular,
        'representante': owner.representante,
        'central': owner.central,
        'auditor': owner.auditor,
        'cnt': owner.cnt,
        'dcto': owner.dcto,
        'estado': estado
      }
      owners_list.append(owner_list)

    # owners_list = [
    #   {
    #     'codigo': owner.codigo,
    #     'nombre_propietario': owner.nombre_propietario,
    #     'ruc': owner.ruc,
    #     'telefono': owner.telefono,
    #     'celular': owner.celular,
    #     'representante': owner.representante,
    #     'central': owner.central,
    #     'auditor': owner.auditor,
    #     'cnt': owner.cnt,
    #     'dcto': owner.dcto,
    #     'estado': owner.estado
    #   }
    #   for owner in owners
    # ]
    return JSONResponse(content=jsonable_encoder(owners_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
# ---------------------------------------------------------------------------------------------------------------

# PETICIÓN DE UN PROPIETARIO ESPECÍFICO A LA BASE DE DATOS
# ---------------------------------------------------------------------------------------------------------------
""" @owners_router.get("/owner/{owner_id}", tags=["Owners"])
async def get_owner(owner_id: int):
  db = session()
  try:
    owner = db.query(
      Propietarios
    ).filter(
      Propietarios.CODIGO == owner_id
    ).first()

    if not owner:
      return JSONResponse(content={"error": "Owner not found"}, status_code=404)

    if owner.ESTADO == 1:
      estado = 'Activo'
    elif owner.ESTADO == 2:
      estado = 'Suspendido'
    elif owner.ESTADO == 3:
      estado = 'Retirado'
    else:
      estado = 'Desconocido'

    owner_dict = {
      'codigo': owner.CODIGO,
      'nombre_propietario': owner.NOMBRE,
      'razon_social': owner.RAZONSOCIA,
      'sexo': owner.REP_SEXO,
      'estado_civil': owner.REP_ESTADO,
      'tipo_documento': owner.REP_TIPDOC,
      'numero_documento': owner.REP_NUMERO,
      'nacionalidad': owner.REP_NACION,
      'ficha': owner.FICHA,
      'documento': owner.DOCUMENTO,
      'representante': owner.REPRESENTA,
      'nombre_abreviado': owner.ABREVIADO,
      'nit': owner.NIT,
      'ruc': owner.RUC,
      'ciudad': owner.CIUDAD,
      'direccion': owner.DIRECCION,
      'telefono': owner.TELEFONO,
      'celular': owner.CELULAR,
      'celular1': owner.CELULAR1,
      'fec_nacimiento': owner.FEC_NACIMI,
      'fec_ingreso': owner.FEC_INGRES,
      'representante': owner.REPRESENTA,
      'contacto': owner.CONTACTO,
      'correo': owner.CORREO,
      'correo1': owner.CORREO1,
      'estado': owner.ESTADO,
      'fec_estado': owner.FEC_ESTADO,
      'central': owner.CENTRAL,
      'grupo': owner.GRUPO,
      'impuesto': owner.IMPUESTO,
      'admon_parado': owner.ADM_PARADO,
      'descuento': owner.DESCUENTO,
      'auditor': owner.USUARIO,  
      'cnt': owner.CONTROL,  
      'dcto': owner.DESCUENTO,
      'estado': estado
    }
    return JSONResponse(content=jsonable_encoder(owner_dict))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close() """

#----------------------------------------------------------------------------------------------------------------

""" @owners_router.put("/owner/{owner_id}", response_model=PropietarioUpdate, tags=["Owners"])
def update_propietario(owner_id: str, propietario: PropietarioUpdate):
    db = session()
    try:
      result = db.query(Propietarios).filter(Propietarios.CODIGO == owner_id).first()
      if not result:
        return JSONResponse(status_code=404, content={"message": "Owner not found"})
      result.NOMBRE = propietario.nombre
      result.ABREVIADO = propietario.abreviado
      result.REPRESENTA = propietario.representante
      result.RAZONSOCIA = propietario.razon_social
      result.REP_SEXO = propietario.sexo
      result.REP_ESTADO = propietario.estado_civil
      result.REP_TIPDOC = propietario.tipo_documento
      result.REP_NUMERO = propietario.numero_documento
      result.REP_NACION = propietario.nacionalidad
      result.FICHA = propietario.ficha
      result.DOCUMENTO = propietario.documento
      result.USUARIO = propietario.auditor
      result.NIT = propietario.cc
      result.RUC = propietario.ruc
      result.CIUDAD = propietario.ciudad
      result.DIRECCION = propietario.direccion
      result.CENTRAL = propietario.central
      result.TELEFONO = propietario.telefono
      result.CELULAR = propietario.celular
      result.CELULAR1 = propietario.celular1
      result.CORREO = propietario.correo
      result.CORREO1 = propietario.correo1
      result.CONTACTO = propietario.contacto
      result.GRUPO = propietario.grupo
      result.IMPUESTO = propietario.impuesto
      result.ADM_PARADO = propietario.admon_parado
      result.DESCUENTO = propietario.descuento
      if propietario.stateEdited:
        if propietario.estado == 'Activo':
          result.ESTADO = 1
        elif propietario.estado == 'Suspendido':
          result.ESTADO = 2
        elif propietario.estado == 'Retirado':
          result.ESTADO = 3
        else:
          result.ESTADO = 0
        date = datetime.now()
        result.FEC_ESTADO = date
      db.commit()
      return JSONResponse(content={"message": "Owner updated"}, status_code=200)
    except Exception as e:
      return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
      db.close() """

#----------------------------------------------------------------------------------------------------------------

@owners_router.post("/owners", response_model=PropietarioCreate)
def create_propietario(propietario: PropietarioCreate):
    db = session()
    try:
        new_propietario = Propietarios(
            CODIGO=propietario.codigo,
            NOMBRE=propietario.nombre,
            ABREVIADO=propietario.abreviado,
            REPRESENTA=propietario.representante,
            RAZONSOCIA=propietario.razon_social,
            REP_SEXO=propietario.sexo,
            REP_ESTADO=propietario.estado_civil,
            REP_TIPDOC=propietario.tipo_documento,
            REP_NUMERO=propietario.numero_documento,
            REP_NACION=propietario.nacionalidad,
            FICHA=propietario.ficha,
            DOCUMENTO=propietario.documento,
            USUARIO=propietario.auditora,
            NIT=propietario.cc,
            RUC=propietario.ruc,
            CIUDAD=propietario.ciudad,
            DIRECCION=propietario.direccion,
            CENTRAL=propietario.central,
            TELEFONO=propietario.telefono,
            CELULAR=propietario.celular,
            CELULAR1=propietario.celular1,
            CORREO=propietario.correo,
            CORREO1=propietario.correo1,
            CONTACTO=propietario.contacto,
            GRUPO=propietario.grupo,
            IMPUESTO=propietario.impuesto,
            ADM_PARADO=propietario.admon_parado,
            DESCUENTO=propietario.descuento,
            ESTADO=1 if propietario.estado == 'Activo' else 2 if propietario.estado == 'Suspendido' else 3 if propietario.estado == 'Retirado' else 0,
            CONTROL="",
            FEC_NACIMI="",
            FEC_INGRES="",
            BANCO1="",
            TIPOCTA1="",
            CUENTA1="",
            BANCO2="",
            TIPOCTA2="",
            CUENTA2="",
            FEC_CREADO="",
            USU_CREADO="",
            USU_MODIFI="",
            SEL="",
            FEC_ESTADO=datetime.now()
        )
        db.add(new_propietario)
        db.commit()
        return JSONResponse(content={"message": "Owner created"}, status_code=201)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": str(e)})
    finally:
        db.close()

#----------------------------------------------------------------------------------------------------------------

@owners_router.get("/owner-vehicles/{owner_id}", tags=["Owners"])
async def get_owners_vehicles(owner_id: int):
  db = session()
  try:
    owner = db.query(
      Vehiculos.PLACA.label('placa'),
      Vehiculos.NUMERO.label('numero'),
      Vehiculos.NOMMARCA.label('marca'),
      Vehiculos.LINEA.label('linea'),
      Vehiculos.MODELO.label('modelo'),
      Vehiculos.LICETRANSI.label('licencia_transito'),
      Conductores.NOMBRE.label('conductor'),
      Estados.NOMBRE.label('estado'),
      Centrales.NOMBRE.label('central')
    ).join(
      Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO
    ).join(
      Estados, Vehiculos.ESTADO == Estados.CODIGO
    ).join(
      Centrales, Vehiculos.CENTRAL == Centrales.CODIGO
    ).filter(
      Vehiculos.PROPI_IDEN == owner_id
    ).all()

    owner_vehicles = []
    for vehicle in owner:
      owner_vehicle = {
        'placa': vehicle.placa,
        'numero': vehicle.numero,
        'marca': vehicle.marca,
        'linea': vehicle.linea,
        'modelo': vehicle.modelo,
        'licencia_transito': vehicle.licencia_transito,
        'conductor': vehicle.conductor,
        'central': vehicle.central,
        'estado': vehicle.estado
      }
      owner_vehicles.append(owner_vehicle)

    return JSONResponse(content=jsonable_encoder(owner_vehicles))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#----------------------------------------------------------------------------------------------------------------

@owners_router.get("/owner-representative/{owner_id}", tags=["Owners"])
async def get_owner_rep(owner_id: int):
  db = session()
  try: 
    owner = db.query(
      Propietarios.NOMBRE.label('nombre_propietario'),
      Propietarios.RAZONSOCIA.label('razon_social'),
      Propietarios.REPRESENTA.label('representante'),
      Propietarios.REP_SEXO.label('sexo'),
      Propietarios.REP_ESTADO.label('estado_civil'),
      Propietarios.REP_TIPDOC.label('tipo_documento'),
      Propietarios.REP_NUMERO.label('numero_documento'),
      Propietarios.REP_NACION.label('nacionalidad'),
      Propietarios.FICHA.label('ficha'),
      Propietarios.DOCUMENTO.label('documento'),
    ).filter(
      Propietarios.CODIGO == owner_id
    ).first()

    if not owner:
      return JSONResponse(content={"error": "Owner not found"}, status_code=404)
    
    owner_rep = {
      'nombre_propietario': owner.nombre_propietario,
      'razon_social': owner.razon_social,
      'sexo': owner.sexo,
      'estado_civil': owner.estado_civil,
      'tipo_documento': owner.tipo_documento,
      'numero_documento': owner.numero_documento,
      'nacionalidad': owner.nacionalidad,
      'ficha': owner.ficha,
      'documento': owner.documento,
      'representante': owner.representante
    }

    return JSONResponse(content=jsonable_encoder(owner_rep))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()

#----------------------------------------------------------------------------------------------------------------

@owners_router.put("/owner-representative/{owner_id}", tags=["Owners"])
async def update_owner_representative(owner_id: int, propietario: RepresentantePropietario):
  db = session()
  try:
    result = db.query(Propietarios).filter(Propietarios.CODIGO == owner_id).first()
    if not result:
      return JSONResponse(status_code=404, content={"message": "Owner not found"})
    result.RAZONSOCIA = propietario.razon_social
    result.REPRESENTA = propietario.representante
    result.REP_SEXO = propietario.sexo
    result.REP_ESTADO = propietario.estado_civil
    result.REP_TIPDOC = propietario.tipo_documento
    result.REP_NUMERO = propietario.numero_documento
    result.REP_NACION = propietario.nacionalidad
    result.FICHA = propietario.ficha
    result.DOCUMENTO = propietario.documento
    db.commit()
    return JSONResponse(content={"message": "Owner representative updated"}, status_code=200)
  except Exception as e:
    return JSONResponse(content={"error": str(e)}, status_code=500)
  finally:
    db.close()
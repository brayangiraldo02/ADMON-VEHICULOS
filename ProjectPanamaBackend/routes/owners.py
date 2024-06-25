from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.propietarios import Propietarios
from models.centrales import Centrales
from models.permisosusuario import PermisosUsuario
from fastapi.encoders import jsonable_encoder

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
@owners_router.get("/owner/{owner_id}", tags=["Owners"])
async def get_owner(owner_id: int):
  db = session()
  try:
    owner = db.query(Propietarios).filter(Propietarios.CODIGO == owner_id).first()

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
      'ruc': owner.RUC,
      'telefono': owner.TELEFONO,
      'celular': owner.CELULAR,
      'representante': owner.REPRESENTA,
      'central': owner.CENTRAL,
      'auditor': owner.USUARIO,  # Ajustar si la columna auditor es diferente
      'cnt': owner.CONTROL,  # Ajustar si la columna cnt es diferente
      'dcto': owner.DESCUENTO,
      'estado': estado
    }
    return JSONResponse(content=jsonable_encoder(owner_dict))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.propietarios import Propietarios
from models.centrales import Centrales
from models.permisosusuario import PermisosUsuario
from middlewares.JWTBearer import JWTBearer
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
      Propietarios.DESCUENTO.label('dcto'),
      Propietarios.ESTADO.label('estado')
    ).join(
      PermisosUsuario, Propietarios.USUARIO == PermisosUsuario.CODIGO
    ).join(
      Centrales, Propietarios.CENTRAL == Centrales.CODIGO
    ).all()

    owners_list = [
      {
        'codigo': owner.codigo,
        'nombre_propietario': owner.nombre_propietario,
        'ruc': owner.ruc,
        'telefono': owner.telefono,
        'celular': owner.celular,
        'representante': owner.representante,
        'central': owner.central,
        'auditor': owner.auditor,
        'dcto': owner.dcto,
        'estado': owner.estado
      }
      for owner in owners
    ]
    return JSONResponse(content=jsonable_encoder(owners_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
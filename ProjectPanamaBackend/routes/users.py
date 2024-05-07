from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.dbconnection import session
from models.permisosusuario import PermisosUsuario

users_router = APIRouter()

# PRUEBA DE PETICIÓN A LA BASE DE DATOS
# ---------------------------------------------------------------------------------------------------------------
@users_router.get('/users')
async def get_users():
  db = session()
  try:
    users = db.query(PermisosUsuario.CODIGO, PermisosUsuario.NOMBRE, PermisosUsuario.GRUPO, PermisosUsuario.DIAS, PermisosUsuario.ESTADO, PermisosUsuario.FEC_ESTADO, PermisosUsuario.CAJERO, PermisosUsuario.GRUPO_CAJE, PermisosUsuario.BAJA_CONDU, PermisosUsuario.COMISION, PermisosUsuario.FOTO, PermisosUsuario.FEC_ULTCLA, PermisosUsuario.FEC_ULTING, PermisosUsuario.COD1, PermisosUsuario.OPCION01, PermisosUsuario.OPCION02, PermisosUsuario.OPCION03, PermisosUsuario.OPCION04, PermisosUsuario.OPCION05, PermisosUsuario.OPCION06, PermisosUsuario.OPCION07, PermisosUsuario.OPCION08, PermisosUsuario.OPCION09, PermisosUsuario.OPCION10, PermisosUsuario.TAREA01, PermisosUsuario.TAREA02, PermisosUsuario.TAREA03, PermisosUsuario.TAREA04, PermisosUsuario.TAREA05, PermisosUsuario.TAREA06, PermisosUsuario.TAREA07, PermisosUsuario.TAREA08, PermisosUsuario.PASSSWORD, PermisosUsuario.FEC_CREADO) \
    .all()
    users_list = [{'codigo': user.CODIGO, 'nombre': user.NOMBRE, 'grupo': user.GRUPO, 'dias': user.DIAS, 'estado': user.ESTADO, 'fec_estado': user.FEC_ESTADO, 'cajero': user.CAJERO, 'grupo_caje': user.GRUPO_CAJE, 'baja_condu': user.BAJA_CONDU, 'comision': user.COMISION, 'foto': user.FOTO, 'fec_ultcla': user.FEC_ULTCLA, 'fec_ulting': user.FEC_ULTING, 'cod1': user.COD1, 'opcion01': user.OPCION01, 'opcion02': user.OPCION02, 'opcion03': user.OPCION03, 'opcion04': user.OPCION04, 'opcion05': user.OPCION05, 'opcion06': user.OPCION06, 'opcion07': user.OPCION07, 'opcion08': user.OPCION08, 'opcion09': user.OPCION09, 'opcion10': user.OPCION10, 'tarea01': user.TAREA01, 'tarea02': user.TAREA02, 'tarea03': user.TAREA03, 'tarea04': user.TAREA04, 'tarea05': user.TAREA05, 'tarea06': user.TAREA06, 'tarea07': user.TAREA07, 'tarea08': user.TAREA08, 'password': user.PASSSWORD, 'fec_creado': user.FEC_CREADO} for user in users]
    return JSONResponse(content=jsonable_encoder(users_list))
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'error': str(e)}))
  finally:
    db.close()
# ---------------------------------------------------------------------------------------------------------------
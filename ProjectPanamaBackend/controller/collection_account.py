from fastapi.responses import JSONResponse, StreamingResponse
from config.dbconnection import session
from sqlalchemy import func, tuple_
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.centrales import Centrales
from models.estados import Estados
from models.conductores import Conductores
from models.cartera import Cartera
from fastapi.encoders import jsonable_encoder
from collections import defaultdict

from io import BytesIO
import pandas as pd

async def get_collection_accounts(companies_list: list):
  db = session()
  try:
    company_code = db.query(Propietarios.EMPRESA).filter(Propietarios.CODIGO == companies_list[0])

    collectionAccounts = db.query(
                          Propietarios.CODIGO.label('propietarios_codigo'), 
                          Propietarios.NOMBRE.label('propietarios_nombre'), 
                          Vehiculos.NUMERO.label('vehiculos_numero'), 
                          Vehiculos.PLACA.label('vehiculos_placa'), 
                          Vehiculos.CONDUCTOR.label('vehiculos_conductor'), 
                          Vehiculos.CENTRAL.label('vehiculos_central'),
                          Vehiculos.ESTADO.label('vehiculos_estado'), 
                          Estados.NOMBRE.label('estados_nombre'), 
                          Centrales.NOMBRE.label('centrales_nombre'), 
                          Conductores.CODIGO.label('conductores_codigo'),
                          Conductores.NOMBRE.label('conductores_nombre'), 
                          Conductores.CEDULA.label('conductores_cedula'),  
                          Conductores.CELULAR.label('conductores_celular'), 
                          Conductores.FEC_INGRES.label('conductores_fecingres'), 
                          Conductores.CUO_DIARIA.label('conductores_cuodiaria')
                        ).join(
                          Propietarios, Propietarios.CODIGO == Vehiculos.PROPI_IDEN
                        ).join(
                          Estados, Vehiculos.ESTADO == Estados.CODIGO
                        ).join(
                          Centrales, Vehiculos.CENTRAL == Centrales.CODIGO
                        ).join(
                          Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO
                        ).filter(
                          Vehiculos.PROPI_IDEN.in_(companies_list), 
                          Vehiculos.ESTADO.in_(['01', '19']), 
                          Vehiculos.CONDUCTOR != '',
                          Centrales.EMPRESA == company_code.scalar_subquery()
                        ).all()
    
    if not collectionAccounts:
      return JSONResponse(content=jsonable_encoder({'message': 'No collection accounts found'}), status_code=404)
    
    conductor_placa_set = {(collectionAccount.conductores_codigo, collectionAccount.vehiculos_numero) for collectionAccount in collectionAccounts}

    cartera_data = db.query(
                      Cartera.CLIENTE,
                      Cartera.UNIDAD,
                      Cartera.TIPO,
                      func.sum(Cartera.SALDO).label('SALDO')
                  ).filter(
                      tuple_(
                        Cartera.CLIENTE,
                        Cartera.UNIDAD
                      ).in_(list(conductor_placa_set))
                  ).group_by(
                    Cartera.CLIENTE,
                    Cartera.UNIDAD,
                    Cartera.TIPO
                  ).all()

    saldos_dict = defaultdict(lambda: 0)
    for row in cartera_data:
        saldos_dict[(row.CLIENTE, row.UNIDAD, row.TIPO)] = row.SALDO

    collectionAccounts_list = []
    collectionAccount_prev = None

    for collectionAccount in collectionAccounts:
      key_base = (collectionAccount.conductores_codigo, collectionAccount.vehiculos_numero)
      deu_renta = saldos_dict.get((*key_base, '10'), 0)
      fon_inscri = saldos_dict.get((*key_base, '01'), 0)
      deu_sinies = saldos_dict.get((*key_base, '11'), 0)
      deu_otras = sum(saldo for (cli, uni, tipo), saldo in saldos_dict.items() if (cli, uni) == key_base and tipo > '11')

      if deu_renta == 0:
        continue
      
      collectionAccount_temp = {
        'codigo': collectionAccount.propietarios_codigo, 
        'nombre': collectionAccount.propietarios_nombre, 
        'vehiculo_numero': collectionAccount.vehiculos_numero, 
        'vehiculo_placa': collectionAccount.vehiculos_placa, 
        'conductor': collectionAccount.vehiculos_conductor, 
        'estado': collectionAccount.estados_nombre, 
        'centrales_nombre': collectionAccount.centrales_nombre, 
        'conductores_nombre': collectionAccount.conductores_nombre, 
        'conductores_cedula': collectionAccount.conductores_cedula, 
        'conductores_celular': collectionAccount.conductores_celular, 
        'conductores_fecingres': collectionAccount.conductores_fecingres, 
        'conductores_cuodiaria': collectionAccount.conductores_cuodiaria,
        'deu_renta': deu_renta,
        'fon_inscri': fon_inscri,
        'diferencia': fon_inscri - deu_renta,
        'deu_sinies': deu_sinies,
        'deu_otras': deu_otras
      }

      if collectionAccount_prev and (collectionAccount_prev['conductor'] == collectionAccount_temp['conductor'] and collectionAccount_prev['vehiculo_numero'] == collectionAccount_temp['vehiculo_numero']):
        pass
      else:
        collectionAccount_prev = collectionAccount_temp
        collectionAccounts_list.append(collectionAccount_temp)

    return JSONResponse(content=jsonable_encoder(collectionAccounts_list), status_code=200)
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'message': str(e)}), status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

# TODO: Revisar si se puede optimizar
async def download_collection_accounts(companies_list: list):
  db = session()
  try:
    company_code = db.query(Propietarios.EMPRESA).filter(Propietarios.CODIGO == companies_list[0])

    collectionAccounts = db.query(
                          Propietarios.CODIGO.label('propietarios_codigo'), 
                          Propietarios.NOMBRE.label('propietarios_nombre'), 
                          Vehiculos.NUMERO.label('vehiculos_numero'), 
                          Vehiculos.PLACA.label('vehiculos_placa'), 
                          Vehiculos.CONDUCTOR.label('vehiculos_conductor'), 
                          Vehiculos.CENTRAL.label('vehiculos_central'),
                          Vehiculos.ESTADO.label('vehiculos_estado'), 
                          Estados.NOMBRE.label('estados_nombre'), 
                          Centrales.NOMBRE.label('centrales_nombre'), 
                          Conductores.CODIGO.label('conductores_codigo'),
                          Conductores.NOMBRE.label('conductores_nombre'), 
                          Conductores.CEDULA.label('conductores_cedula'),  
                          Conductores.CELULAR.label('conductores_celular'), 
                          Conductores.FEC_INGRES.label('conductores_fecingres'), 
                          Conductores.CUO_DIARIA.label('conductores_cuodiaria')
                        ).join(
                          Propietarios, Propietarios.CODIGO == Vehiculos.PROPI_IDEN
                        ).join(
                          Estados, Vehiculos.ESTADO == Estados.CODIGO
                        ).join(
                          Centrales, Vehiculos.CENTRAL == Centrales.CODIGO
                        ).join(
                          Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO
                        ).filter(
                          Vehiculos.PROPI_IDEN.in_(companies_list), 
                          Vehiculos.ESTADO.in_(['01', '19']), 
                          Vehiculos.CONDUCTOR != '',
                          Centrales.EMPRESA == company_code.scalar_subquery()
                        ).all()
    
    if not collectionAccounts:
      return JSONResponse(content=jsonable_encoder({'message': 'No collection accounts found'}), status_code=404)
    
    conductor_placa_set = {(collectionAccount.conductores_codigo, collectionAccount.vehiculos_numero) for collectionAccount in collectionAccounts}

    cartera_data = db.query(
                      Cartera.CLIENTE,
                      Cartera.UNIDAD,
                      Cartera.TIPO,
                      func.sum(Cartera.SALDO).label('SALDO')
                  ).filter(
                      tuple_(
                        Cartera.CLIENTE,
                        Cartera.UNIDAD
                      ).in_(list(conductor_placa_set))
                  ).group_by(
                    Cartera.CLIENTE,
                    Cartera.UNIDAD,
                    Cartera.TIPO
                  ).all()

    saldos_dict = defaultdict(lambda: 0)
    for row in cartera_data:
        saldos_dict[(row.CLIENTE, row.UNIDAD, row.TIPO)] = row.SALDO

    collectionAccounts_list = []
    collectionAccount_prev = None

    for collectionAccount in collectionAccounts:
      key_base = (collectionAccount.conductores_codigo, collectionAccount.vehiculos_numero)
      deu_renta = saldos_dict.get((*key_base, '10'), 0)
      fon_inscri = saldos_dict.get((*key_base, '01'), 0)
      deu_sinies = saldos_dict.get((*key_base, '11'), 0)
      deu_otras = sum(saldo for (cli, uni, tipo), saldo in saldos_dict.items() if (cli, uni) == key_base and tipo > '11')

      if deu_renta == 0:
        continue
      
      collectionAccount_temp = {
        'codigo': collectionAccount.propietarios_codigo, 
        'nombre': collectionAccount.propietarios_nombre, 
        'vehiculo_numero': collectionAccount.vehiculos_numero, 
        'vehiculo_placa': collectionAccount.vehiculos_placa, 
        'conductor': collectionAccount.vehiculos_conductor, 
        'estado': collectionAccount.estados_nombre, 
        'centrales_nombre': collectionAccount.centrales_nombre, 
        'conductores_nombre': collectionAccount.conductores_nombre, 
        'conductores_cedula': collectionAccount.conductores_cedula, 
        'conductores_celular': collectionAccount.conductores_celular, 
        'conductores_fecingres': collectionAccount.conductores_fecingres, 
        'conductores_cuodiaria': collectionAccount.conductores_cuodiaria,
        'deu_renta': deu_renta,
        'fon_inscri': fon_inscri,
        'diferencia': fon_inscri - deu_renta,
        'deu_sinies': deu_sinies,
        'deu_otras': deu_otras
      }

      if collectionAccount_prev and (collectionAccount_prev['conductor'] == collectionAccount_temp['conductor'] and collectionAccount_prev['vehiculo_numero'] == collectionAccount_temp['vehiculo_numero']):
        pass
      else:
        collectionAccount_prev = collectionAccount_temp
        collectionAccounts_list.append(collectionAccount_temp)
    
    df = pd.DataFrame(collectionAccounts_list)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=collection_accounts.xlsx"})
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'message': str(e)}), status_code=500)
  finally:
    db.close()
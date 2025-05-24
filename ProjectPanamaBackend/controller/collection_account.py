from fastapi.responses import JSONResponse
from config.dbconnection import session
from sqlalchemy import func
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.centrales import Centrales
from models.estados import Estados
from models.conductores import Conductores
from models.cartera import Cartera
from fastapi.encoders import jsonable_encoder

async def get_collection_accounts(companies_list: list):
  db = session()
  try:
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
                          Conductores.TELEFONO.label('conductores_telefono'), 
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
                          Vehiculos.CONDUCTOR != ''
                        ).all()
    
    if not collectionAccounts:
      return JSONResponse(content=jsonable_encoder({'message': 'No collection accounts found'}), status_code=404)
    
    collectionAccounts_list = []

    for collectionAccount in collectionAccounts:
      deu_renta = db.query(
                    func.sum(Cartera.SALDO).label('SALDO')
                  ).filter(
                    Cartera.CLIENTE == collectionAccount.conductores_codigo,
                    Cartera.TIPO == '10',
                    Cartera.UNIDAD == collectionAccount.vehiculos_placa
                  ).all()
      
      fon_inscri = db.query(
                    func.sum(Cartera.SALDO).label('SALDO')
                  ).filter(
                    Cartera.CLIENTE == collectionAccount.conductores_codigo,
                    Cartera.TIPO == '01',
                    Cartera.UNIDAD == collectionAccount.vehiculos_placa
                  ).all()
      
      deu_sinies = db.query(
                    func.sum(Cartera.SALDO).label('SALDO')
                  ).filter(
                    Cartera.CLIENTE == collectionAccount.conductores_codigo,
                    Cartera.TIPO == '11',
                    Cartera.UNIDAD == collectionAccount.vehiculos_placa
                  ).all()
      
      deu_otras = db.query(
                    func.sum(Cartera.SALDO).label('SALDO')
                  ).filter(
                    Cartera.CLIENTE == collectionAccount.conductores_codigo,
                    Cartera.TIPO > '11',
                    Cartera.UNIDAD == collectionAccount.vehiculos_placa
                  ).all()
      
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
        'conductores_telefono': collectionAccount.conductores_telefono, 
        'conductores_celular': collectionAccount.conductores_celular, 
        'conductores_fecingres': collectionAccount.conductores_fecingres, 
        'conductores_cuodiaria': collectionAccount.conductores_cuodiaria,
        'deu_renta': deu_renta[0][0] if deu_renta[0][0] else 0,
        'fon_inscri': fon_inscri[0][0] if fon_inscri[0][0] else 0,
        'diferencia': deu_renta[0][0] - fon_inscri[0][0] if deu_renta[0][0] and fon_inscri[0][0] else 0,
        'deu_sinies': deu_sinies[0][0] if deu_sinies[0][0] else 0,
        'deu_otras': deu_otras[0][0] if deu_otras[0][0] else 0
      }

      collectionAccounts_list.append(collectionAccount_temp)

    return JSONResponse(content=jsonable_encoder(collectionAccounts_list), status_code=200)
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'message': str(e)}), status_code=500)
  finally:
    db.close()
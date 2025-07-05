from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.cuentagastos import CuentaGastos
from fastapi.encoders import jsonable_encoder

async def get_expenseAccount():
  db = session()
  try:
    expenseAccounts = db.query(CuentaGastos.CODIGO, CuentaGastos.NOMBRE).all()
    expenseAccounts = [{'codigo': expenseAccount.CODIGO, 'nombre': expenseAccount.NOMBRE} for expenseAccount in expenseAccounts]
    return JSONResponse(content=jsonable_encoder(expenseAccounts), status_code=200)
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'error': str(e)}), status_code=500)
  finally:
    db.close()
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.infoempresas import InfoEmpresas
from fastapi.encoders import jsonable_encoder

async def get_info_companies(company_code: str):
  db = session()
  try:
    company = db.query(InfoEmpresas.NOMBRE, InfoEmpresas.NIT, InfoEmpresas.DIRECCION, InfoEmpresas.CIUDAD, InfoEmpresas.TELEFONO, InfoEmpresas.CORREO, InfoEmpresas.LOGO) \
      .filter(InfoEmpresas.ID == company_code) \
      .first()
    
    if company:
      company_data = {
        "name": company.NOMBRE,
        "nit": company.NIT,
        "direction": company.DIRECCION,
        "city": company.CIUDAD,
        "phone": company.TELEFONO,
        "email": company.CORREO,
        "logo": company.LOGO
      }
      return JSONResponse(content=jsonable_encoder(company_data))
    
    return JSONResponse(
      status_code=404,
      content={"message": "Company not found"}
    )

  except FileNotFoundError:
    return JSONResponse(
      status_code=404,
      content={"message": "File not found"}
    )
  
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(e)}"}
    )
  
  finally:
    db.close()
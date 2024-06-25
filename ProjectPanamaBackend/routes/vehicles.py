from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.vehiculos import Vehiculos
from models.estados import Estados
from fastapi.encoders import jsonable_encoder

vehicles_router = APIRouter()

@vehicles_router.get("/vehicles", tags=["Vehicles"])
async def get_vehicles():
  db = session()
  try:
    vehicles = db.query(
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.MODELO.label('vehiculo_modelo'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.PERMISONRO.label('vehiculo_permiso_nro'),
            Vehiculos.MOTORNRO.label('vehiculo_motor'),
            Vehiculos.CHASISNRO.label('vehiculo_chasis'),
            Vehiculos.FEC_MATRIC.label('vehiculo_fec_matricula'),
            Vehiculos.EMPRESA.label('vehiculo_empresa'),
            Vehiculos.CONDUCTOR.label('vehiculo_conductor'),
            Estados.NOMBRE.label('vehiculo_estado'),
            Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
            Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
            Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
            Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
            Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
        )   .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
            .all()

    vehicles_list = [
      {
        'vehiculo_numero': vehicle.vehiculo_numero,
        'vehiculo_placa': vehicle.vehiculo_placa,
        'vehiculo_modelo': vehicle.vehiculo_modelo,
        'vehiculo_nro_cupo': vehicle.vehiculo_nro_cupo,
        'vehiculo_permiso_nro': vehicle.vehiculo_permiso_nro,
        'vehiculo_motor': vehicle.vehiculo_motor,
        'vehiculo_chasis': vehicle.vehiculo_chasis,
        'vehiculo_fec_matricula': vehicle.vehiculo_matricula,
        'vehiculo_empresa': vehicle.vehiculo_empresa,
        'vehiculo_conductor': vehicle.vehiculo_conductor,
        'vehiculo_estado': vehicle.vehiculo_estado,
        'vehiculo_cuota_diaria': vehicle.vehiculo_cuota_diaria,
        'vehiculo_nro_Ctas': vehicle.vehiculo_nro_Ctas,
        'vehiculo_panapass': vehicle.vehiculo_panapass,
        'vehiculo_panapass_pwd': vehicle.vehiculo_panapass_pwd,
        'vehiculo_saldo_panapass': vehicle.vehiculo_saldo_panapass
      }
      for vehicle in vehicles
    ]
    return JSONResponse(content=jsonable_encoder(vehicles_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
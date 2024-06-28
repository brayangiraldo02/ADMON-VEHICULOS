from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.vehiculos import Vehiculos
from models.estados import Estados
from models.conductores import Conductores
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
            Conductores.NOMBRE.label('vehiculo_conductor'),
            Estados.NOMBRE.label('vehiculo_estado'),
            Vehiculos.CUO_DIARIA.label('vehiculo_cuota_diaria'),
            Vehiculos.NROENTREGA.label('vehiculo_nro_Ctas'),
            Vehiculos.PANAPASSNU.label('vehiculo_panapass'),
            Vehiculos.PANAPASSPW.label('vehiculo_panapass_pwd'),
            Vehiculos.SDO_PANAPA.label('vehiculo_saldo_panapass'),
        )   .join(Estados, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Conductores, Conductores.CODIGO == Vehiculos.CONDUCTOR) \
            .all()

    vehicles_list = [
      {
        'unidad': vehicle.vehiculo_numero,
        'placa': vehicle.vehiculo_placa,
        'modelo': vehicle.vehiculo_modelo,
        'nro_cupo': vehicle.vehiculo_nro_cupo,
        'permiso': vehicle.vehiculo_permiso_nro,
        'motor': vehicle.vehiculo_motor,
        'chasis': vehicle.vehiculo_chasis,
        'matricula': vehicle.vehiculo_fec_matricula,
        'empresa': vehicle.vehiculo_empresa,
        'conductor': vehicle.vehiculo_conductor,
        'estado': vehicle.vehiculo_estado,
        'vlr_cta': vehicle.vehiculo_cuota_diaria,
        'nro_ctas': vehicle.vehiculo_nro_Ctas,
        'panapass': vehicle.vehiculo_panapass,
        'clave': vehicle.vehiculo_panapass_pwd,
        'saldo': vehicle.vehiculo_saldo_panapass
      }
      for vehicle in vehicles
    ]
    return JSONResponse(content=jsonable_encoder(vehicles_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
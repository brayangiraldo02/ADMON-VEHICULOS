from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.conductores import Conductores
from models.vehiculos import Vehiculos
from models.marcas import Marcas
from models.propietarios import Propietarios
from models.estados import Estados
from models.centrales import Centrales
from models.estadocivil import EstadoCivil
from schemas.operations import *
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from utils.docx import *
from utils.pdf import *
from fastapi import BackgroundTasks
import tempfile
import os
from docxtpl import DocxTemplate
import pytz
from num2words import num2words
import locale

#! Verificar si las importaciones son necesarias
from sqlalchemy.orm import aliased
from middlewares.JWTBearer import JWTBearer
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

async def get_vehicle_operation(vehicle_number: str):
  db = session()
  try:
    vehicle_operations = db.query(
      Marcas.NOMBRE.label('MARCA'), Vehiculos.PLACA, Vehiculos.NRO_CUPO,
      Vehiculos.NROENTREGA, Vehiculos.CUO_DIARIA, Vehiculos.ESTADO, 
      Estados.NOMBRE.label('NOMBRE_ESTADO'), Vehiculos.PROPI_IDEN, 
      Propietarios.NOMBRE.label('NOMBRE_PROPI'), Vehiculos.CONDUCTOR,
      Vehiculos.CON_CUPO, Vehiculos.FEC_ESTADO
    ).join(
      Vehiculos, Vehiculos.MARCA == Marcas.CODIGO
    ).join(
      Estados, Vehiculos.ESTADO == Estados.CODIGO
    ).join(
      Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO
    ).filter(
      Vehiculos.NUMERO == vehicle_number
    ).first()

    if not vehicle_operations:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    vehicle = {
      'numero': vehicle_number,
      'marca': vehicle_operations.MARCA,
      'placa': vehicle_operations.PLACA,
      'cupo': vehicle_operations.NRO_CUPO,
      'nro_entrega': vehicle_operations.NROENTREGA,
      'cuota_diaria': vehicle_operations.CUO_DIARIA,
      'estado': vehicle_operations.ESTADO + ' - ' + vehicle_operations.NOMBRE_ESTADO,
      'propietario': vehicle_operations.PROPI_IDEN + ' - ' + vehicle_operations.NOMBRE_PROPI,
      'conductor': vehicle_operations.CONDUCTOR,
      'con_cupo': vehicle_operations.CON_CUPO,
      'fecha_estado': vehicle_operations.FEC_ESTADO
    }

    return JSONResponse(content=jsonable_encoder(vehicle), status_code=200)
  
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def get_driver_operation(driver_number: str):
  db = session()
  try:
    driver_operations = db.query(
      Conductores.NOMBRE, Conductores.CEDULA, Conductores.TELEFONO, 
      Conductores.CELULAR, Conductores.DIRECCION, Conductores.LICEN_NRO, 
      Conductores.LICEN_VCE, Conductores.UND_NRO, Conductores.ESTADO
    ).filter(
      Conductores.CODIGO == driver_number
    ).first()

    if not driver_operations:
      return JSONResponse(content={"message": "Driver not found"}, status_code=404)
    
    driver = {
      'codigo': driver_number,
      'nombre': driver_operations.NOMBRE,
      'cedula': driver_operations.CEDULA,
      'telefono': driver_operations.TELEFONO + ' | ' + driver_operations.CELULAR,
      'direccion': driver_operations.DIRECCION,
      'licencia_numero': driver_operations.LICEN_NRO,
      'licencia_vencimiento': driver_operations.LICEN_VCE,
      'vehiculo': driver_operations.UND_NRO,
      'estado': driver_operations.ESTADO
    }

    return JSONResponse(content=jsonable_encoder(driver), status_code=200)
  
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def delivery_vehicle_driver(data: DeliveryVehicleDriver):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.vehicle_number).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    driver = db.query(Conductores).filter(Conductores.CODIGO == data.driver_number).first()
    if not driver:
      return JSONResponse(content={"message": "Driver not found"}, status_code=404)
    
    if(driver.ESTADO != '1' and 
       driver.UND_NRO != '' and 
       vehicle.ESTADO != '06' and 
       vehicle.CON_CUPO != 1 and
       vehicle.CONDUCTOR != ''):
      return JSONResponse(content={"message": "Driver already has a vehicle assigned"}, status_code=400)
    
    vehicle.CONDUCTOR = driver.CODIGO
    vehicle.ESTADO = '01'
    vehicle.FEC_ESTADO = data.delivery_date
    driver.UND_NRO = data.vehicle_number
    driver.CUO_DIARIA = vehicle.CUO_DIARIA

    db.commit()

    return JSONResponse(content={"message": "Vehicle delivered successfully"}, status_code=200)
  
  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def vehicle_delivery_info(vehicle_number: str):
  db = session()
  try:
    vehicle_info = db.query(
      Vehiculos.NOMMARCA, Vehiculos.PLACA, Vehiculos.NRO_CUPO,
      Vehiculos.NROENTREGA, Vehiculos.CUO_DIARIA, Vehiculos.VLR_DEPOSI,
      Vehiculos.ESTADO, Estados.NOMBRE.label('NOMBRE_ESTADO'), Vehiculos.FEC_ESTADO,
      Vehiculos.CON_CUPO, Vehiculos.CONDUCTOR, Conductores.NOMBRE.label('NOMBRE_CONDUCTOR'),
      Conductores.CEDULA, Conductores.TELEFONO, Conductores.CELULAR, Conductores.DIRECCION,
      Propietarios.NOMBRE.label('PROPIETARIO_NOMBRE'), Centrales.NOMBRE.label('CENTRAL_NOMBRE')
    ).join(
      Estados, Vehiculos.ESTADO == Estados.CODIGO
    ).join(
      Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO
    ).join(
      Centrales, Vehiculos.CENTRAL == Centrales.CODIGO
    ).join(
      Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO
    ).filter(
      Vehiculos.NUMERO == vehicle_number,
      Vehiculos.EMPRESA == Centrales.EMPRESA
    ).first()

    if not vehicle_info:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)

    delivery_info = {
      'numero': vehicle_number,
      'marca': vehicle_info.NOMMARCA,
      'placa': vehicle_info.PLACA,
      'cupo': vehicle_info.NRO_CUPO,
      'central': vehicle_info.CENTRAL_NOMBRE,
      'propietario_nombre': vehicle_info.PROPIETARIO_NOMBRE,
      'nro_entrega': vehicle_info.NROENTREGA,
      'cuota_diaria': vehicle_info.CUO_DIARIA,
      'valor_deposito': vehicle_info.VLR_DEPOSI,
      'estado': vehicle_info.ESTADO + ' - ' + vehicle_info.NOMBRE_ESTADO,
      'con_cupo': 'Con Cupo' if vehicle_info.CON_CUPO == '1' else '',
      'conductor_codigo': vehicle_info.CONDUCTOR,
      'conductor_nombre': vehicle_info.NOMBRE_CONDUCTOR,
      'conductor_cedula': vehicle_info.CEDULA,
      'conductor_celular': vehicle_info.TELEFONO,
      'conductor_direccion': vehicle_info.DIRECCION,
      'fecha_contrato': vehicle_info.FEC_ESTADO.strftime('%d/%m/%Y') if vehicle_info.FEC_ESTADO else None
    }

    return JSONResponse(content=jsonable_encoder(delivery_info), status_code=200)
  
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
docx_template_path = os.path.join(base_dir, 'documents', 'ContratoOriginal.docx')

locale.setlocale(locale.LC_TIME, "es_ES")

async def generate_contract(vehicle_number: str):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_number).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    driver = db.query(Conductores).filter(Conductores.CODIGO == vehicle.CONDUCTOR).first()
    if not driver:
      return JSONResponse(content={"message": "Driver not found"}, status_code=404)
    
    owner = db.query(Propietarios).filter(Propietarios.CODIGO == vehicle.PROPI_IDEN).first()
    if not owner:
      return JSONResponse(content={"message": "Owner not found"}, status_code=404)
    
    central = db.query(Centrales).filter(Centrales.CODIGO == vehicle.CENTRAL, Centrales.EMPRESA == Vehiculos.EMPRESA).first()
    if not central:
      return JSONResponse(content={"message": "Central not found"}, status_code=404)
    
    civil_status = db.query(EstadoCivil).filter(EstadoCivil.CODIGO == driver.ESTA_CIVIL).first()
    if not civil_status:
      return JSONResponse(content={"message": "Civil status not found"}, status_code=404)
    
    zMsg = num2words(float(vehicle.NROENTREGA), lang='es')

    xMsg = "{:,.2f}".format(vehicle.CTA_RENTA + vehicle.CTA_SINIES)
    xMsg1 = "{:,.2f}".format(vehicle.CTA_RENTA)
    xMsg2 = "{:,.2f}".format(vehicle.CTA_SINIES)

    wMsg = num2words(float(vehicle.CTA_RENTA + vehicle.CTA_SINIES), lang='es')
    wMsg1 = num2words(float(vehicle.CTA_RENTA), lang='es')
    wMsg2 = num2words(float(vehicle.CTA_SINIES), lang='es')

    vDepGar = vehicle.VLR_DEPOSI
    wDepGar = num2words(int(vDepGar), lang='es')
    
    if vehicle.NUEVOUSADO == '1':
      wTipAut = 'Nuevo'
    elif vehicle.NUEVOUSADO == '2':
      wTipAut = 'Usado'
    else:
      wTipAut = '**********'

    if vehicle.CON_CUPO == '1':
      Mensaje1 = 'El plan de financiamiento implícito en este contrato otorga el beneficio al ARRENDATARIO que en su favor se haga la '
      Mensaje2 = 'transferencia del Certificado de operación, siempre y cuando éste cumpla con todos los presupuestos para el ' 
      Mensaje3 = 'traspaso por  tanto,  no debe entender el ARRENDATARIO que con el pago de cuotas de financiamientos o repuestos se '
      Mensaje4 = 'computan abonos al valor que representa el certificado de operación, dado a que,  este beneficio es otorgado por la '
      Mensaje5 = 'naturaleza del contrato solo en casos de cumplimiento total y efectivo del mismo.'
    else:
      Mensaje1, Mensaje2, Mensaje3, Mensaje4, Mensaje5 = '', '', '', '', ''

    panama_timezone = pytz.timezone('America/Panama')
    now_in_panama = datetime.now(panama_timezone)
    year = now_in_panama.strftime("%Y")
    month = now_in_panama.strftime("%m")
    day = now_in_panama.strftime("%d")
    n_year = num2words(int(year), lang='es')
    n_month = now_in_panama.strftime("%B")
    n_day = num2words(int(day), lang='es')
    
    data = {
      'Representa': owner.REPRESENTA,
      'Rep_sexo': owner.REP_SEXO,
      'Rep_estado': owner.REP_ESTADO,
      'Rep_tipdoc': owner.REP_TIPDOC,
      'Rep_numero': owner.REP_NUMERO,
      'Empresa': owner.RAZONSOCIA,
      'Ficha': owner.FICHA,
      'Documento': owner.DOCUMENTO,
      #'Rep_admon': owner.REP_ADMON, #! Is not in the database
      'LimNorte': central.LIMI_NORTE,
      'LimSur': central.LIMI_SUR,
      'LimEste': central.LIMI_ESTE,
      'LimOeste': central.LIMI_OESTE,
      'Operador': driver.CODIGO,
      'Con_sexo': 'varón' if driver.SEXO == '1' else 'mujer',
      'Con_estado': civil_status.NOMBRE.lower(),
      'Nombre': driver.NOMBRE,
      'Cedula': str(driver.NIT),
      'Codigo': driver.CODIGO,
      'Direccion': driver.DIRECCION,
      'Telefono': driver.TELEFONO + ' ' + driver.CELULAR,
      'NomRecomen': driver.RECOME_NOM,
      'CedRecom': driver.RECOME_CED,
      'laCuota': zMsg,
      'Cuotas': str(vehicle.NROENTREGA),
      'Puertas': vehicle.PUERTAS,
      'Capacidad': vehicle.CAPACIDAD,
      'Marca': vehicle.NOMMARCA,
      'Linea': vehicle.LINEA,
      'Ano': vehicle.MODELO,
      'Chasis': vehicle.CHASISNRO,
      'Motor': vehicle.MOTORNRO,
      'PanaPass': vehicle.PANAPASSNU,
      'laSuma': wMsg,
      'laSuma1': wMsg1,
      'laSuma2': wMsg2,
      'elValor': xMsg,
      'elValor1': xMsg1,
      'elValor2': xMsg2,
      'Unidad': vehicle.NUMERO,
      'Placa': vehicle.PLACA,
      'NroCupo': vehicle.NRO_CUPO,
      'ConCupo': 'Con Cupo' if vehicle.CON_CUPO == '1' else 'Sin certificado de operación',
      'wDepGar': wDepGar,
      'vDepGar': vDepGar,
      'wTipAut': wTipAut,
      'Mensaje1': Mensaje1,
      'Mensaje2': Mensaje2,
      'Mensaje3': Mensaje3,
      'Mensaje4': Mensaje4,
      'Mensaje5': Mensaje5,
      'fAno': year,
      'fMes': month,
      'fDia': day,
      'nAno': n_year,
      'nMes': n_month,
      'nDia': n_day,
    }
    
    current_docx_path = docx_template_path

    temp_docx_fd, temp_docx_path = tempfile.mkstemp(suffix=".docx")
    os.close(temp_docx_fd)

    #doc = Document(current_docx_path)
    doc = DocxTemplate(current_docx_path)
    doc.render(data)

    #replace_text_in_docx_robust(doc, data) ##
    #insert_page_break_before_paragraph(doc, "UNIDAD N°")
    doc.save(temp_docx_path)

    docx2pdf(temp_docx_path)

    temp_pdf_path = temp_docx_path.replace('.docx', '.pdf')
    if not os.path.exists(temp_pdf_path):
      raise FileNotFoundError(f"El archivo PDF no se generó correctamente: {temp_pdf_path}")

    os.remove(temp_docx_path)

    background_task = BackgroundTasks()
    background_task.add_task(os.remove, temp_pdf_path)

    return FileResponse(
        path=temp_pdf_path,
        filename="contrato.pdf",
        media_type="application/pdf",
        background=background_task
    )

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.conductores import Conductores
from models.vehiculos import Vehiculos
from models.marcas import Marcas
from models.propietarios import Propietarios
from models.estados import Estados
from models.centrales import Centrales
from models.estadocivil import EstadoCivil
from models.cartera import Cartera
from models.patios import Patios
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
from utils.text import clean_text
from sqlalchemy import func

path_10  = "C:/Users/Ximena/Desktop/dropbox-alfasoft/Integracion"
path_58  = "/home/admin/dropbox-alfasoft/Integracion (1)"

async def get_vehicle_operation(vehicle_number: str):
  db = session()
  try:
    vehicle_operations = db.query(
      Marcas.NOMBRE.label('MARCA'), Vehiculos.PLACA, Vehiculos.NRO_CUPO,
      Vehiculos.NROENTREGA, Vehiculos.CUO_DIARIA, Vehiculos.ESTADO, 
      Estados.NOMBRE.label('NOMBRE_ESTADO'), Vehiculos.PROPI_IDEN, 
      Propietarios.NOMBRE.label('NOMBRE_PROPI'), Vehiculos.CONDUCTOR,
      Vehiculos.CON_CUPO, Vehiculos.FEC_ESTADO, Vehiculos.EMPRESA
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

    outstanding_balance = db.query(
      func.sum(Cartera.SALDO).label('outstanding balance')
    ).filter(
      Cartera.EMPRESA == vehicle_operations.EMPRESA,
      Cartera.UNIDAD == vehicle_number,
      Cartera.CLIENTE == vehicle_operations.CONDUCTOR,
      Cartera.TIPO == '11',
    ).scalar()

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
      'fecha_estado': vehicle_operations.FEC_ESTADO,
      'outstanding_balance': outstanding_balance if outstanding_balance else 0
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
      Conductores.LICEN_VCE, Conductores.UND_NRO, Conductores.UND_PRE, Conductores.ESTADO
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
      'vehiculo_original': driver_operations.UND_PRE,
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

    base_path = None

    if vehicle.EMPRESA == '10':
      base_path = path_10
    elif vehicle.EMPRESA == '58':
      base_path = path_58

    if base_path:
      panama_timezone = pytz.timezone('America/Panama')
      now_in_panama = datetime.now(panama_timezone)

      text_file = os.path.join(base_path, f"entregavehiculo_{vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{vehicle.NUMERO},,{driver.CODIGO},,,,,,{now_in_panama.strftime('%Y-%m-%d')},{clean_text(data.user)}")

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
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_number).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    driver = db.query(Conductores).filter(Conductores.CODIGO == vehicle.CONDUCTOR).first()
    if not driver:
      return JSONResponse(content={"message": "Driver not found"}, status_code=404)
    
    owner = db.query(Propietarios).filter(Propietarios.CODIGO == vehicle.PROPI_IDEN).first()
    if not owner:
      return JSONResponse(content={"message": "Owner not found"}, status_code=404)
    
    central = db.query(Centrales).filter(Centrales.CODIGO == vehicle.CENTRAL, Centrales.EMPRESA == vehicle.EMPRESA).first()
    if not central:
      return JSONResponse(content={"message": "Central not found"}, status_code=404)
    
    state = db.query(Estados).filter(Estados.CODIGO == vehicle.ESTADO, Estados.EMPRESA == vehicle.EMPRESA).first()
    
    wReg = 0
    # Verificar datos del vehiculo
    if vehicle.FEC_CONTRA is None or vehicle.FEC_CONTRA == '' or vehicle.FEC_CONTRA == '0000-00-00':
      wReg = 1
      message = 'VEHICULO no Tiene Fecha de Contrato'
    elif float(vehicle.NROENTREGA) == 0:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Cuotas'
    elif Vehiculos.VLR_DEPOSI == 0:
      wReg = 1
      message = 'VEHICULO no Tiene Valor del Deposito'
    elif vehicle.NUEVOUSADO == '0':
      wReg = 1
      message = 'VEHICULO sin Seleccion de Nuevo o Usado'
    elif not vehicle.PUERTAS:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Puertas'
    elif not vehicle.CAPACIDAD:
      wReg = 1
      message = 'VEHICULO no Tiene Capacidad de Pasajeros'
    elif not vehicle.NOMMARCA:
      wReg = 1
      message = 'VEHICULO no Tiene Nombre de Marca'
    elif not vehicle.LINEA:
      wReg = 1
      message = 'VEHICULO no Tiene Nombre de Linea'
    elif not vehicle.MODELO:
      wReg = 1
      message = 'VEHICULO no Tiene Año'
    elif not vehicle.CHASISNRO:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Chasis'
    elif not vehicle.MOTORNRO:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Motor'
    elif (vehicle.CTA_RENTA + vehicle.CTA_SINIES) == 0:
      wReg = 1
      message = 'VEHICULO no Tiene Valor de la Cuota'
    elif not vehicle.NUMERO:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Unidad'
    elif not vehicle.PLACA:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Placa'
    elif vehicle.CON_CUPO == '0':
      wReg = 1
      message = 'VEHICULO no Tiene marca Con Cupo o Sin Cupo'
    # Verificar datos del propietario
    elif not owner.REPRESENTA:
      wReg = 1
      message = 'PROPIETARIO no Tiene Representante'
    elif not owner.REP_SEXO:
      wReg = 1
      message = 'No definio Sexo del REPRESENTANTE'
    elif not owner.REP_ESTADO:
      wReg = 1
      message = 'No definio Estado Civil del REPRESENTANTE'
    elif not owner.REP_TIPDOC:
      wReg = 1
      message = 'No definio Tipo de Documento del REPRESENTANTE'
    elif not owner.REP_NUMERO:
      wReg = 1
      message = 'No definio Numero de Documento del REPRESENTANTE'
    elif not owner.RAZONSOCIA:
      wReg = 1
      message = 'EMPRESA no Tiene Razon Social'
    elif not owner.FICHA:
      wReg = 1
      message = 'EMPRESA no Tiene Ficha Inscripcion'
    elif not owner.DOCUMENTO:
      wReg = 1
      message = 'EMPRESA no Tiene Documento de Inscripcion'
    elif not owner.REP_ADMON:
      wReg = 1
      message = 'Empresa no Tiene Empresa Administradora'
    # Verificar datos de la central
    elif not central.LIMI_NORTE:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Norte'
    elif not central.LIMI_SUR:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Sur'
    elif not central.LIMI_ESTE:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Este'
    elif not central.LIMI_OESTE:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Oeste'
    # Verificar datos del conductor
    elif not driver.NOMBRE:
      wReg = 1
      message = 'CONDUCTOR no Tiene Nombre'
    elif driver.SEXO == '0':
      wReg = 1
      message = 'No definio Sexo del CONDUCTOR'
    elif not driver.ESTA_CIVIL:
      wReg = 1
      message = 'No definio Estado Civil del CONDUCTOR'
    elif not driver.NIT:
      wReg = 1
      message = 'CONDUCTOR no Tiene No. de Cedula'
    elif not driver.DIRECCION:
      wReg = 1
      message = 'CONDUCTOR no Tiene Direccion'
    elif not driver.TELEFONO and not driver.CELULAR:
      wReg = 1
      message = 'CONDUCTOR no Tiene Telefono o Celular'
    elif not driver.RECOME_NOM:
      wReg = 1
      message = 'CONDUCTOR no Tiene RECOMENDADO'
    elif not driver.RECOME_CED:
      wReg = 1
      message = 'RECOMENDADO no Tiene No. de Cedula'

    delivery_info = {
      'numero': vehicle_number,
      'marca': vehicle.NOMMARCA,
      'placa': vehicle.PLACA,
      'cupo': vehicle.NRO_CUPO,
      'central': central.NOMBRE,
      'propietario_nombre': owner.NOMBRE,
      'nro_entrega': vehicle.NROENTREGA,
      'cuota_diaria': vehicle.CUO_DIARIA,
      'valor_deposito': vehicle.VLR_DEPOSI,
      'estado': state.NOMBRE,
      'con_cupo': 'Con Cupo' if vehicle.CON_CUPO == '1' else '',
      'conductor_codigo': vehicle.CONDUCTOR,
      'conductor_nombre': driver.NOMBRE,
      'conductor_cedula': driver.CEDULA,
      'conductor_celular': driver.TELEFONO,
      'conductor_direccion': driver.DIRECCION,
      'fecha_contrato': vehicle.FEC_CONTRA.strftime('%d/%m/%Y') if vehicle.FEC_CONTRA and hasattr(vehicle.FEC_CONTRA, 'strftime') else None,
      'permitido': wReg,
      'mensaje': message if wReg == 1 else '',
    }

    return JSONResponse(content=jsonable_encoder(delivery_info), status_code=200)
  
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
docx_template_path = os.path.join(base_dir, 'documents', 'ContratoOriginal.docx')

locale.setlocale(locale.LC_TIME, "es_ES.utf8")

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
    
    wReg = 0
    # Verificar datos del vehiculo
    if float(vehicle.NROENTREGA) == 0:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Cuotas'
    elif Vehiculos.VLR_DEPOSI == 0:
      wReg = 1
      message = 'VEHICULO no Tiene Valor del Deposito'
    elif vehicle.NUEVOUSADO == '0':
      wReg = 1
      message = 'VEHICULO sin Seleccion de Nuevo o Usado'
    elif not vehicle.PUERTAS:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Puertas'
    elif not vehicle.CAPACIDAD:
      wReg = 1
      message = 'VEHICULO no Tiene Capacidad de Pasajeros'
    elif not vehicle.NOMMARCA:
      wReg = 1
      message = 'VEHICULO no Tiene Nombre de Marca'
    elif not vehicle.LINEA:
      wReg = 1
      message = 'VEHICULO no Tiene Nombre de Linea'
    elif not vehicle.MODELO:
      wReg = 1
      message = 'VEHICULO no Tiene Año'
    elif not vehicle.CHASISNRO:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Chasis'
    elif not vehicle.MOTORNRO:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Motor'
    elif (vehicle.CTA_RENTA + vehicle.CTA_SINIES) == 0:
      wReg = 1
      message = 'VEHICULO no Tiene Valor de la Cuota'
    elif not vehicle.NUMERO:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Unidad'
    elif not vehicle.PLACA:
      wReg = 1
      message = 'VEHICULO no Tiene Nº de Placa'
    elif vehicle.CON_CUPO == '0':
      wReg = 1
      message = 'VEHICULO no Tiene marca Con Cupo o Sin Cupo'
    # Verificar datos del propietario
    elif not owner.REPRESENTA:
      wReg = 1
      message = 'PROPIETARIO no Tiene Representante'
    elif not owner.REP_SEXO:
      wReg = 1
      message = 'No definio Sexo del REPRESENTANTE'
    elif not owner.REP_ESTADO:
      wReg = 1
      message = 'No definio Estado Civil del REPRESENTANTE'
    elif not owner.REP_TIPDOC:
      wReg = 1
      message = 'No definio Tipo de Documento del REPRESENTANTE'
    elif not owner.REP_NUMERO:
      wReg = 1
      message = 'No definio Numero de Documento del REPRESENTANTE'
    elif not owner.RAZONSOCIA:
      wReg = 1
      message = 'EMPRESA no Tiene Razon Social'
    elif not owner.FICHA:
      wReg = 1
      message = 'EMPRESA no Tiene Ficha Inscripcion'
    elif not owner.DOCUMENTO:
      wReg = 1
      message = 'EMPRESA no Tiene Documento de Inscripcion'
    elif not owner.REP_ADMON:
      wReg = 1
      message = 'Empresa no Tiene Empresa Administradora'
    # Verificar datos de la central
    elif not central.LIMI_NORTE:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Norte'
    elif not central.LIMI_SUR:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Sur'
    elif not central.LIMI_ESTE:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Este'
    elif not central.LIMI_OESTE:
      wReg = 1
      message = 'CENTRAL no Tiene Limite por el Oeste'
    # Verificar datos del conductor
    elif driver.SEXO == '0':
      wReg = 1
      message = 'No definio Sexo del CONDUCTOR'
    elif not driver.ESTA_CIVIL:
      wReg = 1
      message = 'No definio Estado Civil del CONDUCTOR'
    elif not driver.NOMBRE:
      wReg = 1
      message = 'CONDUCTOR no Tiene Nombre'
    elif not driver.NIT:
      wReg = 1
      message = 'CONDUCTOR no Tiene No. de Cedula'
    elif not driver.DIRECCION:
      wReg = 1
      message = 'CONDUCTOR no Tiene Direccion'
    elif not driver.TELEFONO and not driver.CELULAR:
      wReg = 1
      message = 'CONDUCTOR no Tiene Telefono o Celular'
    elif not driver.RECOME_NOM:
      wReg = 1
      message = 'CONDUCTOR no Tiene RECOMENDADO'
    elif not driver.RECOME_CED:
      wReg = 1
      message = 'RECOMENDADO no Tiene No. de Cedula'

    if wReg == 1:
      return JSONResponse(content={"message": message}, status_code=400)
    
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
      'Rep_admon': owner.REP_ADMON,
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

#-----------------------------------------------------------------------------------------------

async def validation(bill_data: BillValidation):
  db = session()
  try:
    vehicle_state = db.query(
                Vehiculos
                ).join(
                  Estados, Vehiculos.ESTADO == Estados.CODIGO
                ).filter(
                  Vehiculos.NUMERO == bill_data.vehicle_number,
                  Vehiculos.EMPRESA == bill_data.company_code,
                  Estados.EMPRESA == bill_data.company_code,
                  Estados.ESTADO == 1
                ).first()
    
    vehicle_driver = db.query(
                Vehiculos.CONDUCTOR
                ).filter(
                  Vehiculos.NUMERO == bill_data.vehicle_number,
                  Vehiculos.EMPRESA == bill_data.company_code
                ).first()
    
    # panama_timezone = pytz.timezone('America/Panama')
    # now_in_panama = datetime.now(panama_timezone)
    # year = now_in_panama.strftime("%Y")
    # month = now_in_panama.strftime("%m")
    # day = now_in_panama.strftime("%d")
    # bill_date = f"{str(year)[-2:]}{month}{day}-{vehicle_driver.CONDUCTOR}"

    year = bill_data.bill_date.year
    month = bill_data.bill_date.month
    day = bill_data.bill_date.day
    bill_date = f"{str(year)[-2:]}{month:02d}{day:02d}-{vehicle_driver.CONDUCTOR}"

    vehicle_bill = db.query(
                Cartera
                ).filter(
                  Cartera.EMPRESA == bill_data.company_code,
                  Cartera.UNIDAD == bill_data.vehicle_number,
                  Cartera.FACTURA == bill_date
                ).first()

    response_data = {
      "vehicle_state": 1 if vehicle_state else 0,
      "vehicle_driver": 1 if vehicle_driver.CONDUCTOR not in [None, ''] else 0,
      "vehicle_bill": 1 if vehicle_bill else 0,
    }

    return JSONResponse(content=jsonable_encoder(response_data), status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def new_bill(bill_data: BillInfo):
  db = session()
  try:
    vehicle = db.query(
                Vehiculos
                ).join(
                  Estados, Vehiculos.ESTADO == Estados.CODIGO
                ).filter(
                  Vehiculos.NUMERO == bill_data.vehicle_number,
                  Vehiculos.EMPRESA == bill_data.company_code,
                  Estados.EMPRESA == bill_data.company_code,
                  Estados.ESTADO == 1
                ).first()
    
    if not vehicle:
      return JSONResponse(content={"message": "Vehículo no encontrado o no está en estado activo"}, status_code=404)
    
    vehicle_driver = db.query(
                Conductores
                ).filter(
                  Conductores.CODIGO == vehicle.CONDUCTOR,
                  Conductores.EMPRESA == bill_data.company_code,
                  Conductores.CODIGO == bill_data.driver_number
                ).first()

    if not vehicle_driver:
      return JSONResponse(content={"message": "Conductor no encontrado o no está asignado al vehículo"}, status_code=404)

    bill_date = f"{str(bill_data.bill_date.year)[-2:]}{bill_data.bill_date.month:02d}{bill_data.bill_date.day:02d}-{bill_data.driver_number}"

    vehicle_bill = db.query(
                Cartera
                ).filter(
                  Cartera.EMPRESA == bill_data.company_code,
                  Cartera.UNIDAD == bill_data.vehicle_number,
                  Cartera.FACTURA == bill_date
                ).first()
    
    if vehicle_bill:
      return JSONResponse(content={"message": "La cuenta ya existe para este vehículo"}, status_code=400)
    
    panama_timezone = pytz.timezone('America/Panama')
    now_in_panama = datetime.now(panama_timezone)
    
    new_bill = Cartera(
      EMPRESA=bill_data.company_code,
      FACTURA=bill_date,
      TIPO='10',
      CLIENTE=bill_data.driver_number,
      CEDULA=vehicle_driver.CEDULA,
      ZONA=vehicle.PROPI_IDEN,
      PLACA=vehicle.PLACA,
      UNIDAD=bill_data.vehicle_number,
      PROPI_IDEN=vehicle.PROPI_IDEN,
      FEC_ENTREG=bill_data.bill_date,
      VALOR=vehicle_driver.CUO_DIARIA,
      FECHA=bill_data.bill_date,
      FEC_FACTU= bill_data.bill_date,
      DOC_FACTU=bill_date,
      CAN_FACTU=1,
      DETALLE='Cuenta creada ' + bill_data.bill_date.strftime('%d/%m/%Y') + ' ---> Unidad: ' + bill_data.vehicle_number + ' - Conductor: ' + bill_data.driver_number + ' ' + vehicle_driver.NOMBRE,
      SALDO=vehicle_driver.CUO_DIARIA,
      FEC_CUADRE=bill_data.bill_date,
      FEC_DOC=bill_data.bill_date.strftime('%Y%m%d'),
      FEC_DOCUM=bill_data.bill_date.strftime('%Y%m%d'),
      FEC_CREADO=now_in_panama,
      USU_CREADO=bill_data.user
    )

    db.add(new_bill)
    db.commit()

    base_path = None

    if bill_data.company_code == '10':
      base_path = path_10
    elif bill_data.company_code == '58':
      base_path = path_58

    if base_path:
      text_file = os.path.join(base_path, f"crearcuenta_{vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{vehicle.NUMERO},,,,,,,{now_in_panama.strftime('%d%m%Y')},{now_in_panama.strftime('%Y-%m-%d')},{clean_text(bill_data.user)}")

    return JSONResponse(content={"message": "Cuenta creada con éxito"}, status_code=201)
  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def change_yard(data: ChangeYard):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.vehicle_number, Vehiculos.EMPRESA == data.company_code).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    yard = db.query(Patios).filter(Patios.CODIGO == data.yard_code, Patios.EMPRESA == data.company_code).first()
    if not yard:
      return JSONResponse(content={"message": "Yard not found"}, status_code=404)

    vehicle.PATIO = data.yard_code
    vehicle.NOMPATIO = yard.NOMBRE

    db.commit()

    base_path = None

    if data.company_code == '10':
      base_path = path_10
    elif data.company_code == '58':
      base_path = path_58

    if base_path:
      panama_timezone = pytz.timezone('America/Panama')
      now_in_panama = datetime.now(panama_timezone)

      text_file = os.path.join(base_path, f"cambiopatio_{vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{vehicle.NUMERO},,,,{vehicle.PATIO},,{clean_text(data.description)},,{now_in_panama.strftime('%Y-%m-%d')},{clean_text(data.user)}")

    return JSONResponse(content={"message": "Vehículo cambiado de patio con éxito"}, status_code=200)

  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def change_vehicle_state(data: ChangeVehicleState):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.vehicle_number, Vehiculos.EMPRESA == data.company_code).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    state = db.query(Estados).filter(Estados.CODIGO == data.state_code, Estados.EMPRESA == data.company_code).first()
    if not state:
      return JSONResponse(content={"message": "State not found"}, status_code=404)
    
    yard = db.query(Patios).filter(Patios.CODIGO == data.yard_code, Patios.EMPRESA == data.company_code).first()
    if not yard:
      return JSONResponse(content={"message": "Yard not found"}, status_code=404)

    vehicle.ESTADO = data.state_code
    vehicle.ABREVIADO = state.ABREVIADO
    vehicle.NOMESTADO = state.NOMBRE
    vehicle.PATIO = yard.CODIGO
    vehicle.NOMPATIO = yard.NOMBRE

    db.commit()

    base_path = None

    if data.company_code == '10':
      base_path = path_10
    elif data.company_code == '58':
      base_path = path_58

    if base_path:
      panama_timezone = pytz.timezone('America/Panama')
      now_in_panama = datetime.now(panama_timezone)

      text_file = os.path.join(base_path, f"cambiarestado_{vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{vehicle.NUMERO},,,{vehicle.ESTADO},{vehicle.PATIO},,{clean_text(data.change_reason)},,{now_in_panama.strftime('%Y-%m-%d')},{clean_text(data.user)}")

    return JSONResponse(content={"message": "Estado del vehículo cambiado con éxito"}, status_code=200)

  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def vehicle_mileage(company_code: str, vehicle_number: str):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_number, Vehiculos.EMPRESA == company_code).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    mileage = {
      'mileage': vehicle.KILOMETRAJ
    }

    return JSONResponse(content=jsonable_encoder(mileage), status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def update_mileage(data: VehicleMileage):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.vehicle_number, Vehiculos.EMPRESA == data.company_code).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehicle not found"}, status_code=404)
    
    vehicle.KILO_ANTES = vehicle.KILOMETRAJ
    vehicle.KILOMETRAJ = data.mileage
    db.commit()

    base_path = None

    if data.company_code == '10':
      base_path = path_10
    elif data.company_code == '58':
      base_path = path_58

    if base_path:
      panama_timezone = pytz.timezone('America/Panama')
      now_in_panama = datetime.now(panama_timezone)

      text_file = os.path.join(base_path, f"corregirkilometraje_{vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{vehicle.NUMERO},,,,,{vehicle.KILOMETRAJ},,,{now_in_panama.strftime('%Y-%m-%d')},{clean_text(data.user)}")

    return JSONResponse(content={"message": "Kilometraje actualizado con éxito"}, status_code=200)

  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def loan_validation(company_code: str, vehicle_number: str):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_number, Vehiculos.EMPRESA == company_code).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehículo no encontrado"}, status_code=404)
    
    vehicle_driver = db.query(Conductores).filter(Conductores.CODIGO == vehicle.CONDUCTOR, Conductores.EMPRESA == company_code).first()
    
    state = 0

    if vehicle.ESTADO == '01' or vehicle.ESTADO == '11' or vehicle.ESTADO == '12':
      state = 1

    driver = 0

    if vehicle.CONDUCTOR and vehicle.CONDUCTOR != '':
      driver = 1

    loaned = 0
    if vehicle_driver.UND_PRE and vehicle_driver.UND_PRE != '':
      loaned = 1

    response = {
      "state": state,
      "driver": driver,
      "loaned_unit": loaned
    }

    return JSONResponse(content=response, status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def loan_vehicle(data: LoanVehicle):
  db = session()
  try:
    original_vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.original_vehicle, Vehiculos.EMPRESA == data.company_code).first()

    if not original_vehicle:
      return JSONResponse(content={"message": "Vehículo no encontrado"}, status_code=404)

    if original_vehicle.ESTADO != '01' and original_vehicle.ESTADO != '11' and original_vehicle.ESTADO != '12':
      return JSONResponse(content={"message": "Vehículo no está en estado disponible para préstamo"}, status_code=400)

    if not original_vehicle.CONDUCTOR or original_vehicle.CONDUCTOR == '':
      return JSONResponse(content={"message": "Vehículo debe tener un conductor asignado"}, status_code=400)
    
    loan_vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.loan_vehicle, Vehiculos.EMPRESA == data.company_code).first()

    if not loan_vehicle:
      return JSONResponse(content={"message": "Vehículo para préstamo no encontrado"}, status_code=404)
    
    if loan_vehicle.ESTADO != '06':
      return JSONResponse(content={"message": "Vehículo debe estar esperando operador"}, status_code=400)
    
    if data.reason == '':
      return JSONResponse(content={"message": "Motivo del préstamo es requerido"}, status_code=400)
    
    loan_vehicle_state = db.query(Estados).filter(Estados.CODIGO == '19', Estados.EMPRESA == data.company_code).first()
    if not loan_vehicle_state:
      return JSONResponse(content={"message": "Estado no encontrado"}, status_code=404)

    original_vehicle_state = db.query(Estados).filter(Estados.CODIGO == '11', Estados.EMPRESA == data.company_code).first()
    if not original_vehicle_state:
      return JSONResponse(content={"message": "Estado no encontrado"}, status_code=404)
    
    driver = db.query(Conductores).filter(Conductores.CODIGO == original_vehicle.CONDUCTOR, Conductores.EMPRESA == data.company_code).first()
    if not driver:
      return JSONResponse(content={"message": "Conductor no encontrado"}, status_code=404)
    
    if driver.UND_PRE and driver.UND_PRE != '':
      return JSONResponse(content={"message": "Conductor ya tiene un vehículo prestado"}, status_code=400)

    panama_timezone = pytz.timezone('America/Panama')
    now_in_panama = datetime.now(panama_timezone)
    
    loan_vehicle.ESTADO = '19'
    loan_vehicle.ABREVIADO = loan_vehicle_state.ABREVIADO
    loan_vehicle.NOMESTADO = loan_vehicle_state.NOMBRE

    if original_vehicle.ESTADO == '01':
      original_vehicle.ESTADO = '11'
      original_vehicle.ABREVIADO = original_vehicle_state.ABREVIADO
      original_vehicle.NOMESTADO = original_vehicle_state.NOMBRE

    driver.UND_NRO = loan_vehicle.NUMERO
    driver.UND_PRE = original_vehicle.NUMERO
    driver.FEC_PRESTA = now_in_panama

    loan_vehicle.CONDUCTOR = driver.CODIGO

    db.commit()

    base_path = None

    if data.company_code == '10':
      base_path = path_10
    elif data.company_code == '58':
      base_path = path_58

    if base_path:
      text_file = os.path.join(base_path, f"prestamovehiculo_{original_vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{original_vehicle.NUMERO},{loan_vehicle.NUMERO},,,,,{clean_text(data.reason)},,{now_in_panama.strftime('%Y-%m-%d')},{clean_text(data.user)}")

    return JSONResponse(content={"message": "Préstamo de vehículo realizado con éxito"}, status_code=200)

  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def return_validation(company_code: str, vehicle_number: str):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == vehicle_number, Vehiculos.EMPRESA == company_code).first()
    if not vehicle:
      return JSONResponse(content={"message": "Vehículo no encontrado"}, status_code=404)

    state = 0

    if vehicle.ESTADO == '19':
      state = 1

    response = {
      "state": state,
    }

    return JSONResponse(content=response, status_code=200)

  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def return_vehicle(data: ReturnVehicle):
  db = session()
  try:
    return_vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.return_vehicle, Vehiculos.EMPRESA == data.company_code).first()
    if not return_vehicle:
      return JSONResponse(content={"message": "Vehículo de préstamo no encontrado"}, status_code=404)
    
    if return_vehicle.ESTADO != '19':
      return JSONResponse(content={"message": "Vehículo no está en estado de préstamo"}, status_code=400)
    
    original_vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.original_vehicle, Vehiculos.EMPRESA == data.company_code).first()
    if not original_vehicle:
      return JSONResponse(content={"message": "Vehículo original no encontrado"}, status_code=404)
    
    if data.reason == '':
      return JSONResponse(content={"message": "Motivo de la devolución es requerido"}, status_code=400)
    
    return_vehicle_state = db.query(Estados).filter(Estados.CODIGO == '06', Estados.EMPRESA == data.company_code).first()
    if not return_vehicle_state:
      return JSONResponse(content={"message": "Estado no encontrado"}, status_code=404)
    
    original_vehicle_state = db.query(Estados).filter(Estados.CODIGO == '01', Estados.EMPRESA == data.company_code).first()
    if not original_vehicle_state:
      return JSONResponse(content={"message": "Estado no encontrado"}, status_code=404)
    
    driver = db.query(Conductores).filter(Conductores.CODIGO == return_vehicle.CONDUCTOR, Conductores.EMPRESA == data.company_code).first()
    if not driver:
      return JSONResponse(content={"message": "Conductor no encontrado"}, status_code=404)
    
    panama_timezone = pytz.timezone('America/Panama')
    now_in_panama = datetime.now(panama_timezone)

    return_vehicle.ESTADO = '06'
    return_vehicle.ABREVIADO = return_vehicle_state.ABREVIADO
    return_vehicle.NOMESTADO = return_vehicle_state.NOMBRE
    return_vehicle.CONDUCTOR = ''

    original_vehicle.ESTADO = '01'
    original_vehicle.ABREVIADO = original_vehicle_state.ABREVIADO
    original_vehicle.NOMESTADO = original_vehicle_state.NOMBRE

    driver.UND_NRO = original_vehicle.NUMERO
    driver.UND_PRE = ''
    driver.FEC_PRESTA = None
    driver.FEC_DEVOLU = now_in_panama

    db.commit()

    base_path = None

    if data.company_code == '10':
      base_path = path_10
    elif data.company_code == '58':
      base_path = path_58

    if base_path:
      text_file = os.path.join(base_path, f"devolucion_{return_vehicle.NUMERO}.txt")
      with open(text_file, 'w') as file:
        file.write(f"{original_vehicle.NUMERO},{return_vehicle.NUMERO},,,,,{clean_text(data.reason)},,{now_in_panama.strftime('%Y-%m-%d')},{clean_text(data.user)}")

    return JSONResponse(content={"message": "Devolución de vehículo realizada con éxito"}, status_code=200)
  except Exception as e:
    db.rollback()
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()
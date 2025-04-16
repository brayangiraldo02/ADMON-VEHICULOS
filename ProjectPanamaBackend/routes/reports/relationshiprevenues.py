from fastapi import APIRouter
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.cajarecaudos import CajaRecaudos
from models.propietarios import Propietarios
from schemas.reports import *
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime
import pytz
import os

from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

templateJinja = Jinja2Templates(directory="templates")

relationshiprevenuesReports_router = APIRouter()

@relationshiprevenuesReports_router.post("/relationshiprevenues", tags=["Reports"])
async def relationshiprevenues_report(data: RelationshipRevenuesReport):
  db = session()
  try:
    if data.primeraFecha > data.ultimaFecha:
      return JSONResponse(content={"error": "La primera fecha no puede ser mayor a la última fecha"}, status_code=400)

    user_admin = os.getenv("USER_ADMIN")
    
    if data.unidad == "" or data.unidad == "TODOS":
      if data.usuario != user_admin:
        empresa = db.query(Propietarios.CODIGO).filter(Propietarios.NOMBRE == data.empresa).all()
        if len(empresa) == 0:
          return JSONResponse(content={"error": "No se encontró la empresa"}, status_code=400)
        empresa = empresa[0][0]

        conteo_reporte_ingresos = db.query(
          CajaRecaudos.RECIBO.label('recibo'),
          CajaRecaudos.FEC_RECIBO.label('fecha_recibo'),
          CajaRecaudos.NUMERO.label('unidad'),
          CajaRecaudos.SDO_RENTA.label('saldo_renta'),
          CajaRecaudos.DEU_RENTA.label('deuda_renta'),
          CajaRecaudos.FON_INSCRI.label('fondo_inscripcion'),
          CajaRecaudos.FON_AHORRO.label('fondo_ahorro'),
          CajaRecaudos.DEU_SINIES.label('deuda_siniestro'),
          CajaRecaudos.FORMAPAGO.label('forma_pago'),
          CajaRecaudos.TOTAL.label('total'),
          Propietarios.NOMBRE.label('empresa')
        ) \
        .join(Propietarios, Propietarios.CODIGO == CajaRecaudos.PROPI_IDEN) \
        .filter(
          CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
          CajaRecaudos.FEC_RECIBO <= data.ultimaFecha,
          CajaRecaudos.PROPI_IDEN == empresa
        ).all()
      else:
        conteo_reporte_ingresos = db.query(
          CajaRecaudos.RECIBO.label('recibo'),
          CajaRecaudos.FEC_RECIBO.label('fecha_recibo'),
          CajaRecaudos.NUMERO.label('unidad'),
          CajaRecaudos.SDO_RENTA.label('saldo_renta'),
          CajaRecaudos.DEU_RENTA.label('deuda_renta'),
          CajaRecaudos.FON_INSCRI.label('fondo_inscripcion'),
          CajaRecaudos.FON_AHORRO.label('fondo_ahorro'),
          CajaRecaudos.DEU_SINIES.label('deuda_siniestro'),
          CajaRecaudos.FORMAPAGO.label('forma_pago'),
          CajaRecaudos.TOTAL.label('total'),
          Propietarios.NOMBRE.label('empresa')
        ) \
        .join(Propietarios, Propietarios.CODIGO == CajaRecaudos.PROPI_IDEN) \
        .filter(
          CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
          CajaRecaudos.FEC_RECIBO <= data.ultimaFecha,
        ).all()

    elif data.unidad != "" and data.unidad != "TODOS":
      conteo_reporte_ingresos = db.query(
          CajaRecaudos.RECIBO.label('recibo'),
          CajaRecaudos.FEC_RECIBO.label('fecha_recibo'),
          CajaRecaudos.NUMERO.label('unidad'),
          CajaRecaudos.SDO_RENTA.label('saldo_renta'),
          CajaRecaudos.DEU_RENTA.label('deuda_renta'),
          CajaRecaudos.FON_INSCRI.label('fondo_inscripcion'),
          CajaRecaudos.FON_AHORRO.label('fondo_ahorro'),
          CajaRecaudos.DEU_SINIES.label('deuda_siniestro'),
          CajaRecaudos.FORMAPAGO.label('forma_pago'),
          CajaRecaudos.TOTAL.label('total'),
          Propietarios.NOMBRE.label('empresa')
        ) \
        .join(Propietarios, Propietarios.CODIGO == CajaRecaudos.PROPI_IDEN) \
        .filter(
          CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
          CajaRecaudos.FEC_RECIBO <= data.ultimaFecha,
          CajaRecaudos.NUMERO == data.unidad
        ).all()
      
    if len(conteo_reporte_ingresos) == 0:
      return JSONResponse(content={"error": "No se encontraron registros"}, status_code=400)
    
    aggregated_data = {}
    for item in conteo_reporte_ingresos:
      key = item.recibo
      if key not in aggregated_data:
        aggregated_data[key] = {
          "recibo": item.recibo,
          "fecha_recibo": item.fecha_recibo,
          "unidad": item.unidad,
          "empresa": item.empresa,
          "forma_pago": item.forma_pago,
          "saldo_renta": item.saldo_renta,
          "deuda_renta": item.deuda_renta,
          "fondo_inscripcion": item.fondo_inscripcion,
          "fondo_ahorro": item.fondo_ahorro,
          "deuda_siniestro": item.deuda_siniestro,
          "total": item.total
        }
      else:
      # Verificar y asignar valores no vacíos si el registro existente tiene campos vacíos
        if not aggregated_data[key]["fecha_recibo"] and item.fecha_recibo:
            aggregated_data[key]["fecha_recibo"] = item.fecha_recibo
        if not aggregated_data[key]["unidad"] and item.unidad:
            aggregated_data[key]["unidad"] = item.unidad
        if not aggregated_data[key]["empresa"] and item.empresa:
            aggregated_data[key]["empresa"] = item.empresa
        if not aggregated_data[key]["forma_pago"] and item.forma_pago:
            aggregated_data[key]["forma_pago"] = item.forma_pago
        if not aggregated_data[key]["saldo_renta"] and item.saldo_renta:
            aggregated_data[key]["saldo_renta"] = item.saldo_renta
      
        # Sumar los valores numéricos
        aggregated_data[key]["deuda_renta"] += item.deuda_renta
        aggregated_data[key]["fondo_inscripcion"] += item.fondo_inscripcion
        aggregated_data[key]["fondo_ahorro"] += item.fondo_ahorro
        aggregated_data[key]["deuda_siniestro"] += item.deuda_siniestro

    data_reporte = list(aggregated_data.values())

    # Filtrar registros que tengan campos string obligatorios vacíos.
    # Se consideran obligatorios: recibo, unidad, empresa y forma_pago.
    registros_filtrados = [
      row for row in data_reporte
      if row["recibo"] and row["unidad"] and row["empresa"] and row["forma_pago"]
    ]

    # Ordenar registros por número de unidad
    registros_ordenados = sorted(registros_filtrados, key=lambda x: x["unidad"])

    # CALCULAR LOS TOTALES a partir de los registros filtrados
    total_deuda_renta = 0
    total_fondo_inscripcion = 0
    total_fondo_ahorro = 0
    total_deuda_siniestro = 0
    total_efectivo = 0
    total_nequi = 0
    total_arp = 0
    total_bangeneral = 0
    total_total = 0

    for item in registros_ordenados:
      total_deuda_renta += item["deuda_renta"]
      total_fondo_inscripcion += item["fondo_inscripcion"]
      total_fondo_ahorro += item["fondo_ahorro"]
      total_deuda_siniestro += item["deuda_siniestro"]
      total_total += item["total"]

      if item["forma_pago"] == "1":
        total_efectivo += item["total"]
      elif item["forma_pago"] == "2":
        total_nequi += item["total"]
      elif item["forma_pago"] == "3":
        total_arp += item["total"]
      elif item["forma_pago"] == "4":
        total_bangeneral += item["total"]

    # Get current date
    panama_timezone = pytz.timezone('America/Panama')
    # Obtén la hora actual en la zona horaria de Ciudad de Panamá
    now_in_panama = datetime.now(panama_timezone)
    # Formatea la fecha y la hora según lo requerido
    fecha = now_in_panama.strftime("%d/%m/%Y")
    hora_actual = now_in_panama.strftime("%I:%M:%S %p")
    usuario = data.usuario
    titulo = 'Detalle Relación de Ingresos'

    if data.usuario == user_admin:
      usuario = "Administrador"
    else:
      usuario = data.usuario

    response = {
      "reporte": registros_ordenados,
      "totales": {
        "deuda_renta": total_deuda_renta,
        "fondo_inscripcion": total_fondo_inscripcion,
        "fondo_ahorro": total_fondo_ahorro,
        "deuda_siniestro": total_deuda_siniestro,
        "efectivo": total_efectivo,
        "nequi": total_nequi,
        "arp": total_arp,
        "banco_general": total_bangeneral,
        "total": total_total
      },
      "fechas": {
        "primeraFecha": data.primeraFecha,
        "ultimaFecha": data.ultimaFecha
      },
      "usuario": usuario,
      "fecha": fecha,
      "hora": hora_actual,
    }

    data_reporte = response

    headers = {
      "Content-Disposition": "inline; relacion-ingresos.pdf"
    }  

    # return JSONResponse(content=jsonable_encoder(data_reporte))

    #!Falta corregir un problema con la asignación de los valores de forma de pago

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "RelacionIngresos.html"
    header_file = "header1.html"
    footer_file = "footer1.html"
    template = template_env.get_template(template_file)
    header = template_env.get_template(header_file)
    footer = template_env.get_template(footer_file)
    output_text = template.render(data=data_reporte) 
    output_header = header.render(data_reporte)
    output_footer = footer.render(data_reporte)

    html_path = f'./templates/renderform1.html'
    header_path = f'./templates/renderheader1.html'
    footer_path = f'./templates/renderfooter1.html'
    html_file = open(html_path, 'w')
    header_file = open(header_path, 'w')
    html_footer = open(footer_path, 'w')
    html_file.write(output_text)
    header_file.write(output_header)
    html_footer.write(output_footer)
    html_file.close()
    header_file.close()
    html_footer.close()
    pdf_path = 'relacion-ingresos.pdf'
    html2pdf(titulo,html_path, pdf_path, header_path=header_path, footer_path=footer_path)

    response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/relacion-ingresos.pdf', headers=headers)

    return response
  except Exception as e:
    return JSONResponse(content={"error": str(e)}, status_code=400)
  finally:
    db.close()



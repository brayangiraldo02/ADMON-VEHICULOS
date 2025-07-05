from fastapi import APIRouter
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.infoempresas import InfoEmpresas
from config.dbconnection import session
from models.cajarecaudos import CajaRecaudos
from models.propietarios import Propietarios
from models.vehiculos import Vehiculos
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

@relationshiprevenuesReports_router.post("/relationshiprevenues/", tags=["Reports"])
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
          Propietarios.EMPRESA.label('codigo_empresa'),
          CajaRecaudos.EMPRESA.label('num_empresa'),
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
          Propietarios.NOMBRE.label('empresa'),
          Vehiculos.PAGA_ADMON.label('paga_admon'),
          Vehiculos.GLOBAL_UND.label('global_und'),
          Vehiculos.CUO_ADMON.label('cuota_admon'),
          Vehiculos.CUO_DIARIA.label('cuota_diaria'),
        ) \
        .join(Propietarios, Propietarios.CODIGO == CajaRecaudos.PROPI_IDEN) \
        .join(Vehiculos, Vehiculos.NUMERO == CajaRecaudos.NUMERO) \
        .filter(
          CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
          CajaRecaudos.FEC_RECIBO <= data.ultimaFecha,
          CajaRecaudos.PROPI_IDEN == empresa,
          CajaRecaudos.FORMAPAGO.in_(["1", "2", "3", "4", "5"]),
          CajaRecaudos.EMPRESA == Propietarios.EMPRESA
        ).all()
      else:
        empresa = db.query(Propietarios.CODIGO).filter(Propietarios.NOMBRE == data.empresa).all()
        empresa = empresa[0][0]
        conteo_reporte_ingresos = db.query(
          Propietarios.EMPRESA.label('codigo_empresa'),
          CajaRecaudos.EMPRESA.label('num_empresa'),
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
          Propietarios.NOMBRE.label('empresa'),
          Vehiculos.PAGA_ADMON.label('paga_admon'),
          Vehiculos.GLOBAL_UND.label('global_und'),
          Vehiculos.CUO_ADMON.label('cuota_admon'),
          Vehiculos.CUO_DIARIA.label('cuota_diaria'),
        ) \
        .join(Propietarios, Propietarios.CODIGO == CajaRecaudos.PROPI_IDEN) \
        .join(Vehiculos, Vehiculos.NUMERO == CajaRecaudos.NUMERO) \
        .filter(
          CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
          CajaRecaudos.FEC_RECIBO <= data.ultimaFecha,
          CajaRecaudos.FORMAPAGO.in_(["1", "2", "3", "4", "5"]),
          CajaRecaudos.PROPI_IDEN == empresa,
          CajaRecaudos.EMPRESA == Propietarios.EMPRESA
        ).all()

    elif data.unidad != "" and data.unidad != "TODOS":
      empresa = db.query(Propietarios.CODIGO).filter(Propietarios.NOMBRE == data.empresa).all()
      empresa = empresa[0][0]
      conteo_reporte_ingresos = db.query(
          Propietarios.EMPRESA.label('codigo_empresa'),
          CajaRecaudos.EMPRESA.label('num_empresa'),
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
          Propietarios.NOMBRE.label('empresa'),
          Vehiculos.PAGA_ADMON.label('paga_admon'),
          Vehiculos.GLOBAL_UND.label('global_und'),
          Vehiculos.CUO_ADMON.label('cuota_admon'),
          Vehiculos.CUO_DIARIA.label('cuota_diaria'),
        ) \
        .join(Propietarios, Propietarios.CODIGO == CajaRecaudos.PROPI_IDEN) \
        .join(Vehiculos, Vehiculos.NUMERO == CajaRecaudos.NUMERO) \
        .filter(
          CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
          CajaRecaudos.FEC_RECIBO <= data.ultimaFecha,
          CajaRecaudos.NUMERO == data.unidad,
          CajaRecaudos.FORMAPAGO.in_(["1", "2", "3", "4", "5"]),
          CajaRecaudos.PROPI_IDEN == empresa,
          CajaRecaudos.EMPRESA == Propietarios.EMPRESA
        ).all()
      
    if len(conteo_reporte_ingresos) == 0:
      return JSONResponse(content={"error": "No se encontraron registros"}, status_code=400)
    
    id_empresa = conteo_reporte_ingresos[0].codigo_empresa

    aggregated_data = {}
    for item in conteo_reporte_ingresos:
      # Condición 1: forma_pago debe ser un string entre "1" y "5"
      forma_pago_valida = isinstance(item.forma_pago, str) and "1" <= item.forma_pago <= "5"
      
      # Condición 2: el item no debe tener todos los valores monetarios en 0
      # Se asume que si un valor es None, no se considera 0 para esta validación,
      # o que los valores ya son numéricos (e.g., 0.0 o Decimal('0')).
      todos_valores_monetarios_cero = (
          item.saldo_renta == 0 and
          item.deuda_renta == 0 and
          item.fondo_inscripcion == 0 and
          item.fondo_ahorro == 0 and
          item.deuda_siniestro == 0 and
          item.total == 0 
      )
      
      # Si la forma de pago no es válida o todos los valores monetarios son cero, saltar este item
      if not forma_pago_valida or todos_valores_monetarios_cero:
        continue

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
          "total": item.total,
          "paga_admon": 0
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

        admon_fee_component = 0
      if item.paga_admon == "1" and item.global_und == "2":
        # TODO: REVISAR REDONDEOS
        # print("deuda_renta", aggregated_data[key]["deuda_renta"], "cuota_admon", item.cuota_admon, "cuota_diaria", item.cuota_diaria)
        admon_fee_component = round((aggregated_data[key]["deuda_renta"] * item.cuota_admon) / item.cuota_diaria, 2)
        # admon_fee_component = int(raw * 100) / 100

        aggregated_data[key]["paga_admon"] = admon_fee_component

    data_reporte = list(aggregated_data.values())

    # Filtrar registros que tengan campos string obligatorios vacíos.
    # Se consideran obligatorios: recibo, unidad, empresa y forma_pago.
    registros_filtrados = [
      row for row in data_reporte
      if row["recibo"] and row["unidad"] and row["empresa"] and row["forma_pago"]
    ]

    # Ordenar registros por número de unidad
    registros_ordenados = sorted(registros_filtrados, key=lambda x: x["recibo"])

    # CALCULAR LOS TOTALES a partir de los registros filtrados
    total_deuda_renta = 0
    total_fondo_inscripcion = 0
    total_fondo_ahorro = 0
    total_deuda_siniestro = 0
    total_efectivo = 0
    total_ach = 0
    total_arp = 0 
    total_nequi = 0
    total_yappy = 0
    total_total = 0
    total_admon = 0

    for item in registros_ordenados:
      total_deuda_renta += item["deuda_renta"]
      total_fondo_inscripcion += item["fondo_inscripcion"]
      total_fondo_ahorro += item["fondo_ahorro"]
      total_deuda_siniestro += item["deuda_siniestro"]
      total_total += item["total"]
      total_admon += item["paga_admon"]

      if item["forma_pago"] == "1":
        total_efectivo += item["total"]
      elif item["forma_pago"] == "2":
        total_ach += item["total"]
      elif item["forma_pago"] == "3":
        total_arp += item["total"]
      elif item["forma_pago"] == "4":
        total_nequi += item["total"]
      elif item["forma_pago"] == "5":
        total_yappy += item["total"]

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

    info_empresa = db.query(
      InfoEmpresas.NOMBRE,
      InfoEmpresas.NIT,
      InfoEmpresas.LOGO
    ).filter(InfoEmpresas.ID == id_empresa).first()

    response = {
      "reporte": registros_ordenados,
      "totales": {
        "deuda_renta": total_deuda_renta,
        "fondo_inscripcion": total_fondo_inscripcion,
        "fondo_ahorro": total_fondo_ahorro,
        "deuda_siniestro": total_deuda_siniestro,
        "efectivo": total_efectivo,
        "ach": total_ach,
        "arp": total_arp,
        "nequi": total_nequi,
        "yappy": total_yappy,
        "total": total_total,
        "total_admon": total_admon,
        "total_resta_admon": total_total - total_admon
      },
      "fechas": {
        "primeraFecha": data.primeraFecha,
        "ultimaFecha": data.ultimaFecha
      },
      "usuario": usuario,
      "fecha": fecha,
      "hora": hora_actual,
      "nombre_empresa": info_empresa.NOMBRE,
      "nit_empresa": info_empresa.NIT,
      "logo_empresa": info_empresa.LOGO,
    }

    data_reporte = response

    headers = {
      "Content-Disposition": "attachment; relacion-ingresos.pdf"
    }  

    # return JSONResponse(content=jsonable_encoder(data_reporte)) 

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "RelacionIngresos.html"
    header_file = "header2.html"
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
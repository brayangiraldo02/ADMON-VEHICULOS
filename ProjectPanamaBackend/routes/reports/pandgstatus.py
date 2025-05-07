from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.propietarios import Propietarios
from config.dbconnection import session
from sqlalchemy import func, case
from models.vehiculos import Vehiculos
from models.cajarecaudos import CajaRecaudos
from models.reclamoscolisiones import ReclamosColisiones
from models.movimien import Movimien
from schemas.reports import PandGStatusReport
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

templateJinja = Jinja2Templates(directory="templates")

pandgstatus_router = APIRouter()

@pandgstatus_router.post("/pandgstatus", tags=["Reports"])
async def pandgstatus_report(data: PandGStatusReport):
  db = session()
  try:
    if data.primeraFecha > data.ultimaFecha:
      return JSONResponse(status_code=400, content={"message": "La primera fecha no puede ser mayor que la última fecha"})
    
    user_admin = os.getenv("USER_ADMIN")

    #* Si el usuario seleccionó todas las unidades o dejó vacío el campo
    if data.unidad == "" or data.unidad == "TODOS":

      #* Si el usuario no es el administrador, se obtiene la información de las unidades de la empresa a la que pertenece
      # if data.usuario != user_admin:
        empresa = db.query(Propietarios.CODIGO).filter(Propietarios.NOMBRE == data.empresa).first()
        if len(empresa) == 0:
          return JSONResponse(status_code=400, content={"error": "No se encontró la empresa"})

        empresa = empresa[0]

        # Obtener vehículos con sus recaudos en una sola consulta
        vehiculos_con_recaudos = db.query(
          Vehiculos.NUMERO,
          Vehiculos.FEC_CREADO,
          Vehiculos.MODELO,
          Vehiculos.VLR_COMPRA,
          Vehiculos.NOMESTADO,
          func.coalesce(func.sum(CajaRecaudos.DEU_RENTA), 0).label('total_recaudos')
        ).outerjoin(
          CajaRecaudos,
          (CajaRecaudos.NUMERO == Vehiculos.NUMERO) & 
          (CajaRecaudos.FEC_RECIBO >= data.primeraFecha) & 
          (CajaRecaudos.FEC_RECIBO <= data.ultimaFecha)
        ).filter(
          Vehiculos.PROPI_IDEN == empresa
        ).group_by(
          Vehiculos.NUMERO,
          Vehiculos.FEC_CREADO,
          Vehiculos.MODELO,
          Vehiculos.VLR_COMPRA,
          Vehiculos.NOMESTADO
        ).all()

        # Obtener los números de unidades para usarlos en la siguiente consulta
        numeros_unidades = [v.NUMERO for v in vehiculos_con_recaudos]

        # Obtener totales de movimientos por tipo y unidad en una sola consulta
        movimientos_por_tipo = db.query(
          Movimien.UNIDAD,
          Movimien.TIPO,
          func.sum(Movimien.TOTAL).label('total_tipo')
        ).filter(
          Movimien.UNIDAD.in_(numeros_unidades),
          Movimien.FECHA >= data.primeraFecha,
          Movimien.FECHA <= data.ultimaFecha,
          Movimien.TIPO.in_(['024', '027', '026', '022', '016']),
          # Movimien.FORMAPAGO.in_(['01', '02', '03', '04', '05'])
        ).group_by(
          Movimien.UNIDAD,
          Movimien.TIPO
        ).all()

        # Organizar los totales por unidad y tipo
        totales_movimientos = {}
        for mov in movimientos_por_tipo:
          if mov.UNIDAD not in totales_movimientos:
            totales_movimientos[mov.UNIDAD] = {
              '024': 0, '027': 0, '026': 0, '022': 0, '016': 0
            }
          totales_movimientos[mov.UNIDAD][mov.TIPO] = mov.total_tipo

        # Construir la respuesta final
        info_unidades = []
        for vehiculo in vehiculos_con_recaudos:
          # Obtener los totales de movimiento para esta unidad (o valores predeterminados)
          movs = totales_movimientos.get(vehiculo.NUMERO, {'024': 0, '027': 0, '026': 0, '022': 0, '016': 0})
          
          total_024 = movs.get('024', 0)
          total_027 = movs.get('027', 0)
          total_026 = movs.get('026', 0)
          total_022 = movs.get('022', 0)
          total_016 = movs.get('016', 0)
          total_almacen = total_022 - total_016
          
          # Calcular el balance de pérdidas y ganancias
          estado_pyg = vehiculo.total_recaudos - total_024 - total_027 - total_026 - total_almacen
          
          # Verificar si la unidad tiene algún movimiento
          tiene_movimientos = (
            vehiculo.NUMERO != "" and  # Verificar que el número no esté vacío
            (vehiculo.total_recaudos != 0 or
            total_024 != 0 or
            total_027 != 0 or
            total_026 != 0 or
            total_almacen != 0 or
            estado_pyg != 0)
          )
          
          # Solo agregar unidades con movimientos
          if tiene_movimientos:
              # Crear el diccionario con la información procesada
              info_unidad_dict = {
                  "NUMERO": vehiculo.NUMERO,
                  "FEC_CREADO": vehiculo.FEC_CREADO.strftime('%Y-%m-%d') if vehiculo.FEC_CREADO else None,
                  "MODELO": vehiculo.MODELO,
                  "VLR_COMPRA": vehiculo.VLR_COMPRA,
                  "NOMESTADO": vehiculo.NOMESTADO,
                  "INGRESOS": {
                      "INGRESOS": vehiculo.total_recaudos,
                      "SEGUROS": 0  # !PENDIENTE, REALIZAR LA RECOLECCIÓN DE LA INFORMACIÓN DE LA TABLA RECLAMOSCOLISIONES
                  },
                  "GASTOS": {
                      "GASTO_CAJA": total_024,
                      "GENERALES": total_027,
                      "OTRO_GASTO": 0
                  },
                  "PIEZAS_MOBRA": {
                      "CHAPISTERIA": total_026,
                      "ALMACEN": total_almacen
                  },
                  "ESTADOPyG": estado_pyg,  # Utilidad si es valor positivo, pérdida si es valor negativo
                  "AVANCE": 0
              }
              
              info_unidades.append(info_unidad_dict)

      #* Si el usuario es el administrador, se obtiene la información de todas las unidades
      # else:  
      #   #* Obtengo la información de todas las unidades en una sola consulta
      #   info_unidad = db.query(
      #     Vehiculos.NUMERO,
      #     Vehiculos.FEC_CREADO,
      #     Vehiculos.MODELO,
      #     Vehiculos.VLR_COMPRA,
      #     Vehiculos.NOMESTADO
      #   ).all()
        
      #   # Obtener todos los números de unidades para usarlos en las siguientes consultas
      #   numeros_unidades = [v.NUMERO for v in info_unidad]
        
      #   #* Obtengo la información de recaudos para todas las unidades en una sola consulta
      #   recaudos_por_unidad = db.query(
      #     CajaRecaudos.NUMERO,
      #     func.sum(CajaRecaudos.DEU_RENTA).label('total_recaudos')
      #   ).filter(
      #     CajaRecaudos.NUMERO.in_(numeros_unidades),
      #     CajaRecaudos.FEC_RECIBO >= data.primeraFecha,
      #     CajaRecaudos.FEC_RECIBO <= data.ultimaFecha
      #   ).group_by(
      #     CajaRecaudos.NUMERO
      #   ).all()
        
      #   # Crear un diccionario para acceder fácilmente a los recaudos por unidad
      #   dict_recaudos = {recaudo.NUMERO: recaudo.total_recaudos for recaudo in recaudos_por_unidad}
        
      #   #* Obtengo la información de movimientos para todas las unidades en una sola consulta
      #   movimientos_por_tipo = db.query(
      #     Movimien.UNIDAD,
      #     Movimien.TIPO,
      #     func.sum(Movimien.TOTAL).label('total_tipo')
      #   ).filter(
      #     Movimien.UNIDAD.in_(numeros_unidades),
      #     Movimien.FECHA >= data.primeraFecha,
      #     Movimien.FECHA <= data.ultimaFecha,
      #     Movimien.TIPO.in_(['024', '027', '026', '022', '016'])
      #   ).group_by(
      #     Movimien.UNIDAD,
      #     Movimien.TIPO
      #   ).all()
        
      #   # Organizar los totales por unidad y tipo
      #   totales_movimientos = {}
      #   for mov in movimientos_por_tipo:
      #     if mov.UNIDAD not in totales_movimientos:
      #       totales_movimientos[mov.UNIDAD] = {
      #         '024': 0, '027': 0, '026': 0, '022': 0, '016': 0
      #       }
      #     totales_movimientos[mov.UNIDAD][mov.TIPO] = mov.total_tipo
        
      #   #* Itero sobre cada unidad para construir el resultado final
      #   info_unidades = []
      #   for unidad in info_unidad:
      #     # Obtener los recaudos para esta unidad (o 0 si no hay)
      #     total_deu_renta = dict_recaudos.get(unidad.NUMERO, 0)
          
      #     # Obtener los totales de movimiento para esta unidad (o valores predeterminados)
      #     movs = totales_movimientos.get(unidad.NUMERO, {'024': 0, '027': 0, '026': 0, '022': 0, '016': 0})
          
      #     total_024 = movs.get('024', 0)
      #     total_027 = movs.get('027', 0)
      #     total_026 = movs.get('026', 0)
      #     total_022 = movs.get('022', 0)
      #     total_016 = movs.get('016', 0)
      #     total_almacen = total_022 - total_016
          
      #     # Calcular el balance de pérdidas y ganancias
      #     estado_pyg = total_deu_renta - total_024 - total_027 - total_026 - total_almacen
          
      #     # Verificar si la unidad tiene algún movimiento
      #     tiene_movimientos = (
      #       unidad.NUMERO != "" and  # Verificar que el número no esté vacío
      #       (total_deu_renta != 0 or
      #       total_024 != 0 or
      #       total_027 != 0 or
      #       total_026 != 0 or
      #       total_almacen != 0 or
      #       estado_pyg != 0)
      #     )
          
      #     # Solo agregar unidades con movimientos
      #     if tiene_movimientos:
      #         #* Creo un diccionario con la información de la unidad
      #         info_unidad_dict = {
      #             "NUMERO": unidad.NUMERO,
      #             "FEC_CREADO": unidad.FEC_CREADO.isoformat() if hasattr(unidad.FEC_CREADO, 'isoformat') else unidad.FEC_CREADO,
      #             "MODELO": unidad.MODELO,
      #             "VLR_COMPRA": unidad.VLR_COMPRA,
      #             "NOMESTADO": unidad.NOMESTADO,
      #             "INGRESOS": {
      #                 "INGRESOS": total_deu_renta,
      #                 "SEGUROS": 0 # !PENDIENTE, REALIZAR LA RECOLECCIÓN DE LA INFORMACIÓN DE LA TABLA RECLAMOSCOLISIONES
      #             },
      #             "GASTOS": {
      #                 "GASTO_CAJA": total_024,
      #                 "GENERALES": total_027,
      #                 "OTRO_GASTO": 0
      #             },
      #             "PIEZAS_MOBRA": {
      #                 "CHAPISTERIA": total_026,
      #                 "ALMACEN": total_almacen
      #             },
      #             "ESTADOPyG": estado_pyg, #* Utilidad si es valor positivo, pérdida si es valor negativo
      #             "AVANCE": 0
      #         }
              
      #         #* Agrego el diccionario a la lista de unidades
      #         info_unidades.append(info_unidad_dict)

    elif data.unidad != "" and data.unidad != "TODOS":
      # Optimizado: Obtener información del vehículo en una sola consulta
      info_unidad = db.query(
        Vehiculos.NUMERO,
        Vehiculos.FEC_CREADO,
        Vehiculos.MODELO,
        Vehiculos.VLR_COMPRA,
        Vehiculos.NOMESTADO,
        func.coalesce(func.sum(CajaRecaudos.DEU_RENTA), 0).label('total_recaudos')
      ).outerjoin(
        CajaRecaudos,
        (CajaRecaudos.NUMERO == Vehiculos.NUMERO) & 
        (CajaRecaudos.FEC_RECIBO >= data.primeraFecha) & 
        (CajaRecaudos.FEC_RECIBO <= data.ultimaFecha)
      ).filter(
        Vehiculos.NUMERO == data.unidad
      ).group_by(
        Vehiculos.NUMERO,
        Vehiculos.FEC_CREADO,
        Vehiculos.MODELO,
        Vehiculos.VLR_COMPRA,
        Vehiculos.NOMESTADO
      ).first()

      if not info_unidad:
        return JSONResponse(status_code=404, content={"error": "No se encontró la unidad"})

      # Optimizado: Obtener totales de movimientos por tipo en una sola consulta
      movimientos_por_tipo = db.query(
        Movimien.TIPO,
        func.sum(Movimien.TOTAL).label('total_tipo')
      ).filter(
        Movimien.UNIDAD == data.unidad,
        Movimien.FECHA >= data.primeraFecha,
        Movimien.FECHA <= data.ultimaFecha,
        Movimien.TIPO.in_(['024', '027', '026', '022', '016']),
        # Movimien.FORMAPAGO.in_(['01', '02', '03', '04', '05'])
      ).group_by(
        Movimien.TIPO
      ).all()

      # Crear un diccionario para los totales de cada tipo
      totales = {'024': 0, '027': 0, '026': 0, '022': 0, '016': 0}
      for mov in movimientos_por_tipo:
        totales[mov.TIPO] = mov.total_tipo

      # Calcular totales
      total_024 = totales['024']
      total_027 = totales['027']
      total_026 = totales['026']
      total_022 = totales['022']
      total_016 = totales['016']
      total_almacen = total_022 - total_016

      # Calcular estado de pérdidas y ganancias
      estado_pyg = info_unidad.total_recaudos - total_024 - total_027 - total_026 - total_almacen

      # Crear diccionario con la información procesada
      info_unidad_dict = {
        "NUMERO": data.unidad,
        "FEC_CREADO": info_unidad.FEC_CREADO.strftime('%Y-%m-%d') if vehiculo.FEC_CREADO else None,
        "MODELO": info_unidad.MODELO,
        "VLR_COMPRA": info_unidad.VLR_COMPRA,
        "NOMESTADO": info_unidad.NOMESTADO,
        "INGRESOS": {
          "INGRESOS": info_unidad.total_recaudos,
          "SEGUROS": 0  # !PENDIENTE, REALIZAR LA RECOLECCIÓN DE LA INFORMACIÓN DE LA TABLA RECLAMOSCOLISIONES
        },
        "GASTOS": {
          "GASTO_CAJA": total_024,
          "GENERALES": total_027,
          "OTRO_GASTO": 0
        },
        "PIEZAS_MOBRA": {
          "CHAPISTERIA": total_026,
          "ALMACEN": total_almacen
        },
        "ESTADOPyG": estado_pyg,  # Utilidad si es valor positivo, pérdida si es valor negativo
        "AVANCE": 0
      }

      info_unidades = info_unidad_dict

    # Get current date
    panama_timezone = pytz.timezone('America/Panama')
    # Obtén la hora actual en la zona horaria de Ciudad de Panamá
    now_in_panama = datetime.now(panama_timezone)
    # Formatea la fecha y la hora según lo requerido
    fecha = now_in_panama.strftime("%d/%m/%Y")
    hora_actual = now_in_panama.strftime("%I:%M:%S %p")
    titulo = 'Estado de Pérdidas y Ganancias'

    if data.usuario == user_admin:
      usuario = "Administrador"
    else:
      usuario = data.usuario

    # Reorganizar las unidades por empresa
    empresas_dict = {}

    if data.unidad != "" and data.unidad != "TODOS":
        # Caso de una unidad específica - obtener su empresa
        empresa_info = db.query(
            Propietarios.CODIGO,
            Propietarios.NOMBRE
        ).join(
            Vehiculos, Vehiculos.PROPI_IDEN == Propietarios.CODIGO
        ).filter(
            Vehiculos.NUMERO == data.unidad
        ).first()
        
        if empresa_info:
            codigo_empresa = empresa_info.CODIGO
            nombre_empresa = empresa_info.NOMBRE
            
            # Crear la estructura para esta empresa
            empresas_dict[nombre_empresa] = {
                "codigo": codigo_empresa,
                "nombre": nombre_empresa,
                "unidades": [info_unidades],  # Es un solo objeto, no una lista
                "totales_empresa": {
                    "cantidad_unidades": 1,
                    "ingresos": info_unidades['INGRESOS']['INGRESOS'],
                    "seguros": info_unidades['INGRESOS']['SEGUROS'],
                    "gasto_caja": info_unidades['GASTOS']['GASTO_CAJA'],
                    "generales": info_unidades['GASTOS']['GENERALES'],
                    "otro_gasto": info_unidades['GASTOS']['OTRO_GASTO'],
                    "chapisteria": info_unidades['PIEZAS_MOBRA']['CHAPISTERIA'],
                    "almacen": info_unidades['PIEZAS_MOBRA']['ALMACEN'],
                    "utilidad": max(0, info_unidades['ESTADOPyG']),
                    "perdida": max(0, -info_unidades['ESTADOPyG']),
                    "avance": info_unidades['AVANCE']
                }
            }
    else:
        # Caso de múltiples unidades - obtener empresa para cada unidad
        # Obtener información de todas las empresas y sus vehículos
        empresas_info = db.query(
            Vehiculos.NUMERO,
            Propietarios.CODIGO,
            Propietarios.NOMBRE
        ).join(
            Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO
        ).filter(
            Vehiculos.NUMERO.in_([u["NUMERO"] for u in info_unidades])
        ).all()
        
        # Crear un diccionario para mapear unidades a empresas
        unidad_a_empresa = {e.NUMERO: {"codigo": e.CODIGO, "nombre": e.NOMBRE} for e in empresas_info}
        
        # Crear un diccionario para almacenar unidades temporalmente por empresa
        unidades_por_empresa = {}
        
        # Agrupar unidades por empresa
        for unidad in info_unidades:
            empresa_info = unidad_a_empresa.get(unidad["NUMERO"])
            if empresa_info:
                nombre_empresa = empresa_info["nombre"]
                
                # Si la empresa no existe en el diccionario temporal, crearla
                if nombre_empresa not in unidades_por_empresa:
                    unidades_por_empresa[nombre_empresa] = {
                        "codigo": empresa_info["codigo"],
                        "unidades": []
                    }
                
                # Añadir la unidad al diccionario temporal
                unidades_por_empresa[nombre_empresa]["unidades"].append(unidad)
        
        # Procesar cada empresa, ordenando sus unidades
        for nombre_empresa, info in unidades_por_empresa.items():
            # Ordenar las unidades por número alfabéticamente
            unidades_ordenadas = sorted(info["unidades"], key=lambda u: u["NUMERO"])
            
            # Inicializar totales de la empresa
            totales_empresa = {
                "cantidad_unidades": len(unidades_ordenadas),
                "ingresos": 0,
                "seguros": 0,
                "gasto_caja": 0,
                "generales": 0,
                "otro_gasto": 0,
                "chapisteria": 0,
                "almacen": 0,
                "utilidad": 0,
                "perdida": 0,
                "avance": 0
            }
            
            # Calcular totales de la empresa con las unidades ya ordenadas
            for unidad in unidades_ordenadas:
                totales_empresa["ingresos"] += unidad["INGRESOS"]["INGRESOS"]
                totales_empresa["seguros"] += unidad["INGRESOS"]["SEGUROS"]
                totales_empresa["gasto_caja"] += unidad["GASTOS"]["GASTO_CAJA"]
                totales_empresa["generales"] += unidad["GASTOS"]["GENERALES"]
                totales_empresa["otro_gasto"] += unidad["GASTOS"]["OTRO_GASTO"]
                totales_empresa["chapisteria"] += unidad["PIEZAS_MOBRA"]["CHAPISTERIA"]
                totales_empresa["almacen"] += unidad["PIEZAS_MOBRA"]["ALMACEN"]
                
                if unidad["ESTADOPyG"] > 0:
                    totales_empresa["utilidad"] += unidad["ESTADOPyG"]
                else:
                    totales_empresa["perdida"] += -unidad["ESTADOPyG"]
            
            # Agregar la empresa con sus unidades ordenadas al diccionario final
            empresas_dict[nombre_empresa] = {
                "codigo": info["codigo"],
                "nombre": nombre_empresa,
                "unidades": unidades_ordenadas,
                "totales_empresa": totales_empresa
            }

    # Calcular totales generales sumando los totales de cada empresa
    totales_generales = {
        "cantidad_unidades": 0,
        "ingresos": 0,
        "seguros": 0,
        "gasto_caja": 0,
        "generales": 0,
        "otro_gasto": 0,
        "chapisteria": 0,
        "almacen": 0,
        "utilidad": 0,
        "perdida": 0,
        "avance": 0
    }

    # Solo calculamos los totales si hay empresas en el diccionario
    if empresas_dict:
        totales_generales = {
            "cantidad_unidades": sum(e["totales_empresa"]["cantidad_unidades"] for e in empresas_dict.values()),
            "ingresos": sum(e["totales_empresa"]["ingresos"] for e in empresas_dict.values()),
            "seguros": sum(e["totales_empresa"]["seguros"] for e in empresas_dict.values()),
            "gasto_caja": sum(e["totales_empresa"]["gasto_caja"] for e in empresas_dict.values()),
            "generales": sum(e["totales_empresa"]["generales"] for e in empresas_dict.values()),
            "otro_gasto": sum(e["totales_empresa"]["otro_gasto"] for e in empresas_dict.values()),
            "chapisteria": sum(e["totales_empresa"]["chapisteria"] for e in empresas_dict.values()),
            "almacen": sum(e["totales_empresa"]["almacen"] for e in empresas_dict.values()),
            "utilidad": sum(e["totales_empresa"]["utilidad"] for e in empresas_dict.values()),
            "perdida": sum(e["totales_empresa"]["perdida"] for e in empresas_dict.values()),
            "avance": sum(e["totales_empresa"]["avance"] for e in empresas_dict.values())
        }

    # Construir la respuesta final
    response = {
        "empresas": empresas_dict,
        "totales": totales_generales,
        "fechas": {
            "primeraFecha": data.primeraFecha,
            "ultimaFecha": data.ultimaFecha
        },
        "usuario": usuario,
        "fecha": fecha,
        "hora": hora_actual,
    }

    headers = {
      "Content-Disposition": "inline; estado-perdidas-ganancias.pdf"
    }  

    # return JSONResponse(status_code=200, content=jsonable_encoder(response))

    data_reporte = response

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "EstadoPyG2.html"
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
    pdf_path = 'estado-perdidas-ganancias.pdf'
    html2pdf(titulo,html_path, pdf_path, header_path=header_path, footer_path=footer_path)

    response = FileResponse(pdf_path, media_type='application/pdf', filename='templates/estado-perdidas-ganancias.pdf', headers=headers)

    return response
  except Exception as e:
    return JSONResponse(status_code=500, content={"error": str(e)})
  finally:
    db.close()
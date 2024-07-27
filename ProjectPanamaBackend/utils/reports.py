def fun_conteo_vehiculos_estados(data):
    if not data:
        return {"mensaje": "No hay datos"}
    
    conteo_placas = {}
    for vehiculo in data:
        estado = vehiculo.get("nombre")
        if estado in conteo_placas:
            conteo_placas[estado] += 1
        else:
            conteo_placas[estado] = 1

    # Devolver solo el conteo de placas
    return {"conteo_placas": conteo_placas}

#------------------------------------------------------------

def obtener_conteo_por_propietario(data):
    if not data:
        return {"mensaje": "No hay datos"}

    conteo_por_empresa = {}
    for vehiculo in data:
        codigo_empresa = vehiculo.get("propietario_codigo")
        nombre_empresa = vehiculo.get("propietario_nombre")
        if codigo_empresa not in conteo_por_empresa:
            conteo_por_empresa[codigo_empresa] = {"nombre_empresa": nombre_empresa}
        estado = vehiculo.get("estado_nombre")
        if estado in conteo_por_empresa[codigo_empresa]:
            conteo_por_empresa[codigo_empresa][estado] += 1
        else:
            conteo_por_empresa[codigo_empresa][estado] = 1

    # Crear un nuevo diccionario con las claves modificadas
    conteo_total_por_empresa = {}
    for empresa, conteo_estado in conteo_por_empresa.items():
        total_por_empresa = sum(int(conteo_estado.get(estado, 0)) for estado in conteo_estado if estado != "nombre_empresa")
        conteo_total_por_empresa[empresa] = {"Total": total_por_empresa, **conteo_estado}

    return {"conteo_por_empresa": conteo_total_por_empresa}

#------------------------------------------------------------

def obtener_numeros_por_estado(data):
    if not data:
        return {"mensaje": "No hay datos"}

    conteo_por_estado = {}
    for vehiculo in data:
        estado = vehiculo.get("estado_nombre")
        numero_vehiculo = vehiculo.get("vehiculo_numero")
        if estado in conteo_por_estado:
            conteo_por_estado[estado].append(numero_vehiculo)
        else:
            conteo_por_estado[estado] = [numero_vehiculo]

    # Ordenar las listas de números de vehículos para cada estado
    for estado in conteo_por_estado:
        conteo_por_estado[estado].sort()

    return {"numeros_por_estado": conteo_por_estado}


#------------------------------------------------------------

def obtener_numeros_por_propietario(data):
    if not data:
        return {"mensaje": "No hay datos"}

    conteo_por_empresa = {}
    for vehiculo in data:
        codigo_empresa = vehiculo.get("propietario_codigo")
        nombre_empresa = vehiculo.get("propietario_nombre")
        numero_vehiculo = vehiculo.get("vehiculo_numero")

        if codigo_empresa not in conteo_por_empresa:
            conteo_por_empresa[codigo_empresa] = {"nombre_empresa": nombre_empresa}
        estado = vehiculo.get("estado_nombre")
        if estado in conteo_por_empresa[codigo_empresa]:
            conteo_por_empresa[codigo_empresa][estado].append(numero_vehiculo)
        else:
            conteo_por_empresa[codigo_empresa][estado] = [numero_vehiculo]

    return {"numeros_por_propietario": conteo_por_empresa}

#------------------------------------------------------------
def obtener_conductores_por_propietario(data, codigos_estados_deseados=None):
    cuotas_por_propietario = {}
    for vehiculo in data:
        codigo_propietario = vehiculo["propietario_codigo"]
        if codigo_propietario not in cuotas_por_propietario:
            cuotas_por_propietario[codigo_propietario] = {
                "propietario_codigo": vehiculo["propietario_codigo"],
                "propietario_nombre": vehiculo["propietario_nombre"],
                "empty": "1",
                "estados": {}  # Nuevo diccionario para almacenar los estados
            }
        if vehiculo["conductor_codigo"]:
            estado = vehiculo["estado_nombre"]
            if codigos_estados_deseados is None or not codigos_estados_deseados or vehiculo["estado_codigo"] in codigos_estados_deseados:
                if estado not in cuotas_por_propietario[codigo_propietario]["estados"]:
                    cuotas_por_propietario[codigo_propietario]["estados"][estado] = {
                        "estado_codigo": vehiculo["estado_codigo"],
                        "estado_nombre": estado,
                        "empty": "0"
                    }  # Crea un diccionario para el estado si aún no existe
                cuotas_por_propietario[codigo_propietario]["estados"][estado][vehiculo["vehiculo_numero"]] = vehiculo
                cuotas_por_propietario[codigo_propietario]["empty"] = "0"
    return cuotas_por_propietario

#------------------------------------------------------------

def cuotas_pagas(data, codigos_estados_deseados=None):
    cuotas_por_propietario = {}
    for vehiculo in data:
        codigo_propietario = vehiculo["propietario_codigo"]
        if codigo_propietario not in cuotas_por_propietario:
            cuotas_por_propietario[codigo_propietario] = {
                "propietario_codigo": vehiculo["propietario_codigo"],
                "propietario_nombre": vehiculo["propietario_nombre"],
                "empty": "1"  # Inicialmente, asumimos que solo hay "propietario_codigo" y "propietario_nombre"
            }
        if vehiculo["conductor_codigo"]:
            if codigos_estados_deseados is None or not codigos_estados_deseados:
                cuotas_por_propietario[codigo_propietario][vehiculo["vehiculo_numero"]] = vehiculo
                cuotas_por_propietario[codigo_propietario]["empty"] = "0"  # Hay más datos además de "propietario_codigo" y "propietario_nombre"
            elif vehiculo["estado_codigo"] in codigos_estados_deseados:
                cuotas_por_propietario[codigo_propietario][vehiculo["vehiculo_numero"]] = vehiculo
                cuotas_por_propietario[codigo_propietario]["empty"] = "0"  # Hay más datos además de "propietario_codigo" y "propietario_nombre"
    return cuotas_por_propietario

#------------------------------------------------------------

def obtener_nombre_estado(estado):
    if estado == 0:
        return "Sin clasificar"
    elif estado == 1:
        return "Activo"
    elif estado == 2:
        return "Suspendido"
    elif estado == 3:
        return "Inactivo"
    else:
        return "Desconocido"

def agrupar_empresas_por_estado(empresas):
    empresas_por_estado = {}
    for empresa in empresas:
        estado = empresa["propietario_estado"]
        if estado not in empresas_por_estado:
            empresas_por_estado[estado] = {}
            empresas_por_estado[estado]["nombre_estado"] = obtener_nombre_estado(estado)
        codigo = empresa["propietario_codigo"]
        empresas_por_estado[estado][codigo] = empresa
    return empresas_por_estado

#------------------------------------------------------------

def obtener_nombre_estado_conductor(estado):
    if estado == "0":
        return "Sin clasificar"
    elif estado == "1":
        return "Activo"
    elif estado == "2":
        return "Suspendido"
    elif estado == "3":
        return "Retirado"
    elif estado == "4":
        return "Reportado"
    else:
        return "Desconocido"

def agrupar_conductores_por_estado(conductores):
    conductores_por_estado = {}
    for conductor in conductores:
        estado = conductor["conductor_estado"]
        if estado not in conductores_por_estado:
            conductores_por_estado[estado] = {}
            conductores_por_estado[estado]["nombre_estado"] = obtener_nombre_estado_conductor(estado)
        codigo = conductor["conductor_codigo"]
        conductores_por_estado[estado][codigo] = conductor
    return conductores_por_estado

#------------------------------------------------------------

def agrupar_vehiculos_por_estado(vehiculos):
    vehiculos_por_estado_nombre = {}
    for vehiculo in vehiculos:
        estado_nombre = vehiculo["vehiculo_estado_nombre"]
        if estado_nombre not in vehiculos_por_estado_nombre:
            vehiculos_por_estado_nombre[estado_nombre] = {}
        placa = vehiculo["vehiculo_placa"]
        vehiculos_por_estado_nombre[estado_nombre][placa] = vehiculo
    return vehiculos_por_estado_nombre

#------------------------------------------------------------

def valor_compra_vehiculos(data):
    vehiculos_por_propietario = {}

    for vehiculo in data:
        propietario_codigo = vehiculo["propietario_codigo"]
        if propietario_codigo not in vehiculos_por_propietario:
            vehiculos_por_propietario[propietario_codigo] = {
                "propietario_codigo": propietario_codigo,
                "vehiculo_empresa": vehiculo["vehiculo_empresa"],
                "empty": "1",
                "vehiculos": {}
            }

        vehiculo_unidad = vehiculo["vehiculo_unidad"]
        fecha_compra = vehiculo["vehiculo_fecha_compra"]
        if fecha_compra == "0000-00-00":
            fecha_compra = ""

        vehiculos_por_propietario[propietario_codigo]["vehiculos"][vehiculo_unidad] = {
            "vehiculo_unidad": vehiculo_unidad,
            "vehiculo_placa": vehiculo["vehiculo_placa"],
            "vehiculo_marca": vehiculo["vehiculo_marca"],
            "vehiculo_linea": vehiculo["vehiculo_linea"],
            "vehiculo_modelo": vehiculo["vehiculo_modelo"],
            "vehiculo_cupo": vehiculo["vehiculo_cupo"],
            "vehiculo_motor": vehiculo["vehiculo_motor"],
            "vehiculo_chasis": vehiculo["vehiculo_chasis"],
            "vehiculo_estado": vehiculo["vehiculo_estado"],
            "vehiculo_valor_compra": vehiculo["vehiculo_valor_compra"],
            "vehiculo_fecha_compra": fecha_compra  # Usar la fecha modificada
        }
        vehiculos_por_propietario[propietario_codigo]["empty"] = "0"

    return vehiculos_por_propietario

#------------------------------------------------------------

def check_owner_records(owner):
    return {
        'vehiculo': owner['vehiculo'] is not None,
        'cajarecaudos': owner['cajarecaudos'] is not None,
        'cajarecaudoscontado': owner['cajarecaudoscontado'] is not None,
        'cartera': owner['cartera'] is not None,
        'movienca': owner['movienca'] is not None
    }
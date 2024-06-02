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
        nombre_empresa = vehiculo.get("propietario_abreviado")
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
        nombre_empresa = vehiculo.get("propietario_abreviado")
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
                "propietario_abreviado": vehiculo["propietario_abreviado"],
                "empty": "1"  # Inicialmente, asumimos que solo hay "propietario_codigo" y "propietario_abreviado"
            }
        if vehiculo["conductor_codigo"]:
            if codigos_estados_deseados is None or not codigos_estados_deseados:
                cuotas_por_propietario[codigo_propietario][vehiculo["vehiculo_numero"]] = vehiculo
                cuotas_por_propietario[codigo_propietario]["empty"] = "0"  # Hay más datos además de "propietario_codigo" y "propietario_abreviado"
            elif vehiculo["estado_codigo"] in codigos_estados_deseados:
                cuotas_por_propietario[codigo_propietario][vehiculo["vehiculo_numero"]] = vehiculo
                cuotas_por_propietario[codigo_propietario]["empty"] = "0"  # Hay más datos además de "propietario_codigo" y "propietario_abreviado"
    return cuotas_por_propietario

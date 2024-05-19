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

    return {"conteo_por_empresa": conteo_por_empresa}
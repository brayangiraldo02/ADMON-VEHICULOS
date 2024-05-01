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
        empresa = vehiculo.get("empresa")
        estado = vehiculo.get("nombre")
        if empresa not in conteo_por_empresa:
            conteo_por_empresa[empresa] = {}
        if estado in conteo_por_empresa[empresa]:
            conteo_por_empresa[empresa][estado] += 1
        else:
            conteo_por_empresa[empresa][estado] = 1

    # Consolidar los conteos por empresa
    conteo_total_por_empresa = {}
    for empresa, conteo_estado in conteo_por_empresa.items():
        total_por_empresa = sum(conteo_estado.values())
        conteo_total_por_empresa[empresa] = {"Total": total_por_empresa, **conteo_estado}

    # Devolver el conteo de placas por empresa
    return {"conteo_por_empresa": conteo_total_por_empresa}
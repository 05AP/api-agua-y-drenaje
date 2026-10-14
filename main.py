from fastapi import FastAPI, HTTPException, status, Query
from typing import Optional
from datetime import datetime
import schemas
import database

# Inicialización de la aplicación FastAPI con metadatos para Swagger
app = FastAPI(
    title="API REST - Servicios de Agua y Drenaje",
    description="Sistema de gestión de clientes, lecturas de consumo de agua y facturación.",
    version="1.0.0"
)


# ============================================================
# MÓDULO 1: GESTIÓN DE CLIENTES
# ============================================================

@app.get(
    "/v1/api/clientes",
    response_model=schemas.ClientesListResponse,
    status_code=status.HTTP_200_OK,
    tags=["Clientes"],
    summary="Consultar todos los clientes"
)
def obtener_clientes():
    """
    Retorna la lista de todos los clientes registrados.
    Cumple con el requerimiento del examen:
    - Indicador de éxito.
    - Total de clientes.
    - Lista de clientes.
    """
    return {
        "success": True,
        "total": len(database.clientes),
        "data": database.clientes
    }


@app.get(
    "/v1/api/clientes/{id_cliente}",
    response_model=schemas.ClienteResponse,
    status_code=status.HTTP_200_OK,
    tags=["Clientes"],
    summary="Consultar un cliente por su ID"
)
def obtener_cliente_por_id(id_cliente: int):
    """
    Permite consultar un cliente específico.
    Lanza error 404 si el cliente no existe.
    """
    cliente = database.buscar_cliente(id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {id_cliente} no encontrado."
        )
    return cliente


@app.post(
    "/v1/api/clientes",
    response_model=schemas.ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Clientes"],
    summary="Registrar un nuevo cliente"
)
def crear_cliente(cliente_data: schemas.ClienteCreate):
    """
    Registra un nuevo cliente en el sistema.
    - Valida tipos de datos y restricciones mediante Pydantic.
    - Verifica que el ID no se encuentre duplicado.
    """
    # 1. Validar si ya existe un cliente con ese ID
    if database.buscar_cliente(cliente_data.id_cliente):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un cliente registrado con el ID {cliente_data.id_cliente}."
        )

    # 2. Convertir el modelo a diccionario y almacenarlo en memoria
    nuevo_cliente = cliente_data.model_dump()
    database.clientes.append(nuevo_cliente)

    return nuevo_cliente


@app.put(
    "/v1/api/clientes/{id_cliente}",
    response_model=schemas.ClienteResponse,
    status_code=status.HTTP_200_OK,
    tags=["Clientes"],
    summary="Actualizar la información de un cliente"
)
def actualizar_cliente(id_cliente: int, datos_actualizados: schemas.ClienteUpdate):
    """
    Actualiza parcialmente o totalmente la información de un cliente.
    Si el cliente no existe, lanza un error 404.
    """
    cliente = database.buscar_cliente(id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede actualizar: Cliente con ID {id_cliente} no existe."
        )

    # Actualizar solo los campos que fueron enviados en la petición
    if datos_actualizados.nombre_cliente is not None:
        cliente["nombre_cliente"] = datos_actualizados.nombre_cliente

    if datos_actualizados.direccion is not None:
        cliente["direccion"] = datos_actualizados.direccion

    if datos_actualizados.active is not None:
        cliente["active"] = datos_actualizados.active

    return cliente


@app.delete(
    "/v1/api/clientes/{id_cliente}",
    status_code=status.HTTP_200_OK,
    tags=["Clientes"],
    summary="Desactivar un cliente (Baja Lógica)"
)
def desactivar_cliente(id_cliente: int):
    """
    REGLA DE ORO DEL EXAMEN:
    Los clientes NO se eliminan físicamente (no se hace remove/pop).
    Se realiza un borrado lógico cambiando 'active = False'.
    """
    cliente = database.buscar_cliente(id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede desactivar: Cliente con ID {id_cliente} no existe."
        )

    # Realizamos la baja lógica solicitada
    cliente["active"] = False

    return {
        "success": True,
        "message": f"El cliente {id_cliente} ({cliente['nombre_cliente']}) ha sido desactivado exitosamente.",
        "cliente": cliente
    }

# ============================================================
# MÓDULO 2: GESTIÓN DE TARIFA
# ============================================================

@app.get(
    "/v1/api/tarifa",
    response_model=schemas.TarifaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tarifa"],
    summary="Consultar la tarifa actual por m³"
)
def consultar_tarifa():
    """
    Retorna la tarifa activa que se utiliza para calcular el total a pagar.
    Valor inicial por defecto: 0.50.
    """
    return {
        "tarifa_actual": database.obtener_tarifa()
    }


@app.put(
    "/v1/api/tarifa",
    response_model=schemas.TarifaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tarifa"],
    summary="Actualizar la tarifa por m³"
)
def actualizar_tarifa(tarifa_data: schemas.TarifaUpdate):
    """
    Actualiza la tarifa vigente en el sistema.
    - Pydantic valida automáticamente que la tarifa sea mayor o igual a 0.0 (ge=0.0).
    - Los cálculos posteriores de consumos y reportes reflejarán este nuevo valor.
    """
    nueva_tarifa = database.fijar_tarifa(tarifa_data.tarifa)
    
    return {
        "tarifa_actual": nueva_tarifa
    }

# ============================================================
# MÓDULO 3: GESTIÓN DE CONSUMOS DE AGUA
# ============================================================

@app.get(
    "/v1/api/consumos",
    response_model=list[schemas.ConsumoResponse],
    status_code=status.HTTP_200_OK,
    tags=["Consumos de Agua"],
    summary="Consultar todas las lecturas de consumo"
)
def obtener_consumos():
    """
    Retorna el historial completo de lecturas de agua registradas en memoria.
    """
    return database.consumos


@app.post(
    "/v1/api/consumos",
    response_model=schemas.ConsumoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Consumos de Agua"],
    summary="Registrar una nueva lectura de consumo"
)
def registrar_consumo(consumo_data: schemas.ConsumoCreate):
    """
    Registra una lectura de consumo cumpliendo las reglas del examen:
    1. Verifica que el ID del consumo no esté duplicado.
    2. Valida que el cliente exista (404 si no existe).
    3. Valida que el cliente esté activo (400 si está inactivo).
    4. Asigna fecha automática si no se proporciona.
    """
    # 1. Validar unicidad del id_consumo
    if database.buscar_consumo(consumo_data.id_consumo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una lectura con el ID {consumo_data.id_consumo}."
        )

    # 2. Validar existencia del cliente asociado
    cliente = database.buscar_cliente(consumo_data.id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede registrar consumo: El cliente con ID {consumo_data.id_cliente} no existe."
        )

    # 3. REGLA CLAVE: Solo se pueden registrar consumos para clientes activos
    if not cliente["active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operación denegada: El cliente {cliente['nombre_cliente']} está inactivo (active = False)."
        )

    # 4. Manejo de fecha: si no se envió en el JSON, se establece la fecha y hora actual
    datos_consumo = consumo_data.model_dump()
    if datos_consumo.get("fecha_registro") is None:
        datos_consumo["fecha_registro"] = datetime.now()

    database.consumos.append(datos_consumo)
    return datos_consumo


@app.put(
    "/v1/api/consumos/{id_consumo}",
    response_model=schemas.ConsumoResponse,
    status_code=status.HTTP_200_OK,
    tags=["Consumos de Agua"],
    summary="Actualizar una lectura de consumo existente"
)
def actualizar_consumo(id_consumo: int, datos_actualizados: schemas.ConsumoUpdate):
    """
    Actualiza los valores de una lectura existente.
    Reglas del examen:
    - Valida que el consumo exista.
    - No permite actualizar consumos si el cliente asociado está inactivo.
    """
    # 1. Validar que la lectura exista
    consumo = database.buscar_consumo(id_consumo)
    if not consumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura de consumo con ID {id_consumo} no encontrada."
        )

    # 2. Validar estado del cliente asociado
    cliente = database.buscar_cliente(consumo["id_cliente"])
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente asociado (ID {consumo['id_cliente']}) no existe."
        )

    # REGLA CLAVE: No puedes actualizar un consumo cuyo cliente esté inactivo
    if not cliente["active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede actualizar el consumo: El cliente asociado ({cliente['nombre_cliente']}) se encuentra inactivo."
        )

    # 3. Actualizar campos enviados
    if datos_actualizados.consumo_agua is not None:
        consumo["consumo_agua"] = datos_actualizados.consumo_agua

    if datos_actualizados.fecha_registro is not None:
        consumo["fecha_registro"] = datos_actualizados.fecha_registro

    return consumo


# ============================================================
# MÓDULO 4: REPORTE Y FACTURACIÓN CON FILTRO DE FECHAS
# ============================================================

@app.get(
    "/v1/api/reportes/consumos",
    response_model=schemas.ReporteResponse,
    status_code=status.HTTP_200_OK,
    tags=["Reportes y Facturación"],
    summary="Generar reporte de consumos y cobros (solo clientes activos)"
)
def generar_reporte_consumos(
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha inicio filtro (ej. 2026-01-01T00:00:00)"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha fin filtro (ej. 2026-12-31T23:59:59)")
):
    """
    Genera el reporte financiero de consumos:
    - Muestra ÚNICAMENTE registros pertenecientes a clientes activos.
    - Incluye datos del cliente, consumo, fecha y tarifa vigente.
    - Calcula en tiempo real: total_pagar = consumo_agua * tarifa_actual.
    - Permite filtrar registros por rango de fechas (fecha_inicio y fecha_fin).
    """
    tarifa_vigente = database.obtener_tarifa()
    reporte_resultado = []

    for item in database.consumos:
        # Obtenemos el cliente dueño de la lectura
        cliente = database.buscar_cliente(item["id_cliente"])

        # REGLA DEL EXAMEN: Mostrar únicamente información correspondiente a clientes activos
        if not cliente or not cliente["active"]:
            continue

        fecha_lectura = item["fecha_registro"]

        # Filtro de rango de fechas
        if fecha_inicio and fecha_lectura < fecha_inicio:
            continue
        if fecha_fin and fecha_lectura > fecha_fin:
            continue

        # Cálculo de facturación solicitado por el examen
        total_a_pagar = round(item["consumo_agua"] * tarifa_vigente, 2)

        reporte_resultado.append({
            "id_cliente": cliente["id_cliente"],
            "nombre_cliente": cliente["nombre_cliente"],
            "direccion": cliente["direccion"],
            "consumo_agua": item["consumo_agua"],
            "fecha_registro": fecha_lectura,
            "tarifa": tarifa_vigente,
            "total_pagar": total_a_pagar
        })

    return {
        "success": True,
        "total_registros": len(reporte_resultado),
        "data": reporte_resultado
    }
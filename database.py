from datetime import datetime

# Tarifa base inicial definida por el examen
tarifa_actual: float = 0.50

# Estructuras de datos principales
clientes = [
    {
        "id_cliente": 1,
        "nombre_cliente": "Juan Pérez",
        "direccion": "Av. Constitución 100, Monterrey",
        "active": True
    },
    {
        "id_cliente": 2,
        "nombre_cliente": "María García",
        "direccion": "Calle Hidalgo 250, San Nicolás",
        "active": False
    }
]

consumos = [
    {
        "id_consumo": 1,
        "id_cliente": 1,
        "consumo_agua": 15.5,
        "fecha_registro": datetime(2026, 10, 1, 10, 30, 0)
    }
]


# FUNCIONES AUXILIARES DE GESTIÓN Y BÚSQUEDA

def obtener_tarifa() -> float:
    """Retorna la tarifa actual por m3."""
    return tarifa_actual


def fijar_tarifa(nueva_tarifa: float) -> float:
    """Actualiza la tarifa global en memoria."""
    global tarifa_actual
    tarifa_actual = nueva_tarifa
    return tarifa_actual


def buscar_cliente(id_cliente: int) -> dict | None:
    """
    Busca un cliente por su ID único.
    Retorna el diccionario del cliente o None si no existe.
    """
    for cliente in clientes:
        if cliente["id_cliente"] == id_cliente:
            return cliente
    return None


def buscar_consumo(id_consumo: int) -> dict | None:
    """
    Busca un registro de consumo por su ID único.
    Retorna el diccionario de la lectura o None si no existe.
    """
    for consumo in consumos:
        if consumo["id_consumo"] == id_consumo:
            return consumo
    return None

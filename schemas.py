from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ============================================================
# 1. MODELOS DE CLIENTES
# ============================================================

class ClienteBase(BaseModel):
    nombre_cliente: str = Field(..., min_length=2, description="Nombre completo del cliente")
    direccion: str = Field(..., min_length=5, description="Dirección domiciliaria")


class ClienteCreate(ClienteBase):
    id_cliente: int = Field(..., gt=0, description="Identificador único del cliente")
    active: bool = Field(default=True, description="Estado del contrato (activo/inactivo)")


class ClienteUpdate(BaseModel):
    nombre_cliente: Optional[str] = Field(None, min_length=2)
    direccion: Optional[str] = Field(None, min_length=5)
    active: Optional[bool] = None


class ClienteResponse(ClienteBase):
    id_cliente: int
    active: bool


# Respuesta estructurada para GET /v1/api/clientes según requerimiento del examen
class ClientesListResponse(BaseModel):
    success: bool = True
    total: int
    data: List[ClienteResponse]


# ============================================================
# 2. MODELOS DE CONSUMO DE AGUA
# ============================================================

class ConsumoBase(BaseModel):
    id_cliente: int = Field(..., gt=0, description="ID del cliente asociado")
    consumo_agua: float = Field(..., ge=0.0, description="Consumo en m3 (no puede ser negativo)")


class ConsumoCreate(ConsumoBase):
    id_consumo: int = Field(..., gt=0, description="Identificador único del consumo")
    # Si el usuario no envía fecha_registro, se genera automáticamente con la fecha y hora actual
    fecha_registro: Optional[datetime] = Field(
        default_factory=datetime.now, 
        description="Fecha y hora de lectura (ISO 8601)"
    )


class ConsumoUpdate(BaseModel):
    consumo_agua: Optional[float] = Field(None, ge=0.0, description="Nuevo consumo en m3")
    fecha_registro: Optional[datetime] = Field(None, description="Nueva fecha de lectura")


class ConsumoResponse(ConsumoBase):
    id_consumo: int
    fecha_registro: datetime


# ============================================================
# 3. MODELOS DE TARIFA
# ============================================================

class TarifaUpdate(BaseModel):
    tarifa: float = Field(..., ge=0.0, description="Tarifa por m3 (no puede ser negativa)")


class TarifaResponse(BaseModel):
    tarifa_actual: float


# ============================================================
# 4. MODELOS DE REPORTE Y FACTURACIÓN
# ============================================================

class ReporteItemResponse(BaseModel):
    id_cliente: int
    nombre_cliente: str
    direccion: str
    consumo_agua: float
    fecha_registro: datetime
    tarifa: float
    total_pagar: float


class ReporteResponse(BaseModel):
    success: bool = True
    total_registros: int
    data: List[ReporteItemResponse]
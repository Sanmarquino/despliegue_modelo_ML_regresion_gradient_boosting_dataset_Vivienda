"""Contrato de validación de datos (Pydantic v2) para la API de viviendas."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ViviendaEntrada(BaseModel):
    """Esquema de entrada con rangos numéricos y categorías permitidas."""

    # 8 Variables Numéricas con sus rangos válidos
    OverallQual: int = Field(
        ...,
        ge=1,
        le=10,
        description="Calidad general de materiales y acabados de la vivienda (1 a 10).",
    )
    GrLivArea: float = Field(
        ...,
        ge=334.0,
        le=5642.0,
        description="Área habitable sobre el nivel del suelo en pies cuadrados (334 a 5642).",
    )
    GarageCars: int = Field(
        ...,
        ge=0,
        le=4,
        description="Capacidad del garaje en número de autos (0 a 4).",
    )
    TotalBsmtSF: float = Field(
        ...,
        ge=0.0,
        le=6110.0,
        description="Área total del sótano en pies cuadrados (0 a 6110).",
    )
    FullBath: int = Field(
        ...,
        ge=0,
        le=3,
        description="Número de baños completos sobre el nivel del suelo (0 a 3).",
    )
    YearBuilt: int = Field(
        ...,
        ge=1872,
        le=2010,
        description="Año original de construcción de la vivienda (1872 a 2010).",
    )
    YearRemodAdd: int = Field(
        ...,
        ge=1950,
        le=2010,
        description="Año de remodelación o adición (1950 a 2010).",
    )
    LotArea: float = Field(
        ...,
        ge=1300.0,
        le=215245.0,
        description="Superficie total del lote en pies cuadrados (1300 a 215245).",
    )

    # 4 Variables Categóricas con sus valores estrictamente permitidos
    KitchenQual: Literal["Ex", "Gd", "TA", "Fa"] = Field(
        ...,
        description="Calidad de la cocina: Ex (Excelente), Gd (Buena), TA (Típica/Promedio), Fa (Regular).",
    )
    ExterQual: Literal["Ex", "Gd", "TA", "Fa"] = Field(
        ...,
        description="Calidad del material exterior: Ex, Gd, TA, Fa.",
    )
    CentralAir: Literal["Y", "N"] = Field(
        ...,
        description="Aire acondicionado central: Y (Sí) o N (No).",
    )
    Neighborhood: Literal[
        "Blmngtn", "Blueste", "BrDale", "BrkSide", "ClearCr",
        "CollgCr", "Crawfor", "Edwards", "Gilbert", "IDOTRR",
        "MeadowV", "Mitchel", "NAmes", "NPkVill", "NWAmes",
        "NoRidge", "NridgHt", "OldTown", "SWISU", "Sawyer",
        "SawyerW", "Somerst", "StoneBr", "Timber", "Veenker"
    ] = Field(
        ...,
        description="Vecindario físico dentro de la ciudad de Ames (25 vecindarios válidos).",
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "OverallQual": 6,
                "GrLivArea": 1068.0,
                "GarageCars": 1,
                "TotalBsmtSF": 1059.0,
                "FullBath": 1,
                "YearBuilt": 1963,
                "YearRemodAdd": 2003,
                "LotArea": 8414.0,
                "KitchenQual": "TA",
                "ExterQual": "TA",
                "CentralAir": "Y",
                "Neighborhood": "Sawyer",
            }
        },
    )


class PrediccionRespuesta(BaseModel):
    """Esquema de salida para el endpoint POST /predecir."""

    prediccion_usd: float = Field(..., description="Precio estimado de venta en USD.")
    moneda: str = Field(default="USD", description="Moneda de la estimación.")
    algoritmo: str = Field(..., description="Modelo utilizado en el pipeline.")
    r2_test_referencia: float = Field(..., description="R2 del modelo en datos no vistos.")
    fecha_entrenamiento: str = Field(..., description="Fecha UTC de entrenamiento del bundle.")
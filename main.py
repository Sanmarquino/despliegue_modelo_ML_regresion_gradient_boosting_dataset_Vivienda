"""API REST con FastAPI para servir el modelo de predicción de precios de viviendas."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from esquemas import PrediccionRespuesta, ViviendaEntrada

RUTA_BUNDLE = Path(__file__).resolve().parent / "modelo_bundle_viviendas.joblib"
bundle_activo: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el bundle .joblib una sola vez al iniciar el servidor."""
    if not RUTA_BUNDLE.exists():
        raise FileNotFoundError(f"No se encontró el bundle en: {RUTA_BUNDLE}")
    datos_cargados = joblib.load(RUTA_BUNDLE)
    bundle_activo.update(datos_cargados)
    yield
    bundle_activo.clear()


app = FastAPI(
    title="API de Predicción de Precios de Viviendas",
    description=(
        "Servicio de inferencia en producción basado en un Pipeline de "
        "GradientBoostingRegressor entrenado sobre Ames Housing (12 variables)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
def inicio() -> dict[str, Any]:
    """Endpoint 1: Bienvenida, estado general y rutas disponibles de la API."""
    return {
        "mensaje": "API de Predicción de Precios de Viviendas operativa.",
        "estado": "activo",
        "modelo_cargado": bool(bundle_activo),
        "endpoints": {
            "raiz": "GET /",
            "informacion_y_salud": "GET /info",
            "prediccion": "POST /predecir",
            "documentacion_interactiva": "GET /docs",
        },
    }


@app.get("/info", tags=["Salud y Metadatos"])
@app.get("/health", tags=["Salud y Metadatos"], include_in_schema=False)
def info_modelo() -> dict[str, Any]:
    """Endpoint 2: Salud del servicio y metadatos completos del bundle."""
    if not bundle_activo:
        raise HTTPException(status_code=503, detail="El bundle del modelo no está cargado.")

    return {
        "status": "ok",
        "tipo_problema": bundle_activo.get("tipo_problema", "regresion"),
        "algoritmo": bundle_activo.get("algoritmo", "GradientBoostingRegressor"),
        "target": bundle_activo.get("target", "SalePrice"),
        "columnas_entrada": bundle_activo["columnas"],
        "total_columnas": len(bundle_activo["columnas"]),
        "valores_validos": bundle_activo["valores_validos"],
        "metricas": bundle_activo["metricas"],
        "fecha_entrenamiento": bundle_activo["fecha_entrenamiento"],
        "versiones_librerias": bundle_activo["versiones_librerias"],
    }


@app.post("/predecir", response_model=PrediccionRespuesta, tags=["Inferencia"])
def predecir_precio(datos: ViviendaEntrada) -> PrediccionRespuesta:
    """Endpoint 3: Recibe las 12 variables validadas y retorna el precio estimado en USD."""
    if not bundle_activo:
        raise HTTPException(status_code=503, detail="El modelo no está disponible.")

    modelo = bundle_activo["modelo"]
    columnas_ordenadas = bundle_activo["columnas"]

    # Convertimos el payload validado a DataFrame respetando el orden exacto de columnas
    registro_dict = datos.model_dump()
    df_entrada = pd.DataFrame([registro_dict])[columnas_ordenadas]

    try:
        prediccion = float(modelo.predict(df_entrada)[0])
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno durante la inferencia del pipeline: {exc}",
        ) from exc

    return PrediccionRespuesta(
        prediccion_usd=round(prediccion, 2),
        moneda="USD",
        algoritmo=bundle_activo.get("algoritmo", "GradientBoostingRegressor"),
        r2_test_referencia=bundle_activo["metricas"]["r2_test"],
        fecha_entrenamiento=bundle_activo["fecha_entrenamiento"],
    )
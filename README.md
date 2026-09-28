# Despliegue de Modelo de Machine Learning en Producción — Precios de Viviendas

**Autor:** Daniel Humberto Llanos Llanos 
 
**Arquitectura:** Scikit-Learn Pipeline + Joblib + Pydantic v2 + FastAPI + Docker (`python:3.14-slim`)

Proyecto *end-to-end* de Ciencia de Datos y MLOps para estimar el precio de venta de viviendas (`SalePrice` en USD) utilizando un `Pipeline` de **Scikit-Learn (`GradientBoostingRegressor`)**, validación estricta de contratos de entrada con **Pydantic v2**, servicio API REST con **FastAPI** y contenedorización con **Docker**.

---

## 1. Métricas del Modelo Ganador (Datos No Vistos — Test 20%)

Se entrenaron y evaluaron tres algoritmos sobre una base de **1,460 viviendas** (`1,168` de entrenamiento y `292` de prueba no vista) utilizando **12 variables clave** (8 numéricas y 4 categóricas):

| Modelo Evaluado | $R^2$ CV (5-Fold) | $R^2$ Test (No Visto) | RMSE Test (USD) | MAE Test (USD) | Decisión |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Ridge Regression** | 0.8057 | 0.8491 (84.9%) | $34,021.16 | $20,894.90 | Descartado |
| **Random Forest** | 0.8249 | 0.8967 (89.7%) | $28,150.22 | $17,845.96 | Competitivo |
| **Gradient Boosting (Ganador)** | **0.8462** | **0.9162 (91.6%)** | **$25,348.27** | **$16,587.64** | **Seleccionado** |

---

## 2. Estructura de Entregables en el Repositorio

* **`Entrenamiento_Modelo_Viviendas.ipynb`**: Notebook con la selección de variables, entrenamiento del `Pipeline`, evaluación en datos no vistos, creación del bundle `.joblib` y verificación de predicción idéntica (`$139,223.61 USD`).
* **`modelo_bundle_viviendas.joblib`**: Artefacto serializado que empaqueta el modelo entrenado, las 12 columnas, los rangos y valores válidos, las métricas, la fecha de entrenamiento (UTC) y las versiones de las librerías.
* **`esquemas.py`**: Contrato de validación en Pydantic v2 (`ViviendaEntrada` y `PrediccionRespuesta`) con control de rangos numéricos y categorías permitidas.
* **`main.py`**: API REST en FastAPI con tres endpoints (`GET /`, `GET /info` y `POST /predecir`).
* **`requirements.txt`**: Versiones exactas del entorno de producción (`scikit-learn==1.9.1`, `fastapi==0.141.1`, `pydantic==2.13.5`, `joblib==1.6.0`).
* **`Dockerfile`**: Receta del contenedor sobre imagen oficial ligera `python:3.14-slim`.
* **`Informe Ejecutivo.pdf` y `capturas_despliegue_modelo_ganador.pdf`**: Documentación ejecutiva y evidencias de las pruebas en `/docs` (respuestas `200 OK`, validación `422 Unprocessable Content` y ejecución del contenedor Docker).

---

## 3. Ejecución del Contenedor con Docker

```bash
# 1. Construir la imagen Docker
docker build -t api-viviendas:v1 .

# 2. Ejecutar el contenedor en segundo plano exponiendo el puerto 8000
docker run -d -p 8000:8000 --name contenedor-viviendas api-viviendas:v1
```

Una vez iniciado el contenedor, la documentación interactiva (Swagger UI) se encuentra disponible en:  
`http://localhost:8000/docs`
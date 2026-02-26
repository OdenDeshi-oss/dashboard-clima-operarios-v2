"""
loader.py - Carga y preprocesamiento de encuesta + inventario.
"""

from pathlib import Path

import pandas as pd
import streamlit as st
from core.mappings import (
    LIKERT_QUESTIONS,
    CARGOS_OPERARIOS,
    get_scale_map,
)

# Ruta base del proyecto (donde está app.py)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


@st.cache_data
def load_encuesta(path: str | None = None) -> pd.DataFrame:
    """Carga la encuesta y agrega columnas numéricas Likert."""
    filepath = Path(path) if path else DATA_DIR / "encuesta.xlsx"
    df = pd.read_excel(filepath)

    # Crear columna numérica para cada pregunta Likert
    for q in LIKERT_QUESTIONS:
        col_text = q["col"]
        col_num = f"_likert_{q['key']}"
        scale_map = get_scale_map(q["scale"])
        df[col_num] = df[col_text].map(scale_map)

    return df


@st.cache_data
def load_inventario(path: str | None = None) -> pd.DataFrame:
    """Carga el inventario, limpia whitespace y filtra solo operarios válidos."""
    filepath = Path(path) if path else DATA_DIR / "inventario.xlsx"
    df = pd.read_excel(filepath)

    # Limpiar espacios en columnas de texto clave
    for col in ["CARGO", "CLIENTE", "UNIDAD", "DEPARTAMENTO"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Filtrar solo cargos de operarios
    df = df[df["CARGO"].isin(CARGOS_OPERARIOS)].copy()

    return df

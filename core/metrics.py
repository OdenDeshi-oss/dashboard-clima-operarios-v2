"""
metrics.py - Cálculo de KPIs, NPS y participación.
"""

import pandas as pd
from core.mappings import LIKERT_QUESTIONS


def _likert_col(key: str) -> str:
    """Retorna el nombre de la columna numérica Likert."""
    return f"_likert_{key}"


def get_likert_numeric_cols() -> list[str]:
    """Lista de columnas numéricas Likert."""
    return [_likert_col(q["key"]) for q in LIKERT_QUESTIONS]


def total_respuestas(df: pd.DataFrame) -> int:
    return len(df)


def inventario_operarios(df_inv: pd.DataFrame) -> int:
    return len(df_inv)


def participacion(respuestas: int, inventario: int) -> float:
    """% de participación. Retorna 0 si inventario es 0."""
    if inventario == 0:
        return 0.0
    return (respuestas / inventario) * 100


def promedio_general_likert(df: pd.DataFrame) -> float:
    """Promedio de todas las preguntas Likert sobre todos los registros."""
    cols = get_likert_numeric_cols()
    values = df[cols].values.flatten()
    values = values[~pd.isna(values)]
    if len(values) == 0:
        return 0.0
    return float(values.mean())


def indice_satisfaccion(df: pd.DataFrame) -> float:
    """Top-2 Box: % de respuestas que son 4 o 5."""
    cols = get_likert_numeric_cols()
    values = df[cols].values.flatten()
    values = values[~pd.isna(values)]
    if len(values) == 0:
        return 0.0
    top2 = sum(1 for v in values if v >= 4)
    return (top2 / len(values)) * 100


def calcular_nps(df: pd.DataFrame) -> dict:
    """
    NPS basado en escala 1-5:
      - Detractores: 1-2
      - Pasivos: 3
      - Promotores: 4-5
    NPS = %Promotores - %Detractores
    Usa la pregunta "Limtek buen lugar" como base para NPS.
    """
    col = _likert_col("Limtek buen lugar")
    values = df[col].dropna()
    total = len(values)

    if total == 0:
        return {"nps": 0.0, "promotores": 0, "pasivos": 0, "detractores": 0,
                "pct_promotores": 0.0, "pct_pasivos": 0.0, "pct_detractores": 0.0,
                "total": 0}

    detractores = int((values <= 2).sum())
    pasivos = int((values == 3).sum())
    promotores = int((values >= 4).sum())

    pct_prom = (promotores / total) * 100
    pct_det = (detractores / total) * 100
    pct_pas = (pasivos / total) * 100
    nps = pct_prom - pct_det

    return {
        "nps": round(nps, 1),
        "promotores": promotores,
        "pasivos": pasivos,
        "detractores": detractores,
        "pct_promotores": round(pct_prom, 1),
        "pct_pasivos": round(pct_pas, 1),
        "pct_detractores": round(pct_det, 1),
        "total": total,
    }


def promedio_por_pregunta(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna un DataFrame con promedio por cada pregunta Likert."""
    rows = []
    for q in LIKERT_QUESTIONS:
        col = _likert_col(q["key"])
        vals = df[col].dropna()
        prom = float(vals.mean()) if len(vals) > 0 else 0.0
        n = len(vals)
        rows.append({
            "Pregunta": q["key"],
            "Columna original": q["col"],
            "Promedio": round(prom, 2),
            "Respuestas": n,
        })
    return pd.DataFrame(rows)


def ranking_mejor_peor(df: pd.DataFrame) -> tuple[dict, dict]:
    """Retorna la mejor y peor pregunta por promedio."""
    df_prom = promedio_por_pregunta(df)
    if df_prom.empty:
        empty = {"Pregunta": "N/A", "Promedio": 0}
        return empty, empty
    mejor = df_prom.loc[df_prom["Promedio"].idxmax()].to_dict()
    peor = df_prom.loc[df_prom["Promedio"].idxmin()].to_dict()
    return mejor, peor


def distribucion_pregunta(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """Distribución de respuestas para una pregunta Likert individual."""
    col = _likert_col(key)
    counts = df[col].dropna().value_counts().sort_index()
    total = counts.sum()
    result = pd.DataFrame({
        "Valor": counts.index.astype(int),
        "Frecuencia": counts.values,
        "Porcentaje": (counts.values / total * 100).round(1) if total > 0 else 0,
    })
    return result

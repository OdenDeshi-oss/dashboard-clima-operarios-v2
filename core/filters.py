"""
filters.py - Lógica de filtros para encuesta e inventario.
Filtros entrelazados dinámicos: cada filtro recalcula las opciones de los otros dos.
Todas las opciones salen exclusivamente de df_enc.
"""

import pandas as pd
from core.mappings import COL_CLIENTE_ENC, COL_UNIDAD_ENC, COL_DEPTO_ENC


def apply_encuesta_filters(
    df: pd.DataFrame,
    cliente: str | None,
    unidad: str | None,
    departamento: str | None,
) -> pd.DataFrame:
    """Filtra el dataframe de encuesta por cliente, unidad y departamento."""
    out = df.copy()
    if cliente and cliente != "Todos":
        out = out[out[COL_CLIENTE_ENC] == cliente]
    if unidad and unidad != "Todos":
        out = out[out[COL_UNIDAD_ENC] == unidad]
    if departamento and departamento != "Todos":
        out = out[out[COL_DEPTO_ENC] == departamento]
    return out


def apply_inventario_filters(
    df: pd.DataFrame,
    cliente: str | None,
    unidad: str | None,
    departamento: str | None,
) -> pd.DataFrame:
    """Filtra el dataframe de inventario por cliente, unidad y departamento."""
    out = df.copy()
    if cliente and cliente != "Todos":
        out = out[out["CLIENTE"] == cliente]
    if unidad and unidad != "Todos":
        out = out[out["UNIDAD"] == unidad]
    if departamento and departamento != "Todos":
        out = out[out["DEPARTAMENTO"] == departamento]
    return out


def get_filter_options(
    df_enc: pd.DataFrame, df_inv: pd.DataFrame
) -> dict[str, list[str]]:
    """
    Genera las opciones de filtro usando exclusivamente df_enc.
    Firma original conservada por compatibilidad (df_inv se ignora).
    """
    clientes = sorted(df_enc[COL_CLIENTE_ENC].dropna().unique())
    unidades = sorted(df_enc[COL_UNIDAD_ENC].dropna().unique())
    departamentos = sorted(df_enc[COL_DEPTO_ENC].dropna().unique())
    return {
        "clientes": ["Todos"] + clientes,
        "unidades": ["Todos"] + unidades,
        "departamentos": ["Todos"] + departamentos,
    }


def get_dynamic_filter_options(
    df_enc: pd.DataFrame,
    sel_cliente: str,
    sel_depto: str,
    sel_unidad: str,
) -> dict[str, list[str]]:
    """
    Filtros entrelazados bidireccionales.
    Para cada filtro, calcula opciones válidas basándose en los OTROS dos filtros.
    Usa exclusivamente datos de df_enc.

    Ejemplo:
      - Opciones de Cliente = clientes únicos en df_enc filtrado por Depto + Unidad actuales
      - Opciones de Depto = deptos únicos en df_enc filtrado por Cliente + Unidad actuales
      - Opciones de Unidad = unidades únicas en df_enc filtrado por Cliente + Depto actuales
    """
    # ── Opciones para CLIENTE (filtrar por depto + unidad) ───
    df_c = df_enc.copy()
    if sel_depto and sel_depto != "Todos":
        df_c = df_c[df_c[COL_DEPTO_ENC] == sel_depto]
    if sel_unidad and sel_unidad != "Todos":
        df_c = df_c[df_c[COL_UNIDAD_ENC] == sel_unidad]
    clientes = ["Todos"] + sorted(df_c[COL_CLIENTE_ENC].dropna().unique())

    # ── Opciones para DEPARTAMENTO (filtrar por cliente + unidad) ─
    df_d = df_enc.copy()
    if sel_cliente and sel_cliente != "Todos":
        df_d = df_d[df_d[COL_CLIENTE_ENC] == sel_cliente]
    if sel_unidad and sel_unidad != "Todos":
        df_d = df_d[df_d[COL_UNIDAD_ENC] == sel_unidad]
    departamentos = ["Todos"] + sorted(df_d[COL_DEPTO_ENC].dropna().unique())

    # ── Opciones para UNIDAD (filtrar por cliente + depto) ───
    df_u = df_enc.copy()
    if sel_cliente and sel_cliente != "Todos":
        df_u = df_u[df_u[COL_CLIENTE_ENC] == sel_cliente]
    if sel_depto and sel_depto != "Todos":
        df_u = df_u[df_u[COL_DEPTO_ENC] == sel_depto]
    unidades = ["Todos"] + sorted(df_u[COL_UNIDAD_ENC].dropna().unique())

    return {
        "clientes": clientes,
        "departamentos": departamentos,
        "unidades": unidades,
    }

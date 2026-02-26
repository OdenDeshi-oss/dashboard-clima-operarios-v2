"""
kpis.py - Componente UI para mostrar KPIs principales.
"""

import streamlit as st
from core.metrics import (
    total_respuestas,
    inventario_operarios,
    participacion,
    promedio_general_likert,
    indice_satisfaccion,
    calcular_nps,
)
import pandas as pd


def render_kpis(df_enc: pd.DataFrame, df_inv: pd.DataFrame) -> None:
    """Renderiza los 6 KPIs principales en una fila."""
    resp = total_respuestas(df_enc)
    inv = inventario_operarios(df_inv)
    part = participacion(resp, inv)
    prom = promedio_general_likert(df_enc)
    sat = indice_satisfaccion(df_enc)
    nps_data = calcular_nps(df_enc)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.metric("📋 Total respuestas", f"{resp:,}")
    with c2:
        st.metric("👷 Inventario operarios", f"{inv:,}")
    with c3:
        st.metric("📊 Participación", f"{part:.1f}%")
    with c4:
        st.metric("⭐ Promedio Likert", f"{prom:.2f} / 5")
    with c5:
        st.metric("😊 Satisfacción (Top-2)", f"{sat:.1f}%")
    with c6:
        nps_val = nps_data["nps"]
        st.metric("📈 NPS", f"{nps_val:+.1f}")


def render_nps_detail(df_enc: pd.DataFrame) -> None:
    """Renderiza detalle del NPS con desglose."""
    nps_data = calcular_nps(df_enc)

    st.markdown("#### 📈 Detalle NPS")
    st.caption("Base: *Considero a Limtek como un buen lugar para trabajar* · Detractores (1-2) · Pasivos (3) · Promotores (4-5)")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("NPS", f"{nps_data['nps']:+.1f}")
    with c2:
        st.metric("🟢 Promotores", f"{nps_data['promotores']} ({nps_data['pct_promotores']}%)")
    with c3:
        st.metric("🟡 Pasivos", f"{nps_data['pasivos']} ({nps_data['pct_pasivos']}%)")
    with c4:
        st.metric("🔴 Detractores", f"{nps_data['detractores']} ({nps_data['pct_detractores']}%)")

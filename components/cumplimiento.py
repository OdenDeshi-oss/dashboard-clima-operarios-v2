"""
cumplimiento.py - Indicadores dinámicos de cumplimiento según filtros activos.
Solo se muestra cuando hay al menos un filtro activo.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.mappings import COL_CLIENTE_ENC, COL_UNIDAD_ENC, COL_DEPTO_ENC

AZUL = "#000064"
AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"
BLANCO = "#FFFFFF"
GRIS = "#c8c8e0"


def _build_cumplimiento_table(
    df_enc: pd.DataFrame,
    df_inv: pd.DataFrame,
    group_col_enc: str,
    group_col_inv: str,
) -> pd.DataFrame:
    """
    Construye tabla de cumplimiento cruzando encuesta e inventario
    agrupados por una columna común (Unidad, Cliente, etc.).
    """
    inv_counts = (
        df_inv.groupby(group_col_inv)
        .size()
        .reset_index(name="Inventario")
    )
    inv_counts.rename(columns={group_col_inv: "Grupo"}, inplace=True)

    enc_counts = (
        df_enc.groupby(group_col_enc)
        .size()
        .reset_index(name="Respuestas")
    )
    enc_counts.rename(columns={group_col_enc: "Grupo"}, inplace=True)

    merged = inv_counts.merge(enc_counts, on="Grupo", how="left").fillna(0)
    merged["Respuestas"] = merged["Respuestas"].astype(int)
    merged["% Cumplimiento"] = (
        (merged["Respuestas"] / merged["Inventario"]) * 100
    ).round(1)
    merged = merged.sort_values("% Cumplimiento", ascending=False).reset_index(drop=True)

    return merged


def render_cumplimiento(
    df_enc: pd.DataFrame,
    df_inv: pd.DataFrame,
    df_enc_raw: pd.DataFrame,
    df_inv_raw: pd.DataFrame,
    sel_cliente: str,
    sel_depto: str,
    sel_unidad: str,
) -> None:
    """Renderiza indicadores de cumplimiento solo si hay filtro activo."""
    has_cliente = sel_cliente and sel_cliente != "Todos"
    has_depto = sel_depto and sel_depto != "Todos"
    has_unidad = sel_unidad and sel_unidad != "Todos"

    if not (has_cliente or has_depto or has_unidad):
        return  # No mostrar nada sin filtros

    st.markdown(
        '<p class="section-title">📌 Cumplimiento de participación</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#FFFFFF; font-size:1.07rem; margin:-10px 0 12px 0;">'
        'Comparación entre el inventario de operarios registrados y el total de respuestas recibidas '
        'según el filtro activo. Muestra el nivel de participación por unidad.'
        '</p>',
        unsafe_allow_html=True,
    )

    # ── Bloque informativo del filtro activo ─────────────────
    total_inv = len(df_inv)
    total_resp = len(df_enc)
    pct = round((total_resp / total_inv) * 100, 1) if total_inv > 0 else 0.0

    filtros_activos = []
    if has_cliente:
        filtros_activos.append(f"Cliente: **{sel_cliente}**")
    if has_depto:
        filtros_activos.append(f"Departamento: **{sel_depto}**")
    if has_unidad:
        filtros_activos.append(f"Unidad: **{sel_unidad}**")

    filtro_label = " · ".join(filtros_activos)
    st.markdown(filtro_label)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("👷 Inventario operarios", f"{total_inv:,}")
    with c2:
        st.metric("📋 Respondieron", f"{total_resp:,}")
    with c3:
        st.metric("📊 Nivel de cumplimiento", f"{pct}%")

    # ── Tabla de cumplimiento por unidad ─────────────────────
    if has_unidad:
        # Solo unidad seleccionada: no hay desglose adicional
        return

    # Si hay cliente o departamento, desglosar por unidad
    table = _build_cumplimiento_table(
        df_enc, df_inv, COL_UNIDAD_ENC, "UNIDAD"
    )

    if table.empty:
        return

    # Renombrar columna Grupo
    desglose_label = "Unidad"
    if has_depto and not has_cliente:
        desglose_label = f"Unidad (en {sel_depto})"
    elif has_cliente and not has_depto:
        desglose_label = f"Unidad (de {sel_cliente})"
    elif has_cliente and has_depto:
        desglose_label = f"Unidad"

    table.rename(columns={"Grupo": desglose_label}, inplace=True)

    st.markdown(f"**Desglose por unidad** ({len(table)} unidades)")

    # Gráfico horizontal top 15
    df_plot = table.head(15).sort_values("% Cumplimiento", ascending=True)

    max_pct = df_plot["% Cumplimiento"].max()
    colors = [
        AMARILLO if p == max_pct else AZUL_LIGHT
        for p in df_plot["% Cumplimiento"]
    ]

    fig = go.Figure(go.Bar(
        x=df_plot["% Cumplimiento"],
        y=df_plot[desglose_label],
        orientation="h",
        text=[
            f"{p}% ({int(r)} / {int(i)})"
            for p, r, i in zip(
                df_plot["% Cumplimiento"],
                df_plot["Respuestas"],
                df_plot["Inventario"],
            )
        ],
        textposition="outside",
        textfont=dict(color=BLANCO, size=11),
        marker_color=colors,
        marker_line=dict(width=0),
        cliponaxis=False,
    ))
    max_pct = df_plot["% Cumplimiento"].max()
    fig.update_layout(
        height=max(250, len(df_plot) * 35 + 60),
        margin=dict(t=5, b=25, l=10, r=120),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, max_pct * 1.3],
        ),
        yaxis=dict(
            tickfont=dict(color=BLANCO, size=11),
            gridcolor="rgba(0,0,0,0)",
        ),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Tabla completa en expander
    with st.expander(f"📋 Tabla completa ({len(table)} unidades)", expanded=False):
        st.dataframe(
            table,
            hide_index=True,
            use_container_width=True,
            height=400,
        )

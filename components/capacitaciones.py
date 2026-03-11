"""
capacitaciones.py - Componente UI para análisis de capacitaciones.
Fondo blanco, colores corporativos, tabla desplegable.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.mappings import CAPACITACION_COLS

AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"


def render_capacitaciones(df_enc: pd.DataFrame) -> None:
    """Renderiza conteo y porcentaje de capacitaciones seleccionadas."""
    st.markdown(
        '<p class="section-title">🎓 Capacitaciones solicitadas</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#FFFFFF; font-size:1.07rem; margin:-10px 0 12px 0;">'
        'Temas de capacitación seleccionados por los operarios en la encuesta. '
        'Muestra la cantidad de solicitudes y su porcentaje sobre el total de encuestados.'
        '</p>',
        unsafe_allow_html=True,
    )

    total_encuestados = len(df_enc)
    rows = []

    for col in CAPACITACION_COLS:
        if col == "Otro (especifique)":
            count = int(df_enc[col].dropna().shape[0])
        else:
            count = int(df_enc[col].notna().sum())
        pct = round((count / total_encuestados) * 100, 1) if total_encuestados > 0 else 0.0
        rows.append({"Capacitación": col, "Cantidad": count, "Porcentaje (%)": pct})

    df_cap = pd.DataFrame(rows).sort_values("Cantidad", ascending=True)

    max_cant = df_cap["Cantidad"].max()
    colors = [AMARILLO if c == max_cant else AZUL_LIGHT for c in df_cap["Cantidad"]]

    fig = go.Figure(go.Bar(
        x=df_cap["Cantidad"],
        y=df_cap["Capacitación"],
        orientation="h",
        text=[f"  {int(c)}  ({p}%)" for c, p in zip(df_cap["Cantidad"], df_cap["Porcentaje (%)"])],
        textposition="outside",
        textfont=dict(color="#333333", size=12),
        marker_color=colors,
        marker_line=dict(width=1, color="#FFFFFF"),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=10, b=20, l=10, r=120),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, max_cant * 1.35],
        ),
        yaxis=dict(
            tickfont=dict(color="#333333", size=12),
            gridcolor="rgba(0,0,0,0)",
        ),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with st.expander("📋 Tabla de capacitaciones", expanded=False):
        st.dataframe(
            df_cap.sort_values("Cantidad", ascending=False),
            hide_index=True,
            use_container_width=True,
        )

    otros = df_enc["Otro (especifique)"].dropna()
    if len(otros) > 0:
        with st.expander(f"📝 Respuestas \"Otro\" ({len(otros)})", expanded=False):
            st.dataframe(
                otros.reset_index(drop=True).to_frame(name="Respuesta"),
                hide_index=True,
                use_container_width=True,
            )

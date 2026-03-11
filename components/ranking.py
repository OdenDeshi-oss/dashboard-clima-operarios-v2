"""
ranking.py - Componente UI para ranking mejor/peor pregunta + tabla general.
Fondo blanco, colores corporativos, tabla desplegable.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.metrics import promedio_por_pregunta, ranking_mejor_peor

AZUL = "#000064"
AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"


def render_ranking(df_enc: pd.DataFrame) -> None:
    """Renderiza ranking de preguntas: mejor, peor y gráfico."""
    st.markdown(
        '<p class="section-title">🏆 Ranking de preguntas Likert</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#FFFFFF; font-size:1.07rem; margin:-10px 0 12px 0;">'
        'Promedio de satisfacción por dimensión evaluada en la encuesta de clima laboral (escala 1–5). '
        'Destaca la mejor y peor dimensión según la percepción de los operarios.'
        '</p>',
        unsafe_allow_html=True,
    )

    mejor, peor = ranking_mejor_peor(df_enc)

    c1, c2 = st.columns(2)
    with c1:
        st.success(f"🥇 **Mejor:** {mejor['Pregunta']} — **{mejor['Promedio']:.2f}**")
    with c2:
        st.error(f"🥉 **Peor:** {peor['Pregunta']} — **{peor['Promedio']:.2f}**")

    df_prom = promedio_por_pregunta(df_enc).sort_values("Promedio", ascending=True)

    max_prom = df_prom["Promedio"].max()
    colors = [AMARILLO if p == max_prom else AZUL_LIGHT for p in df_prom["Promedio"]]

    fig = go.Figure(go.Bar(
        x=df_prom["Promedio"],
        y=df_prom["Pregunta"],
        orientation="h",
        text=[f"  {p:.2f}" for p in df_prom["Promedio"]],
        textposition="outside",
        textfont=dict(color="#333333", size=13),
        marker_color=colors,
        marker_line=dict(width=1, color="#FFFFFF"),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=350,
        margin=dict(t=10, b=30, l=10, r=80),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(
            range=[0, 5.5],
            tickfont=dict(color="#888888", size=10),
            gridcolor="#ECECEC",
            zeroline=False,
            title="Promedio (1-5)",
            title_font=dict(color="#888888", size=11),
        ),
        yaxis=dict(
            tickfont=dict(color="#333333", size=12),
            gridcolor="rgba(0,0,0,0)",
        ),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with st.expander("📋 Tabla de promedios", expanded=False):
        st.dataframe(
            df_prom[["Pregunta", "Promedio", "Respuestas"]].sort_values("Promedio", ascending=False),
            hide_index=True,
            use_container_width=True,
        )

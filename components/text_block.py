"""
text_block.py - Componente UI para análisis de preguntas abiertas.
  - "¿Qué destacas?" → Bloques conceptuales + respuestas clasificadas
  - "¿Qué mejorar?"  → Bloques conceptuales + respuestas clasificadas
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.text_analysis import (
    bloques_conceptuales,
    bloques_conceptuales_mejorar,
    classify_responses_by_block,
    classify_responses_mejorar,
)

AZUL = "#000064"
AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"
BLANCO = "#FFFFFF"
GRIS = "#c8c8e0"


def _render_bloques_section(
    series: pd.Series,
    title: str,
    emoji: str,
    bloques_fn,
    classify_fn,
    color_scale: str,
) -> None:
    """Renderiza bloques conceptuales + texto clasificado para cualquier pregunta abierta."""
    st.markdown(
        f'<p class="section-title">{emoji} {title}</p>',
        unsafe_allow_html=True,
    )

    df_bloques = bloques_fn(series)
    total_resp = int(series.dropna().shape[0])

    if df_bloques.empty or total_resp == 0:
        st.info("Sin datos de texto para analizar.")
        return

    top_bloque = df_bloques.iloc[0]

    c1, c2 = st.columns(2)
    with c1:
        st.metric("🏆 Bloque más mencionado", top_bloque["Bloque"])
    with c2:
        st.metric("💬 Total respuestas analizadas", f"{total_resp:,}")

    # ── Gráfico de barras horizontal ─────────────────────────
    df_plot = df_bloques.sort_values("Menciones", ascending=True)
    max_menciones = df_plot["Menciones"].max()

    colors = [
        AMARILLO if m == max_menciones else AZUL_LIGHT
        for m in df_plot["Menciones"]
    ]

    fig = go.Figure(go.Bar(
        x=df_plot["Menciones"],
        y=df_plot["Bloque"],
        orientation="h",
        text=[
            f"  {int(m)}  ({p}%)"
            for m, p in zip(df_plot["Menciones"], df_plot["Porcentaje (%)"])
        ],
        textposition="outside",
        textfont=dict(color="#333333", size=13),
        marker_color=colors,
        marker_line=dict(width=1, color="#FFFFFF"),
        cliponaxis=False,
    ))
    max_m_val = df_plot["Menciones"].max()
    fig.update_layout(
        height=330,
        margin=dict(t=10, b=20, l=10, r=120),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, max_m_val * 1.35],
        ),
        yaxis=dict(
            tickfont=dict(color="#333333", size=12),
            gridcolor="rgba(0,0,0,0)",
        ),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Texto original clasificado por bloque ────────────────
    classified = classify_fn(series)

    with st.expander("📂 TEXTO ORIGINAL CLASIFICADO POR BLOQUE", expanded=False):
        ordered_blocks = df_bloques["Bloque"].tolist()

        tab_labels = [
            f"{bloque} ({len(classified.get(bloque, []))})"
            for bloque in ordered_blocks
        ]
        tabs = st.tabs(tab_labels)

        for tab, bloque in zip(tabs, ordered_blocks):
            with tab:
                responses = classified.get(bloque, [])
                st.markdown(
                    f"**{bloque}** — {len(responses)} respuestas clasificadas",
                )
                if not responses:
                    st.caption("Sin respuestas en este bloque.")
                    continue

                html_items = "".join(
                    f"<p>• {resp}</p>" for resp in responses
                )
                st.markdown(
                    f'<div class="text-scroll-container">{html_items}</div>',
                    unsafe_allow_html=True,
                )


def render_text_blocks(df_enc: pd.DataFrame, col_destacar: str, col_mejorar: str) -> None:
    """Renderiza ambos bloques de texto separados."""
    _render_bloques_section(
        series=df_enc[col_destacar],
        title="¿Qué destacas de Limtek?",
        emoji="🌟",
        bloques_fn=bloques_conceptuales,
        classify_fn=classify_responses_by_block,
        color_scale="Greens",
    )

    st.divider()

    _render_bloques_section(
        series=df_enc[col_mejorar],
        title="¿Qué tendría que mejorar Limtek?",
        emoji="🔧",
        bloques_fn=bloques_conceptuales_mejorar,
        classify_fn=classify_responses_mejorar,
        color_scale="Oranges",
    )

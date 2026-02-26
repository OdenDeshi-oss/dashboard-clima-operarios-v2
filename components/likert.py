"""
likert.py - Componente UI para detalle individual por pregunta Likert.
Barras verticales, orden 5→1, fondo blanco, KPI grande al costado.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.mappings import LIKERT_QUESTIONS
from core.metrics import distribucion_pregunta, promedio_por_pregunta

# Paleta corporativa por valor Likert
COLOR_MAP = {
    5: "#000064",
    4: "#3355AA",
    3: "#A0A0B0",
    2: "#E8943A",
    1: "#CC4444",
}

ETIQUETAS_CORTAS = {
    5: "Totalmente<br>de acuerdo",
    4: "Parcialmente<br>de acuerdo",
    3: "Neutral",
    2: "Parcialmente<br>en desacuerdo",
    1: "Totalmente<br>en desacuerdo",
}

AMARILLO = "#FFB239"
AZUL = "#000064"
BLANCO = "#FFFFFF"


def render_likert_detail(df_enc: pd.DataFrame) -> None:
    """Renderiza detalle individual de cada pregunta Likert."""
    st.markdown(
        '<p class="section-title">📊 Detalle por pregunta Likert</p>',
        unsafe_allow_html=True,
    )

    df_prom = promedio_por_pregunta(df_enc)

    for _, row in df_prom.iterrows():
        key = row["Pregunta"]
        col_orig = row["Columna original"]
        prom = row["Promedio"]
        n = row["Respuestas"]
        # Top-2 Box per question
        likert_col = f"_likert_{key}"
        if likert_col in df_enc.columns:
            vals = df_enc[likert_col].dropna()
            top2 = int((vals >= 4).sum())
            pct_satisf = round((top2 / len(vals)) * 100, 1) if len(vals) > 0 else 0.0
        else:
            pct_satisf = round((prom / 5) * 100, 1)

        # ── Título ───────────────────────────────────────────
        st.markdown(
            f"""<div style="
                background: rgba(13,13,107,0.6);
                border: 1px solid #1a1a7a;
                border-left: 4px solid {AMARILLO};
                border-radius: 6px;
                padding: 10px 16px;
                margin: 24px 0 4px 0;
            ">
                <span style="color:{BLANCO}; font-weight:600; font-size:1.05rem;">
                    {key}
                </span>
            </div>
            <p style="color:#8888aa; font-size:0.82rem; margin:2px 0 10px 0;">
                {col_orig}
            </p>""",
            unsafe_allow_html=True,
        )

        dist = distribucion_pregunta(df_enc, key)
        if dist.empty:
            st.info("Sin datos.")
            continue

        # ── Layout: gráfico (izq) + KPI (der) ───────────────
        col_chart, col_kpi = st.columns([3, 1])

        with col_chart:
            orden = [5, 4, 3, 2, 1]
            dist_map = dict(zip(dist["Valor"].astype(int), zip(dist["Frecuencia"], dist["Porcentaje"])))

            freqs, colors, labels, texts = [], [], [], []
            for v in orden:
                if v in dist_map and dist_map[v][0] > 0:
                    f, p = dist_map[v]
                    freqs.append(int(f))
                    colors.append(COLOR_MAP[v])
                    labels.append(ETIQUETAS_CORTAS[v])
                    texts.append(f"<b>{int(f)}</b> ({round(p, 1)}%)")

            # Calcular margen superior dinámico para que el texto no se corte
            max_freq = max(freqs) if freqs else 1
            y_top = max_freq * 1.35

            fig = go.Figure(go.Bar(
                x=labels,
                y=freqs,
                text=texts,
                textposition="outside",
                textfont=dict(color="#333333", size=13, family="Arial"),
                marker_color=colors,
                marker_line=dict(width=1, color="#FFFFFF"),
                cliponaxis=False,
            ))
            fig.update_layout(
                height=340,
                margin=dict(t=40, b=10, l=10, r=10),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                xaxis=dict(
                    tickfont=dict(color="#333333", size=12, family="Arial"),
                    showgrid=False,
                    zeroline=False,
                    fixedrange=True,
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    fixedrange=True,
                    range=[0, y_top],
                ),
                bargap=0.25,
                uniformtext=dict(minsize=11, mode="show"),
            )
            st.plotly_chart(
                fig, use_container_width=True,
                config={"displayModeBar": False},
                key=f"likert_{key}",
            )

        with col_kpi:
            st.markdown(
                f"""<div style="
                    background: #FFFFFF !important;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                    border: 2px solid #CCCCCC;
                    border-radius: 10px;
                    padding: 20px 16px;
                    text-align: center;
                    margin-top: 10px;
                ">
                    <p style="color:#222222 !important; font-size:0.78rem; margin:0 0 4px 0; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;">
                        Promedio
                    </p>
                    <p style="color:#000064 !important; font-size:2.6rem; font-weight:800; margin:0; line-height:1.1;">
                        {prom:.2f}
                    </p>
                    <p style="color:#444444 !important; font-size:0.85rem; font-weight:500; margin:2px 0 12px 0;">
                        de 5.00
                    </p>
                    <hr style="border:none; border-top:2px solid #CCCCCC; margin:8px 0;">
                    <p style="color:#222222 !important; font-size:0.75rem; margin:0 0 2px 0; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;">
                        Satisfacción (Top-2)
                    </p>
                    <p style="color:#E8943A !important; font-size:1.6rem; font-weight:800; margin:0;">
                        {pct_satisf}%
                    </p>
                    <hr style="border:none; border-top:2px solid #CCCCCC; margin:8px 0;">
                    <p style="color:#222222 !important; font-size:0.75rem; margin:0 0 2px 0; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;">
                        Respuestas
                    </p>
                    <p style="color:#111111 !important; font-size:1.3rem; font-weight:700; margin:0;">
                        {n:,}
                    </p>
                </div>""",
                unsafe_allow_html=True,
            )

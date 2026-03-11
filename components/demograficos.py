"""
demograficos.py - Gráficos de WhatsApp y Tiempo en Limtek.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

AZUL = "#000064"
AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"
BLANCO = "#FFFFFF"
GRIS = "#c8c8e0"

COL_WHATSAPP = "¿Usas whatsapp en tu vida diaria?"
COL_TIEMPO = "¿Cuánto tiempo llevas trabajando en Limtek?"

ORDEN_TIEMPO = [
    "De 0 a 6 meses",
    "De 6 meses a 1 año",
    "De 1 a 2 años",
    "De 2 a 3 años",
    "De 3 años a más",
]


def render_demograficos(df_enc: pd.DataFrame) -> None:
    """Renderiza gráficos de WhatsApp y Tiempo en Limtek."""
    st.markdown(
        '<p class="section-title">📱 Perfil del encuestado</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#FFFFFF; font-size:1.07rem; margin:-10px 0 12px 0;">'
        'Características generales de los operarios que respondieron la encuesta: '
        'uso de WhatsApp en su vida diaria y antigüedad trabajando en Limtek.'
        '</p>',
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns(2)

    # ── WhatsApp (donut) ─────────────────────────────────────
    with col_left:
        st.markdown(
            f"""<div style="
                background: rgba(13,13,107,0.6);
                border: 1px solid #1a1a7a;
                border-left: 4px solid {AMARILLO};
                border-radius: 6px;
                padding: 8px 14px;
                margin-bottom: 8px;
            ">
                <span style="color:{BLANCO}; font-weight:600; font-size:0.95rem;">
                    ¿Usas WhatsApp en tu vida diaria?
                </span>
            </div>""",
            unsafe_allow_html=True,
        )

        wa = df_enc[COL_WHATSAPP].value_counts()
        total = wa.sum()

        # Calcular porcentajes para leyenda
        wa_labels = []
        for lab, val in zip(wa.index, wa.values):
            pct = round(val / total * 100, 1)
            wa_labels.append(f"{lab}: {val:,} ({pct}%)")

        fig_wa = go.Figure(go.Pie(
            labels=wa.index.tolist(),
            values=wa.values.tolist(),
            hole=0.5,
            textinfo="percent",
            textfont=dict(size=15, color=BLANCO),
            textposition="inside",
            marker=dict(
                colors=[AZUL, AMARILLO],
                line=dict(color="#FFFFFF", width=2),
            ),
            hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>",
        ))
        fig_wa.update_layout(
            height=320,
            margin=dict(t=10, b=10, l=10, r=10),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(color="#333333", size=13),
            ),
            annotations=[dict(
                text=f"<b>{total:,}</b><br><span style='font-size:11px'>resp.</span>",
                x=0.5, y=0.5, font_size=20, font_color="#333333",
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_wa, use_container_width=True, config={"displayModeBar": False}, key="chart_whatsapp")

        # Leyenda explícita debajo
        for lbl in wa_labels:
            st.markdown(f"<p style='color:#333333; text-align:center; margin:0; font-size:0.9rem;'>{lbl}</p>", unsafe_allow_html=True)

    # ── Tiempo en Limtek (barras verticales) ─────────────────
    with col_right:
        st.markdown(
            f"""<div style="
                background: rgba(13,13,107,0.6);
                border: 1px solid #1a1a7a;
                border-left: 4px solid {AMARILLO};
                border-radius: 6px;
                padding: 8px 14px;
                margin-bottom: 8px;
            ">
                <span style="color:{BLANCO}; font-weight:600; font-size:0.95rem;">
                    ¿Cuánto tiempo llevas trabajando en Limtek?
                </span>
            </div>""",
            unsafe_allow_html=True,
        )

        tiempo = df_enc[COL_TIEMPO].value_counts()
        total_t = tiempo.sum()

        labels, freqs, pcts = [], [], []
        for cat in ORDEN_TIEMPO:
            if cat in tiempo.index:
                f = int(tiempo[cat])
                labels.append(cat.replace("De ", "").replace(" a ", "-"))
                freqs.append(f)
                pcts.append(round(f / total_t * 100, 1))

        max_f = max(freqs) if freqs else 1
        colors = [AMARILLO if f == max_f else AZUL_LIGHT for f in freqs]

        fig_t = go.Figure(go.Bar(
            x=labels,
            y=freqs,
            text=[f"<b>{f}</b><br>({p}%)" for f, p in zip(freqs, pcts)],
            textposition="outside",
            textfont=dict(color="#333333", size=12),
            marker_color=colors,
            marker_line=dict(width=1, color="#FFFFFF"),
            cliponaxis=False,
        ))
        fig_t.update_layout(
            height=320,
            margin=dict(t=35, b=10, l=10, r=10),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            xaxis=dict(
                tickfont=dict(color="#333333", size=11),
                showgrid=False,
                zeroline=False,
                fixedrange=True,
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                fixedrange=True,
                range=[0, max_f * 1.25],
            ),
            bargap=0.25,
        )
        st.plotly_chart(fig_t, use_container_width=True, config={"displayModeBar": False}, key="chart_tiempo")

"""
Dashboard de Encuesta de Clima Laboral — OPERARIOS
Limtek Servicios Integrales
"""

import streamlit as st

from core.loader import load_encuesta, load_inventario
from core.filters import apply_encuesta_filters, apply_inventario_filters, get_filter_options, get_dynamic_filter_options
from core.mappings import COL_DESTACAR, COL_MEJORAR

from components.kpis import render_kpis, render_nps_detail
from components.ranking import render_ranking
from components.likert import render_likert_detail
from components.capacitaciones import render_capacitaciones
from components.text_block import render_text_blocks
from components.cumplimiento import render_cumplimiento
from components.demograficos import render_demograficos

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Clima Laboral — Operarios | Limtek",
    page_icon="📋",
    layout="wide",
)

# ── Corporate CSS ────────────────────────────────────────────
st.markdown("""
<style>
/* ── Variables ─────────────────────────────── */
:root {
    --azul: #000064;
    --azul-light: #0a0a80;
    --azul-surface: #0d0d6b;
    --amarillo: #FFB239;
    --blanco: #FFFFFF;
    --gris-text: #c8c8e0;
    --gris-border: #1a1a7a;
}

/* ── Main background ───────────────────────── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--azul) !important;
}
header[data-testid="stHeader"] {
    background-color: var(--azul) !important;
}

/* ── Sidebar ───────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #000050 !important;
    border-right: 1px solid var(--gris-border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--blanco) !important;
}
section[data-testid="stSidebar"] .stSelectbox label {
    color: var(--gris-text) !important;
    font-weight: 500;
}

/* ── Text colors ───────────────────────────── */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: var(--blanco) !important;
}
.stApp p, .stApp span, .stApp label, .stApp li, .stApp div {
    color: var(--gris-text) !important;
}
.stApp .stMarkdown {
    color: var(--gris-text) !important;
}

/* ── Metrics ───────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--azul-surface);
    border: 1px solid var(--gris-border);
    border-radius: 8px;
    padding: 12px 16px;
}
[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: var(--gris-text) !important;
}
[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
    color: var(--gris-text) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--blanco) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] div {
    color: var(--blanco) !important;
}

/* ── Dividers ──────────────────────────────── */
.stApp hr {
    border-color: var(--gris-border) !important;
    opacity: 0.5;
}

/* ── Expanders ─────────────────────────────── */
.stApp details {
    background: var(--azul-surface) !important;
    border: 1px solid var(--gris-border) !important;
    border-radius: 8px !important;
}
.stApp details summary {
    color: var(--blanco) !important;
}
.stApp details summary span {
    color: var(--blanco) !important;
}

/* ── DataFrames / tables ───────────────────── */
.stApp .stDataFrame {
    border: 1px solid var(--gris-border) !important;
    border-radius: 6px;
}

/* ── Success/Error boxes ───────────────────── */
.stApp .stAlert {
    background: var(--azul-surface) !important;
    border: 1px solid var(--gris-border) !important;
    color: var(--blanco) !important;
}
.stApp .stAlert p, .stApp .stAlert span, .stApp .stAlert strong {
    color: var(--blanco) !important;
}

/* ── Selectbox dropdowns ───────────────────── */
.stApp .stSelectbox > div > div {
    background-color: var(--azul-surface) !important;
    border-color: var(--gris-border) !important;
    color: var(--blanco) !important;
}

/* ── Section title underline accent ────────── */
.section-title {
    color: var(--blanco) !important;
    font-size: 1.3rem;
    font-weight: 600;
    padding-bottom: 6px;
    border-bottom: 3px solid var(--amarillo);
    display: inline-block;
    margin-bottom: 16px;
}

/* ── Tabs styling ──────────────────────────── */
.stApp .stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--azul-surface);
    border-radius: 8px;
    padding: 4px;
}
.stApp .stTabs [data-baseweb="tab"] {
    color: var(--gris-text) !important;
    background: transparent;
    border-radius: 6px;
    padding: 8px 16px;
}
.stApp .stTabs [aria-selected="true"] {
    background: var(--azul-light) !important;
    color: var(--amarillo) !important;
    border-bottom: 2px solid var(--amarillo) !important;
}
.stApp .stTabs [aria-selected="true"] p {
    color: var(--amarillo) !important;
}

/* ── Scrollable text containers ────────────── */
.text-scroll-container {
    max-height: 300px;
    overflow-y: auto;
    background: rgba(0,0,50,0.5);
    border: 1px solid var(--gris-border);
    border-radius: 6px;
    padding: 12px;
}
.text-scroll-container p {
    color: var(--gris-text) !important;
    font-size: 0.85rem;
    margin-bottom: 6px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(26,26,122,0.5);
}
</style>
""", unsafe_allow_html=True)

# ── Header with logo ────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGa7xFnFuRMmopHsst6MCpjR2VhLYMRL_-IQ&s"
         alt="Limtek" height="52"
         onerror="this.style.display='none'">
    <div>
        <h1 style="margin:0; color:#FFFFFF; font-size:1.8rem;">Dashboard Clima Laboral — Operarios</h1>
        <p style="margin:0; color:#FFB239; font-size:0.95rem; font-weight:500;">
            Limtek Servicios Integrales · Encuesta de Satisfacción
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Data load ────────────────────────────────────────────────
df_enc_raw = load_encuesta()
df_inv_raw = load_inventario()

# ── Sidebar filters ─────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGa7xFnFuRMmopHsst6MCpjR2VhLYMRL_-IQ&s"
         alt="Limtek" height="40"
         onerror="this.style.display='none'">
</div>
""", unsafe_allow_html=True)
st.sidebar.header("🔍 Filtros")

# ── Reset handler (debe ejecutarse ANTES de los widgets) ─────
if st.session_state.get("_reset_filters", False):
    st.session_state["_reset_filters"] = False
    st.session_state["f_cliente"] = "Todos"
    st.session_state["f_depto"] = "Todos"
    st.session_state["f_unidad"] = "Todos"

# ── Filtros entrelazados dinámicos ───────────────────────────
_cur_cliente = st.session_state.get("f_cliente", "Todos")
_cur_depto = st.session_state.get("f_depto", "Todos")
_cur_unidad = st.session_state.get("f_unidad", "Todos")

opts = get_dynamic_filter_options(df_enc_raw, _cur_cliente, _cur_depto, _cur_unidad)

if _cur_cliente not in opts["clientes"]:
    _cur_cliente = "Todos"
if _cur_depto not in opts["departamentos"]:
    _cur_depto = "Todos"
if _cur_unidad not in opts["unidades"]:
    _cur_unidad = "Todos"

sel_cliente = st.sidebar.selectbox(
    "Cliente", opts["clientes"],
    index=opts["clientes"].index(_cur_cliente),
    key="f_cliente",
)
sel_depto = st.sidebar.selectbox(
    "Departamento", opts["departamentos"],
    index=opts["departamentos"].index(_cur_depto),
    key="f_depto",
)
sel_unidad = st.sidebar.selectbox(
    "Unidad", opts["unidades"],
    index=opts["unidades"].index(_cur_unidad),
    key="f_unidad",
)

def _do_reset():
    st.session_state["_reset_filters"] = True

st.sidebar.button("🔄 Limpiar filtros", use_container_width=True, on_click=_do_reset)

# ── Apply filters ────────────────────────────────────────────
df_enc = apply_encuesta_filters(df_enc_raw, sel_cliente, sel_unidad, sel_depto)
df_inv = apply_inventario_filters(df_inv_raw, sel_cliente, sel_unidad, sel_depto)

# ── KPIs ─────────────────────────────────────────────────────
render_kpis(df_enc, df_inv)

st.divider()

# ── Cumplimiento (solo con filtro activo) ────────────────────
render_cumplimiento(df_enc, df_inv, df_enc_raw, df_inv_raw, sel_cliente, sel_depto, sel_unidad)

# ── NPS Detail ───────────────────────────────────────────────
render_nps_detail(df_enc)

st.divider()

# ── Ranking ──────────────────────────────────────────────────
render_ranking(df_enc)

st.divider()

# ── Detalle individual Likert ────────────────────────────────
render_likert_detail(df_enc)

st.divider()

# ── Capacitaciones ───────────────────────────────────────────
render_capacitaciones(df_enc)

st.divider()

# ── Perfil del encuestado (WhatsApp + Tiempo) ───────────────
render_demograficos(df_enc)

st.divider()

# ── Preguntas abiertas ───────────────────────────────────────
render_text_blocks(df_enc, COL_DESTACAR, COL_MEJORAR)

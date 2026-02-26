"""
text_analysis.py - Limpieza y análisis de frecuencia de palabras para preguntas abiertas.
"""

import re
from collections import Counter

import pandas as pd

# Stopwords español básicas
STOPWORDS = {
    "de", "la", "el", "en", "y", "a", "los", "las", "del", "un", "una",
    "que", "es", "se", "con", "por", "para", "al", "lo", "como", "más",
    "su", "me", "mi", "no", "si", "sus", "le", "les", "nos", "muy",
    "ya", "hay", "son", "pero", "ser", "está", "este", "esta", "todo",
    "todos", "toda", "todas", "hace", "tiene", "han", "fue", "hemos",
    "he", "ha", "o", "e", "u", "ni", "entre", "sobre", "sin", "desde",
    "hasta", "cada", "eso", "ese", "esa", "esos", "esas", "aquí", "ahí",
    "allí", "cuando", "donde", "mientras", "también", "otros", "otras",
    "otro", "otra", "mismo", "misma", "tan", "tanto", "tanta", "tantos",
    "tantas", "mucho", "mucha", "muchos", "muchas", "poco", "poca",
    "pocos", "pocas", "bien", "mal", "mejor", "peor", "bueno", "buena",
    "buenos", "buenas", "malo", "mala", "malos", "malas", "grande",
    "grandes", "pequeño", "pequeña", "nuevo", "nueva", "nuevos", "nuevas",
    "primer", "primero", "primera", "último", "última", "parte", "tiempo",
    "forma", "manera", "vez", "veces", "día", "días", "año", "años",
    "cosa", "cosas", "hombre", "mujer", "mundo", "vida", "casa", "vez",
    "así", "sí", "aún", "después", "antes", "siempre", "nunca", "nada",
    "algo", "alguien", "nadie", "aquello", "uno", "dos", "tres",
    "ser", "estar", "haber", "tener", "hacer", "poder", "deber",
    "ir", "dar", "ver", "saber", "querer", "llegar", "pasar",
    "dijo", "tipo", "era", "sido", "sea", "cual", "solo", "puede",
    "pueden", "hecho", "tiene", "van", "eso", "etc", "ellos", "ella",
    "él", "yo", "tú", "usted", "nosotros", "ustedes", "nos",
}


def clean_text(text: str) -> list[str]:
    """Limpia un texto y retorna lista de palabras válidas."""
    text = text.lower()
    text = re.sub(r"[^a-záéíóúüñ\s]", "", text)
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def word_frequency(series: pd.Series) -> pd.DataFrame:
    """
    Calcula frecuencia de palabras desde una serie de textos.
    Retorna DataFrame con columnas: Palabra, Frecuencia, Porcentaje.
    """
    all_words: list[str] = []
    for text in series.dropna():
        all_words.extend(clean_text(str(text)))

    total = len(all_words)
    counter = Counter(all_words)

    if not counter:
        return pd.DataFrame(columns=["Palabra", "Frecuencia", "Porcentaje"])

    df = pd.DataFrame(
        counter.most_common(),
        columns=["Palabra", "Frecuencia"],
    )
    df["Porcentaje"] = (df["Frecuencia"] / total * 100).round(1)
    return df


# ── Bloques conceptuales para "¿Qué destacas?" ──────────────
import unicodedata

BLOQUES_DESTACAR: dict[str, list[str]] = {
    "Pagos y puntualidad": [
        "pago", "pagos", "puntual", "puntualidad", "puntuales",
        "sueldo", "salario", "quincena",
    ],
    "Ambiente laboral": [
        "ambiente", "clima", "laboral", "compañerismo", "companerismo",
        "equipo", "respeto", "trato", "apoyo",
    ],
    "Estabilidad y formalidad": [
        "formal", "planilla", "estabilidad", "contrato", "seguridad",
    ],
    "Liderazgo": [
        "supervisor", "jefe", "liderazgo", "comunicacion", "apoyo del jefe",
    ],
    "Crecimiento": [
        "crecimiento", "oportunidad", "aprendizaje", "capacitacion", "desarrollo",
    ],
    "Identificación": [
        "empresa", "orgullo", "recomendable", "me gusta", "buena empresa",
    ],
}

# ── Bloques conceptuales para "¿Qué mejorar?" ───────────────
BLOQUES_MEJORAR: dict[str, list[str]] = {
    "Gestión y liderazgo": [
        "supervisor", "supervisores", "jefe", "jefes", "liderazgo",
        "coordinador", "encargado", "gestion", "administracion",
    ],
    "Comunicación interna": [
        "comunicacion", "informacion", "charlas", "aviso", "avisos",
        "dialogo", "escuchar", "escuchen",
    ],
    "Condiciones laborales": [
        "materiales", "uniforme", "uniformes", "equipo", "equipos",
        "herramientas", "implementos", "limpieza", "insumos",
        "horas", "horario", "horarios", "descanso",
    ],
    "Clima laboral": [
        "trato", "respeto", "ambiente", "laboral", "companerismo",
        "compañerismo", "apoyo", "reconocimiento", "valorar",
    ],
    "Capacitación y desarrollo": [
        "capacitacion", "capacitaciones", "capacitar", "aprendizaje",
        "crecimiento", "desarrollo", "oportunidad", "oportunidades",
        "linea de carrera",
    ],
    "Remuneración y beneficios": [
        "sueldo", "sueldos", "salario", "pago", "pagos", "aumento",
        "beneficios", "canasta", "canastas", "vacaciones", "navidad",
        "bonificacion", "bono", "incentivo", "incentivos",
    ],
}


def _strip_accents(text: str) -> str:
    """Quita tildes de un texto."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _bloques_generic(
    series: pd.Series, bloques_dict: dict[str, list[str]]
) -> pd.DataFrame:
    """
    Analiza bloques conceptuales genéricos sobre la serie de texto.
    Cada respuesta cuenta máximo 1 vez por bloque.
    """
    total_encuestados = len(series.dropna())
    counts = {bloque: 0 for bloque in bloques_dict}

    for text in series.dropna():
        normalized = _strip_accents(str(text).lower())
        for bloque, keywords in bloques_dict.items():
            if any(kw in normalized for kw in keywords):
                counts[bloque] += 1

    rows = [
        {
            "Bloque": bloque,
            "Menciones": count,
            "Porcentaje (%)": round((count / total_encuestados) * 100, 1) if total_encuestados > 0 else 0.0,
        }
        for bloque, count in counts.items()
    ]

    return pd.DataFrame(rows).sort_values("Menciones", ascending=False).reset_index(drop=True)


def _classify_generic(
    series: pd.Series, bloques_dict: dict[str, list[str]]
) -> dict[str, list[str]]:
    """Clasifica respuestas originales en bloques genéricos."""
    classified: dict[str, list[str]] = {bloque: [] for bloque in bloques_dict}

    for text in series.dropna():
        original = str(text).strip()
        if not original:
            continue
        normalized = _strip_accents(original.lower())
        for bloque, keywords in bloques_dict.items():
            if any(kw in normalized for kw in keywords):
                classified[bloque].append(original)

    return classified


# ── API pública (compatibilidad) ─────────────────────────────

def bloques_conceptuales(series: pd.Series) -> pd.DataFrame:
    """Bloques conceptuales para '¿Qué destacas?'"""
    return _bloques_generic(series, BLOQUES_DESTACAR)


def bloques_conceptuales_mejorar(series: pd.Series) -> pd.DataFrame:
    """Bloques conceptuales para '¿Qué mejorar?'"""
    return _bloques_generic(series, BLOQUES_MEJORAR)


def classify_responses_by_block(series: pd.Series) -> dict[str, list[str]]:
    """Clasifica respuestas de '¿Qué destacas?' por bloque."""
    return _classify_generic(series, BLOQUES_DESTACAR)


def classify_responses_mejorar(series: pd.Series) -> dict[str, list[str]]:
    """Clasifica respuestas de '¿Qué mejorar?' por bloque."""
    return _classify_generic(series, BLOQUES_MEJORAR)

    return classified


def get_text_summary(series: pd.Series) -> dict:
    """
    Resumen de texto abierto:
    - palabra_top: la más frecuente
    - top_10: DataFrame top 10
    - tabla_completa: DataFrame completo
    - total_menciones: total de palabras
    - total_respuestas: cantidad de respuestas no vacías
    """
    freq = word_frequency(series)
    total_menciones = int(freq["Frecuencia"].sum()) if not freq.empty else 0
    total_respuestas = int(series.dropna().shape[0])

    return {
        "palabra_top": freq.iloc[0]["Palabra"] if not freq.empty else "N/A",
        "top_10": freq.head(10),
        "tabla_completa": freq,
        "total_menciones": total_menciones,
        "total_respuestas": total_respuestas,
    }

"""
mappings.py - Mapeo de respuestas Likert texto → escala 1-5
Soporta escala de acuerdo y escala de frecuencia.
Incluye neutral (3) aunque no exista en datos actuales.
"""

# Escala de acuerdo (preguntas 1-5 y 7)
ACUERDO_MAP: dict[str, int] = {
    "Totalmente en desacuerdo": 1,
    "Parcialmente en desacuerdo": 2,
    "Ni de acuerdo ni en desacuerdo": 3,  # neutral — no presente aún
    "Parcialmente de acuerdo": 4,
    "Totalmente de acuerdo": 5,
}

# Escala de frecuencia (pregunta 6)
FRECUENCIA_MAP: dict[str, int] = {
    "Nunca": 1,
    "Casi nunca": 2,
    "A veces": 3,  # neutral — no presente aún
    "Casi siempre": 4,
    "Siempre": 5,
}

# Definición de cada pregunta Likert individual
# key = nombre corto para UI, col = columna exacta en Excel, scale = qué mapa usar
LIKERT_QUESTIONS: list[dict] = [
    {
        "key": "Ambiente de trabajo",
        "col": "Me siento a gusto con el ambiente de trabajo que se genera en mi equipo.",
        "scale": "acuerdo",
    },
    {
        "key": "Motivación",
        "col": "Me siento motivado a dar lo mejor de mí y hacer un buen trabajo",
        "scale": "acuerdo",
    },
    {
        "key": "Soporte del jefe",
        "col": "Mi supervisor o jefe directo me otorga el soporte que necesito para afrontar cualquier problema que afecte mi trabajo",
        "scale": "acuerdo",
    },
    {
        "key": "Trabajo en equipo",
        "col": "Mi supervisor o jefe directo fomenta que nos apoyemos entre todos en el equipo",
        "scale": "acuerdo",
    },
    {
        "key": "Reconocimiento",
        "col": "Siento que mi trabajo es reconocido por mi supervisor o jefe directo.",
        "scale": "acuerdo",
    },
    {
        "key": "Comunicación del jefe",
        "col": "Mi supervisor o jefe directo nos brinda charlas de 5 minutos y comunica las novedades relevantes a mi puesto de trabajo",
        "scale": "frecuencia",
    },
    {
        "key": "Limtek buen lugar",
        "col": "Considero a Limtek como un buen lugar para trabajar",
        "scale": "acuerdo",
    },
]

# Columnas de capacitación (selección múltiple: la celda tiene el nombre o es NaN)
CAPACITACION_COLS: list[str] = [
    "Seguridad y Salud en el Trabajo",
    "Uso de maquinarias y equipos",
    "Uso de insumos",
    "Atención al cliente",
    "Otro (especifique)",
]

# Columnas de preguntas abiertas
COL_DESTACAR = "¿Qué destacas de Limtek al considerarlo un buen lugar para trabajar?"
COL_MEJORAR = "¿Qué tendría que mejorar Limtek para que lo consideres un buen lugar para trabajar?"

# Columnas de filtro en la encuesta
COL_CLIENTE_ENC = "¿En qué cliente estás destacado?"
COL_UNIDAD_ENC = "¿En qué unidad estás destacado?"
COL_DEPTO_ENC = "¿En qué departamento trabajas?"

# Cargos válidos para participación en inventario
CARGOS_OPERARIOS: list[str] = [
    "OPERARIO",
    "OPERARIO POLIVALENTE",
    "OPERARIO PART TIME",
    "OPERARIO INTERMITENTE",
]


def get_scale_map(scale: str) -> dict[str, int]:
    """Retorna el mapa de escala correspondiente."""
    if scale == "acuerdo":
        return ACUERDO_MAP
    elif scale == "frecuencia":
        return FRECUENCIA_MAP
    else:
        raise ValueError(f"Escala desconocida: {scale}")

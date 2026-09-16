"""Plantillas de prompting parametrizables (few-shot y chain-of-thought).

Caso de uso: Asistente de atención al cliente PyME e-commerce Argentina.
Técnica justificada few-shot + instrucción de razonamiento
paso a paso ligera (CoT) + política de la tienda como contexto.
"""

SYSTEM_PROMPT = (
    "Sos el asistente virtual de la tienda online 'Tienda Ejemplo' (Argentina). "
    "Respondé en español rioplatense, trato amable y formal, máximo 120 palabras. "
    "Nunca inventes números de seguimiento, precios ni plazos: usá solo la política vigente. "
    "Si la consulta expresa enojo, es compleja o pide algo fuera de política, "
    "derivá a un agente humano y generá un resumen para el CRM."
)

POLITICA_TIENDA = (
    "Política vigente:\n"
    "- Envío estándar CABA/GBA 2-4 días $3.500, interior 3-7 días $4.500-$6.000. Gratis desde $30.000.\n"
    "- Envío expreso 1-2 días $7.200.\n"
    "- Devolución por falla dentro de 30 días con etiqueta gratuita, cambio o reembolso.\n"
    "- Garantía 12 meses por falla de fábrica.\n"
    "- Seguimiento con código RA + 9 dígitos + AR."
)

# Ejemplos de Few Shots
EJEMPLOS_FEW_SHOT = [
    {
        "consulta": "¿Dónde está mi pedido #3890? Hace 4 días que lo espero.",
        "respuesta": (
            "Su pedido #3890 fue despachado por Correo Argentino y figura en tránsito. "
            "El plazo para su zona es de 3-5 días hábiles, por lo que debería llegar entre hoy y mañana. "
            "Código de seguimiento RA987654321AR. Si en 48 hs no lo recibe, lo derivo con un agente para reclamo prioritario."
        ),
    },
    {
        "consulta": "¿Cuánto sale enviar a Rosario?",
        "respuesta": (
            "El envío estándar a Rosario cuesta $4.500 y tarda 3-5 días hábiles, con seguimiento incluido. "
            "Si su compra supera $30.000, el envío estándar es gratis. El expreso cuesta $7.200 y tarda 1-2 días."
        ),
    },
    {
        "consulta": "Se me rompió la licuadora a los 20 días, ¿qué hago?",
        "respuesta": (
            "Está cubierta por la garantía de 30 días por falla. Le enviamos la etiqueta de devolución gratuita "
            "y al recibirla le hacemos cambio inmediato o reembolso, como prefiera. ¿Desea que inicie la devolución?"
        ),
    },
    {
        "consulta": "SON UNOS ESTAFADORES, QUIERO HABLAR CON UN HUMANO YA",
        "respuesta": (
            "Lamento mucho la molestia. Derivo su caso de inmediato con un agente humano que lo contactará "
            "en menos de 2 horas. Resumen para CRM: cliente enojado, pide contacto humano urgente, prioridad alta."
        ),
    },
]

INSTRUCCION_CHAIN_OF_THOUGHT = (
    "Antes de responder, pensá paso a paso: 1) Clasificá la intención "
    "(pedido/envío/devolución/enojo/otro), 2) Verificá qué parte de la política aplica, "
    "3) Redactá la respuesta en <=120 palabras, 4) Decidí si derivar a humano (SÍ/NO). "
    "Mostrá solo la respuesta final al cliente (y si deriva, agregá 'Derivación: SÍ - resumen CRM')."
)


def construir_prompt_few_shot(
    consulta: str, ejemplos: list[dict] = EJEMPLOS_FEW_SHOT
) -> str:
    """Arma prompt few-shot + system + política + CoT ligero."""
    bloques_ejemplo = [
        f"Consulta: {ejemplo['consulta']}\nRespuesta: {ejemplo['respuesta']}"
        for ejemplo in ejemplos
    ]
    ejemplos_formateados = "\n\n".join(bloques_ejemplo)

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"{POLITICA_TIENDA}\n\n"
        f"{INSTRUCCION_CHAIN_OF_THOUGHT}\n\n"
        f"Ejemplos:\n{ejemplos_formateados}\n\n"
        f"Consulta: {consulta}\n"
        "Respuesta:"
    )


def construir_prompt_chain_of_thought(consulta: str) -> str:
    """Variante CoT pura"""
    return (
        f"{SYSTEM_PROMPT}\n\n{POLITICA_TIENDA}\n\n"
        f"{INSTRUCCION_CHAIN_OF_THOUGHT}\n\nConsulta: {consulta}\nRespuesta:"
    )

"""Proveedor demo offline (sin API key).

Permite verificar el flujo completo sin gastar cuota:
aplica la misma interfaz BaseProvider pero con respuestas determinísticas
basadas en reglas simples. No reemplaza la ejecución real con Groq/Gemini,
solo sirve para validar `python -m src.main` y el formato de evidencias.md.
"""

from src.providers.base_provider import BaseProvider


class DemoProvider(BaseProvider):
    """Respuestas simuladas para el caso PyME e-commerce."""

    def _ultima_consulta(self, prompt: str) -> str:
        # El prompt few-shot contiene varios "Consulta:", nos interesa solo la última.
        partes = prompt.rsplit("Consulta:", 1)
        ultima = partes[-1] if len(partes) > 1 else prompt
        return ultima.lower()

    def generate(self, prompt: str) -> str:
        consulta = self._ultima_consulta(prompt)
        # La última consulta real es la última línea "Consulta: ..."
        # Respondemos por intención simple para demo verificable.
        if "#4521" in consulta or "dónde está mi pedido #4521" in consulta:
            return (
                "Su pedido #4521 fue despachado hace 3 días por Correo Argentino y está "
                "en distribución en su ciudad. El plazo estimado es de 24-48 hs hábiles. "
                "Puede seguirlo con el código RA123456789AR. Si no llega en 48 hs, le derivamos "
                "con un agente humano para gestión prioritaria."
            )
        if "córdoba" in consulta or "cuánto cuesta el envío" in consulta:
            return (
                "El envío a Córdoba capital cuesta $4.500 y tarda 3-5 días hábiles por "
                "correo estándar, o $7.200 y tarda 1-2 días por expreso. Superando los $30.000 "
                "el envío estándar es gratis. Según política vigente, todos los envíos incluyen seguimiento."
            )
        if "cafetera" in consulta or "fallada" in consulta or "devolverla" in consulta:
            return (
                "Sí, puede devolver la cafetera. Está dentro de los 30 días de garantía por falla "
                "de fábrica según nuestra política de devolución. Le enviamos la etiqueta de devolución "
                "gratuita y al recibir el producto le hacemos reembolso o cambio inmediato. "
                "¿Prefiere cambio o reembolso?"
            )
        return (
            "Gracias por su consulta. Según nuestras políticas vigentes, un agente revisará "
            "su caso. Si es urgente o expresa enojo, derivamos a humano en menos de 2 horas. "
            "(Respuesta demo: configure GROQ_API_KEY para respuesta real del Foundation Model.)"
        )

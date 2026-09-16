"""Factory Method simple para instanciar el proveedor según MODEL_PROVIDER.

`main.py` llama a `get_provider()` una sola vez y no necesita saber nada más
sobre cómo se construye cada proveedor.
"""

from src.providers.base_provider import BaseProvider
from src.providers.demo_provider import DemoProvider
from src.providers.gemini_provider import GeminiProvider
from src.providers.groq_provider import GroqProvider

PROVIDER_GROQ = "groq"
PROVIDER_GEMINI = "gemini"
PROVIDER_DEMO = "demo"


def get_provider(name: str) -> BaseProvider:
    """Devuelve la instancia de proveedor correspondiente a `name`."""
    nombre_normalizado = name.strip().lower()

    if nombre_normalizado == PROVIDER_GROQ:
        return GroqProvider()

    if nombre_normalizado == PROVIDER_GEMINI:
        return GeminiProvider()

    if nombre_normalizado == PROVIDER_DEMO:
        return DemoProvider()

    raise ValueError(
        f"Proveedor '{name}' no soportado. Usá '{PROVIDER_GROQ}', '{PROVIDER_GEMINI}' "
        f"o '{PROVIDER_DEMO}' (demo offline) en la variable de entorno MODEL_PROVIDER."
    )

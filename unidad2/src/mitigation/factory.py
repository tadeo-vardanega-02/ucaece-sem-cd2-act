from sklearn.base import BaseEstimator

from src.config import MITIGATION_METHOD_AMBOS
from src.mitigation.base_mitigator import BaseMitigator
from src.mitigation.exponentiated_gradient import ExponentiatedGradientMitigator
from src.mitigation.threshold_optimizer import ThresholdOptimizerMitigator

# --- Nombres válidos de MITIGATION_METHOD (además de "ambos") ---
METODO_EXPONENTIATED_GRADIENT = "exponentiated_gradient"
METODO_THRESHOLD_OPTIMIZER = "threshold_optimizer"
METODOS_INDIVIDUALES = (METODO_EXPONENTIATED_GRADIENT, METODO_THRESHOLD_OPTIMIZER)


def get_mitigator(
    nombre: str, restriccion: str, estimador_base: BaseEstimator
) -> BaseMitigator:
    """Devuelve la instancia de mitigador correspondiente a `nombre`.

    `estimador_base` es el modelo ya entrenado en `model_training.py`: cada
    mitigador decide si lo reentrena (ExponentiatedGradient) o lo reutiliza
    tal cual (ThresholdOptimizer).
    """
    if nombre == METODO_EXPONENTIATED_GRADIENT:
        return ExponentiatedGradientMitigator(restriccion, estimador_base)
    if nombre == METODO_THRESHOLD_OPTIMIZER:
        return ThresholdOptimizerMitigator(restriccion, estimador_base)

    raise ValueError(
        f"Método de mitigación '{nombre}' no soportado. Usá uno de: "
        f"{', '.join(METODOS_INDIVIDUALES)}."
    )


def resolver_metodos(mitigation_method: str) -> tuple[str, ...]:
    """Expande MITIGATION_METHOD='ambos' a la lista de métodos a ejecutar."""
    if mitigation_method == MITIGATION_METHOD_AMBOS:
        return METODOS_INDIVIDUALES
    return (mitigation_method,)

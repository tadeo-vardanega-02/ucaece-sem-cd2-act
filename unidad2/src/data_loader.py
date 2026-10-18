import os

import pandas as pd

from src.config import Config

SEMILLA = 42
MAX_FILAS_MUESTRA = 10000


def _cargar_dataset_demo() -> pd.DataFrame:
    """Descarga el dataset público Adult Income (atributo sensible: sexo)."""
    from fairlearn.datasets import fetch_adult

    datos = fetch_adult(as_frame=True)
    dataframe = datos.data.copy()
    dataframe["class"] = datos.target.astype(str).str.strip()
    return dataframe


def _cargar_dataset_propio(ruta: str) -> pd.DataFrame:
    if not os.path.isfile(ruta):
        raise FileNotFoundError(
            f"No se encontró el archivo '{ruta}' (DATASET_PATH). "
            "Verificá la ruta o colocá tu CSV dentro de la carpeta data/."
        )
    return pd.read_csv(ruta)


def _validar_columnas(dataframe: pd.DataFrame, config: Config) -> None:
    columnas_faltantes = [
        columna
        for columna in (config.target_column, config.sensitive_attribute)
        if columna not in dataframe.columns
    ]
    if columnas_faltantes:
        columnas_disponibles = ", ".join(dataframe.columns)
        raise ValueError(
            f"No se encontraron en el dataset las columnas {columnas_faltantes}. "
            f"Columnas disponibles: {columnas_disponibles}. "
            "Revisá TARGET_COLUMN y SENSITIVE_ATTRIBUTE en tu .env."
        )


def _binarizar_target(dataframe: pd.DataFrame, config: Config) -> pd.DataFrame:
    valores_target = dataframe[config.target_column].astype(str).str.strip()
    if config.positive_label not in valores_target.unique():
        valores_disponibles = ", ".join(sorted(valores_target.unique()))
        raise ValueError(
            f"POSITIVE_LABEL='{config.positive_label}' no aparece en la columna "
            f"'{config.target_column}'. Valores disponibles: {valores_disponibles}."
        )
    dataframe = dataframe.copy()
    dataframe[config.target_column] = (valores_target == config.positive_label).astype(
        int
    )
    return dataframe


def _submuestrear(dataframe: pd.DataFrame) -> pd.DataFrame:
    if len(dataframe) <= MAX_FILAS_MUESTRA:
        return dataframe
    return dataframe.sample(n=MAX_FILAS_MUESTRA, random_state=SEMILLA).reset_index(
        drop=True
    )


def cargar_datos(config: Config) -> pd.DataFrame:
    """Devuelve el DataFrame listo para entrenar: columnas validadas y target binario."""
    dataframe = (
        _cargar_dataset_demo()
        if config.usa_dataset_demo
        else _cargar_dataset_propio(config.dataset_path)
    )
    _validar_columnas(dataframe, config)
    dataframe = _binarizar_target(dataframe, config)
    return _submuestrear(dataframe)

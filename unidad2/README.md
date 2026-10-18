# Unidad 2 — Entrega: Tadeo Vardanega

> Caso elegido: sistema de reclutamiento automatizado de Amazon (Dastin, 2018).
> Dataset: German Credit (Statlog, UCI, 1000 filas) — `data/german_credit.csv` (no se versiona por `.gitignore`; reproducir descargando de UCI y derivando `sex` desde `personal_status`).
> Atributo sensible: `sex` (female=310, male=690). Columna objetivo: `class` (clase positiva `good`).
> Configuración: `MITIGATION_METHOD=ambos`, `FAIRNESS_CONSTRAINT=demographic_parity`.

## Resultados principales

| Escenario | Exactitud | DPD | EOD |
|---|---|---|---|
| Modelo base | 0,740 | 0,102 | 0,089 |
| ExponentiatedGradient | 0,717 | 0,040 | 0,145 |
| ThresholdOptimizer | 0,750 | 0,026 | 0,085 |

Base por grupo: female acc 0,708 sel 0,677; male acc 0,755 sel 0,779. Métrica extra `equalized_odds_ratio=0,836`.
Ver detalle e interpretación en `evidencias.md` y gráficos en `outputs/`.

## Cómo ejecutar

```bash
cp .env.example .env
pip install -r requirements.txt
python -m src.main
```

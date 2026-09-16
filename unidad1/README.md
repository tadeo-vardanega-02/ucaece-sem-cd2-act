# Unidad 1 — Asistente PyME e-commerce con Foundation Model

## 1. Caso de uso
Asistente virtual de atención al cliente para PyME e-commerce Argentina.
Responde pedidos, envíos, devoluciones/garantía y deriva a humano si hay enojo o caso complejo.
Restricciones: presupuesto ~0 USD, privacidad media-baja (anonimizar pedidos), latencia <3s.

## 2. Modelo elegido
**Pesos abiertos vía Groq: LLaMA 3.1 8B (`MODEL_PROVIDER=groq`).**
Fallback: Gemini 1.5 Flash (`MODEL_PROVIDER=gemini`).
Justificación completa: costo cero, sin GPU propia, migración futura a self-hosted, latencia 0.5-1.5s en Groq.

Para entrega offline / verificación sin key: `MODEL_PROVIDER=demo` (respuestas simuladas, no requiere API).

## 3. Estrategia de adaptación
**Prompt engineering avanzado: few-shot + CoT ligero + política de tienda.**
Ver `src/prompt_templates.py`: `SYSTEM_PROMPT` + `POLITICA_TIENDA` + `EJEMPLOS_FEW_SHOT` + `INSTRUCCION_CHAIN_OF_THOUGHT`.
Full fine-tuning descartado. PEFT LoRA queda como evolución futura en `notebooks/notebook_peft.ipynb`.

## 4. Cómo ejecutar

### Opción A - Demo offline (sin key, para verificar flujo)
```bash
cp .env.example .env
pip install -r requirements.txt
python -m src.main
```

### Opción B - Real con Groq (rama elegida)
1. Key gratuita en https://console.groq.com/keys
2. En `.env`: `MODEL_PROVIDER=groq` + `GROQ_API_KEY=API_KEY`
3. `pip install -r requirements.txt`
4. `python -m src.main`
5. Si error 404 model_not_found: listar modelos vigentes y actualizar `GROQ_MODEL_NAME` en `src/providers/groq_provider.py`:
```bash
curl -s -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
```

### Opción C - Real con Gemini (fallback)
1. Key en https://aistudio.google.com/app/apikey
2. En `.env`: `MODEL_PROVIDER=gemini` + `GEMINI_API_KEY=API_KEY`
3. `python -m src.main`

## 5. Estructura
```
unidad1/
├── .env.example
├── requirements.txt
├── README.md
├── evidencias.md            # se genera al ejecutar (3 consultas)
├── src/
│   ├── main.py              # 3 CONSULTAS_DE_EJEMPLO del caso
│   ├── prompt_templates.py  # few-shot + CoT + política
│   └── providers/
│       ├── base_provider.py
│       ├── factory.py       # groq / gemini / demo
│       ├── groq_provider.py
│       ├── gemini_provider.py
│       └── demo_provider.py
└── notebooks/               # reservado rama PEFT (no aplica, prompt engineering)
```

## 6. Evidencias
- `evidencias.md` generado con prompt + respuesta de las 3 consultas.
- Captura terminal ejecución exitosa: agregar al Word/PDF junto al link del repo forkeado.

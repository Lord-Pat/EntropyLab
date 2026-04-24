# EntropyLab

**Generador de claves criptográficas mediante entropía física real**

EntropyLab captura el movimiento caótico de lámparas de lava a través de una cámara, extrae la diferencia entre frames consecutivos y la convierte en claves criptográficas de alta entropía. Sin semillas artificiales, sin generadores pseudoaleatorios: entropía física pura.

Los resultados son validados con los tests estadísticos **NIST SP800-22**, **entropía de Shannon**, **autocorrelación serial** y **Maurer's Universal Test**, y están disponibles públicamente. Todo el código es open source y auditable.

---

## Índice

- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Algoritmos](#algoritmos)
- [API REST](#api-rest)
- [Análisis estadístico](#análisis-estadístico)
- [Resultados](#resultados)
- [Autores](#autores)

---

## Arquitectura

```
EntropyLab/
└── backend/
    ├── config.py                        ← configuración global
    ├── main.py                          ← punto de entrada
    ├── domain/
    │   ├── entropy_frame.py             ← frame capturado por la cámara
    │   ├── key.py                       ← clave criptográfica generada
    │   ├── nist_result.py               ← resultado análisis NIST
    │   ├── shannon_result.py            ← resultado análisis Shannon
    │   ├── autocorrelation_result.py    ← resultado autocorrelación serial
    │   └── maurer_result.py             ← resultado Maurer's Universal Test
    ├── infrastructure/
    │   ├── camera_reader.py             ← captura frames via OpenCV
    │   ├── sqlite_repository.py         ← persistencia en SQLite
    │   └── csv_exporter.py             ← exportación a CSV
    ├── services/
    │   ├── entropy_service.py           ← extrae entropía de los frames
    │   ├── key_generator_service.py     ← genera GUIDs desde entropía
    │   ├── analysis_service.py          ← gestor de análisis estadístico
    │   ├── algorithms/
    │   │   ├── algorithms.json          ← especificaciones de cada algoritmo
    │   │   ├── v0_1_0.py               ← SHA-256 de diff entre 2 frames
    │   │   ├── v0_2_0.py               ← igual que v0.1.0 (lámpara nueva)
    │   │   ├── v0_3_0.py               ← selección zonas activas (percentil 75)
    │   │   └── v0_4_0.py               ← XOR de diffs entre 3 frames
    │   └── analyzers/
    │       ├── nist_analyzer.py         ← tests NIST SP800-22
    │       ├── shannon_analyzer.py      ← entropía de Shannon
    │       ├── autocorrelation_analyzer.py ← autocorrelación serial
    │       └── maurer_analyzer.py       ← Maurer's Universal Test
    └── interfaces/
        ├── cli.py                       ← menú de control por consola
        └── api.py                       ← API REST con FastAPI
```

**Stack:** Python · OpenCV · FastAPI · SQLite · MicroPython (ESP32)

**Hardware:** Freenove ESP32-WROVER-CAM con sensor OV2640. Stream MJPEG en `http://[IP]/video`.

---

## Requisitos

### Software
- Python 3.8 o superior
- pip

### Hardware
- Freenove ESP32-WROVER-CAM (o compatible con stream MJPEG)
- Lámpara de lava — cualquier tamaño, cuanta más superficie en movimiento visible por la cámara, mejor calidad de entropía

### Dependencias Python

```
fastapi
uvicorn
opencv-python
numpy
scipy
python-dotenv
mailjet-rest
slowapi
```

---

## Instalación

**1. Clona el repositorio:**

```bash
git clone https://github.com/Lord-Pat/EntropyLab.git
cd EntropyLab/backend
```

**2. Crea y activa el entorno virtual:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

**3. Instala las dependencias:**

```bash
pip install fastapi uvicorn opencv-python numpy scipy python-dotenv mailjet-rest slowapi
```

**4. Configura las variables de entorno:**

Crea un fichero `.env` en `backend/` con el siguiente contenido:

```
MAILJET_API_KEY=tu_api_key
MAILJET_SECRET_KEY=tu_secret_key
```

> El `.env` está en `.gitignore` y nunca se sube al repositorio.

---

## Configuración

Edita `backend/config.py` para ajustar los parámetros principales:

```python
STREAM_URL = "http://192.168.X.X/video"   # IP de la ESP32 en tu red
DB_PATH = "entropylab.db"                  # ruta de la base de datos
CSV_EXPORT_PATH = "exports/"               # carpeta de exportación
ALGORITHM_VERSION = "0.2.0"               # versión del algoritmo activo
GENERATION_LIMIT = 100000                  # límite de claves por ciclo
```

> La IP de la ESP32 cambia según la red. Consulta la IP asignada en el router o en el monitor serie de Thonny.

---

## Uso

Arranca el sistema desde `backend/`:

```bash
python main.py
```

El menú de control aparece en la consola:

```
╔══════════════════════════════════╗
║      EntropyLab v0.1             ║
╠══════════════════════════════════╣
║  1. Iniciar generación masiva    ║
║  2. Parar generación             ║
║  3. Exportar a CSV               ║
║  4. Registrar análisis           ║
║  5. Arrancar servidor API        ║
║  6. Estado del sistema           ║
║  0. Salir                        ║
╚══════════════════════════════════╝
```

### Flujo de trabajo típico

1. **Opción 1** — inicia la generación masiva. El sistema genera claves en un hilo separado hasta alcanzar el límite configurado (por defecto 100.000) o hasta que lo pares manualmente.
2. **Opción 2** — para la generación en cualquier momento.
3. **Opción 4** — ejecuta el análisis estadístico completo (NIST + Shannon) sobre las claves acumuladas y guarda los resultados en la base de datos.
4. **Opción 3** — exporta las claves a CSV. Al exportar pregunta si deseas borrarlas de la BD para liberar espacio antes del siguiente ciclo.
5. **Opción 5** — arranca el servidor API REST en `http://localhost:8000`.

### Exponer la API públicamente con ngrok

```bash
ngrok http 8000
```

Copia la URL generada (`https://xxxx.ngrok-free.app`) y úsala como base URL en el frontend.

---

## Algoritmos

Cada algoritmo vive en `services/algorithms/` y expone una función `extraer_entropia(frame1, frame2)` o `extraer_entropia(frame1, frame2, frame3)`. El número de frames que necesita cada algoritmo está definido en `algorithms.json`:

```json
{
    "0_1_0": {"frames": 2},
    "0_2_0": {"frames": 2},
    "0_3_0": {"frames": 2},
    "0_4_0": {"frames": 3}
}
```

Para cambiar de algoritmo basta con actualizar `ALGORITHM_VERSION` en `config.py`. Para añadir un nuevo algoritmo:

1. Crea `services/algorithms/v0_X_X.py` con la función `extraer_entropia`
2. Añade la entrada correspondiente en `algorithms.json`
3. Actualiza `ALGORITHM_VERSION` en `config.py`

### Versiones implementadas

| Versión | Descripción | Frames |
|---------|-------------|--------|
| v0.1.0 | SHA-256 de la diferencia absoluta entre 2 frames | 2 |
| v0.2.0 | Igual que v0.1.0 — control con lámpara nueva | 2 |
| v0.3.0 | SHA-256 sobre píxeles con mayor movimiento (percentil 75) | 2 |
| v0.4.0 | XOR de diferencias entre 3 frames consecutivos + SHA-256 | 3 |

---

## API REST

El servidor expone dos endpoints en `http://localhost:8000`:

### `POST /keys/generate`

Genera claves criptográficas y las devuelve en el formato solicitado.

| Parámetro | Valores | Por defecto |
|-----------|---------|-------------|
| `cantidad` | 1, 5, 10, 15, 20 | 1 |
| `formato` | json, csv, txt | json |

**Ejemplo:**
```
POST /keys/generate?cantidad=5&formato=json
```

**Límite:** 10 peticiones por minuto por IP.

### `POST /keys/send-email`

Genera claves y las envía como adjunto al email indicado.

| Parámetro | Valores | Por defecto |
|-----------|---------|-------------|
| `cantidad` | 1, 5, 10, 15, 20 | 1 |
| `formato` | json, csv, txt | json |
| `email` | dirección válida | — |

**Límite:** 5 peticiones por minuto por IP.

### `GET /keys/count`

Devuelve el total de claves generadas acumuladas en la base de datos.

**Ejemplo:**
```
GET /keys/count
```

**Respuesta:**
```json
{ "total": 391610 }
```

Sin límite de peticiones.

> Documentación interactiva disponible en `http://localhost:8000/docs`.

---

## Análisis estadístico

El sistema ejecuta cuatro tipos de análisis sobre las claves generadas, todos accesibles desde la opción 4 del menú:

### NIST SP800-22

Batería de 4 tests estadísticos. El umbral de aceptación es p ≥ 0.01 en todos los tests.

| Test | Qué detecta |
|------|-------------|
| Monobit | Desequilibrio global entre 0s y 1s |
| Frecuencia por bloques | Desequilibrio local en bloques de 128 bits |
| Rachas | Patrones de repetición entre bits consecutivos |
| Entropía aproximada | Patrones repetidos en secuencias de 10 bits |

### Entropía de Shannon

Mide la distribución global de bytes en una escala de 0 a 8 bits. Una secuencia perfectamente aleatoria da 8.0. Se reporta también la eficiencia como porcentaje.

### Autocorrelación serial

Detecta dependencia entre bits separados por una distancia fija. Se ejecuta con lag=1 (bits consecutivos) y lag=8 (cada byte). Una secuencia aleatoria no debería mostrar correlación significativa entre posiciones.

### Maurer's Universal Statistical Test

Mide cuánto se puede comprimir la secuencia. Una secuencia verdaderamente aleatoria es incompresible — valores de fn cercanos a 6.196 con p ≥ 0.01 indican buena aleatoriedad. Es el test más sensible a estructuras ocultas en la secuencia.

Los resultados de los cuatro análisis se guardan en tablas separadas de la base de datos para comparativa entre versiones.

---

## Resultados

Los resultados completos del análisis estadístico por versión de algoritmo están documentados en la memoria del proyecto.

En resumen, todos los algoritmos superan los tests NIST SP800-22 con muestras de 100.000+ claves. v0.4.0 falla el test de Maurer's Universal, lo que indica que el XOR de tres frames introduce estructura compresible en la secuencia. v0.2.0 ofrece los mejores resultados globales.

---

## Frontend

La interfaz web está construida en Next.js con React y TypeScript, desplegada en Vercel.

### Stack

| Tecnología | Uso |
|------------|-----|
| Next.js / React | Framework principal de la aplicación web |
| TypeScript | Tipado estático del código frontend |
| Tailwind CSS | Estilos y diseño visual |

### Variables de entorno

Crea un fichero `.env.local` en la raíz del frontend:

```
NEXT_PUBLIC_API_URL=https://xxxx.ngrok-free.app
```

### Funcionalidades

- Landing page con vídeo de fondo y animación de entrada
- Contador de claves generadas en tiempo real desde la API
- Onboarding de 4 pasos para solicitar claves (cantidad, formato, método de entrega)
- Descarga directa en JSON, CSV o TXT
- Envío por email con adjunto
- Sección "Sobre nosotros" con perfiles del equipo

---

## Autores

**Aarón Martínez Nieto** — Backend Python, firmware ESP32, análisis estadístico

**Patrick Carbajal Malato** — Frontend React/Next.js, diseño e integración API

CFGS Desarrollo de Aplicaciones Multiplataforma · 2024-2026
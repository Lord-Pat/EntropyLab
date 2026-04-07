import os
from dotenv import load_dotenv


load_dotenv()


# ── Cámara ────────────────────────────────────────────
STREAM_URL = "http://192.168.32.175/video"

# ── Base de datos ─────────────────────────────────────
DB_PATH = "entropylab.db"

# ── Exportación ───────────────────────────────────────
CSV_EXPORT_PATH = "exports/"

# ── Algoritmo ─────────────────────────────────────────
ALGORITHM_VERSION = "0.1.0"

# ── Email Ngrok ───────────────────────────────────────
EMAIL_SENDER = os.getenv("ENTROPYLAB_EMAIL")

# ── Password Ngrok ────────────────────────────────────
EMAIL_PASSWORD = os.getenv("ENTROPYLAB_PASSWORD")
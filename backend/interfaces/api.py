from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import io
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

key_svc = None

def init(k):
    global key_svc
    key_svc = k

def _generar_claves(cantidad, formato):
    """Genera las claves y devuelve el contenido en el formato pedido."""
    claves = [key_svc.generate() for _ in range(cantidad)]

    if formato == "json":
        return "json", [{"value": k.value} for k in claves]

    if formato == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["value"])
        for k in claves:
            writer.writerow([k.value])
        return "csv", output.getvalue()

    if formato == "txt":
        return "txt", "\n".join([k.value for k in claves])

@app.post("/keys/generate")
def generate_keys(cantidad: int = 1, formato: str = "json"):
    if cantidad not in [1, 5, 10, 15, 20]:
        return JSONResponse(status_code=400, content={"error": "Cantidad no válida."})
    if formato not in ["json", "csv", "txt"]:
        return JSONResponse(status_code=400, content={"error": "Formato no válido."})

    fmt, contenido = _generar_claves(cantidad, formato)

    if fmt == "json":
        return contenido

    media = "text/csv" if fmt == "csv" else "text/plain"
    filename = f"claves.{fmt}"
    return StreamingResponse(
        iter([contenido]),
        media_type=media,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/keys/send-email")
def send_email(cantidad: int = 1, formato: str = "json", email: str = ""):
    if cantidad not in [1, 5, 10, 15, 20]:
        return JSONResponse(status_code=400, content={"error": "Cantidad no válida."})
    if formato not in ["json", "csv", "txt"]:
        return JSONResponse(status_code=400, content={"error": "Formato no válido."})
    if not email or "@" not in email:
        return JSONResponse(status_code=400, content={"error": "Email no válido."})

    from config import EMAIL_SENDER, EMAIL_PASSWORD

    fmt, contenido = _generar_claves(cantidad, formato)

    if fmt == "json":
        import json
        contenido_str = json.dumps(contenido, indent=2)
    else:
        contenido_str = contenido

    # Construir el email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = email
    msg["Subject"] = f"EntropyLab — tus {cantidad} claves"

    msg.attach(MIMEText(f"Adjunto encontrarás {cantidad} claves en formato {fmt.upper()}.", "plain"))

    adjunto = MIMEBase("application", "octet-stream")
    adjunto.set_payload(contenido_str.encode("utf-8"))
    encoders.encode_base64(adjunto)
    adjunto.add_header("Content-Disposition", f"attachment; filename=claves.{fmt}")
    msg.attach(adjunto)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_SENDER, email, msg.as_string())
        return {"ok": True, "mensaje": f"Claves enviadas a {email}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error enviando email: {str(e)}"})
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import io
import csv
import json
import os
import resend

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

def _generar_contenido(cantidad, formato):
    claves = [key_svc.generate() for _ in range(cantidad)]

    if formato == "json":
        return "json", json.dumps([{"value": k.value} for k in claves], indent=2)

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

    fmt, contenido = _generar_contenido(cantidad, formato)

    if fmt == "json":
        return json.loads(contenido)

    media = "text/csv" if fmt == "csv" else "text/plain"
    return StreamingResponse(
        iter([contenido]),
        media_type=media,
        headers={"Content-Disposition": f"attachment; filename=claves.{fmt}"}
    )

@app.post("/keys/send-email")
def send_email(cantidad: int = 1, formato: str = "json", email: str = ""):
    if cantidad not in [1, 5, 10, 15, 20]:
        return JSONResponse(status_code=400, content={"error": "Cantidad no válida."})
    if formato not in ["json", "csv", "txt"]:
        return JSONResponse(status_code=400, content={"error": "Formato no válido."})
    if not email or "@" not in email:
        return JSONResponse(status_code=400, content={"error": "Email no válido."})

    resend.api_key = os.getenv("RESEND_API_KEY")
    fmt, contenido = _generar_contenido(cantidad, formato)

    try:
        resend.Emails.send({
            "from": "EntropyLab <onboarding@resend.dev>",
            "to": [email],
            "subject": f"EntropyLab — tus {cantidad} claves",
            "text": f"Adjunto encontrarás {cantidad} claves en formato {fmt.upper()}.",
            "attachments": [{
                "filename": f"claves.{fmt}",
                "content": list(contenido.encode("utf-8"))
            }]
        })
        return {"ok": True, "mensaje": f"Claves enviadas a {email}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
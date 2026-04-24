from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
import io
import csv
import json
import os
import resend

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
key_svc = None
_sse_clients: set[asyncio.Queue] = set()

def init(k):
    global key_svc
    key_svc = k

def _get_total_sync() -> int:
    import sqlite3
    from config import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM keys")
    total = cursor.fetchone()[0]
    conn.close()
    return total

async def _broadcast(total: int):
    for q in list(_sse_clients):
        await q.put(total)

async def _stream_count():
    q: asyncio.Queue = asyncio.Queue()
    _sse_clients.add(q)
    try:
        total = await asyncio.to_thread(_get_total_sync)
        yield f"data: {total}\n\n"
        while True:
            try:
                total = await asyncio.wait_for(q.get(), timeout=25)
                yield f"data: {total}\n\n"
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        _sse_clients.discard(q)

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

@app.get("/keys/count/stream")
async def get_count_stream():
    return StreamingResponse(
        _stream_count(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

@app.post("/keys/generate")
@limiter.limit("10/minute")
async def generate_keys(request: Request, cantidad: int = 1, formato: str = "json"):
    if cantidad not in [1, 5, 10, 15, 20]:
        return JSONResponse(status_code=400, content={"error": "Cantidad no válida."})
    if formato not in ["json", "csv", "txt"]:
        return JSONResponse(status_code=400, content={"error": "Formato no válido."})

    fmt, contenido = _generar_contenido(cantidad, formato)

    total = await asyncio.to_thread(_get_total_sync)
    await _broadcast(total)

    if fmt == "json":
        return json.loads(contenido)

    media = "text/csv" if fmt == "csv" else "text/plain"
    return StreamingResponse(
        iter([contenido]),
        media_type=media,
        headers={"Content-Disposition": f"attachment; filename=claves.{fmt}"}
    )

@app.post("/keys/send-email")
@limiter.limit("5/minute")
async def send_email(request: Request, cantidad: int = 1, formato: str = "json", email: str = ""):
    if cantidad not in [1, 5, 10, 15, 20]:
        return JSONResponse(status_code=400, content={"error": "Cantidad no válida."})
    if formato not in ["json", "csv", "txt"]:
        return JSONResponse(status_code=400, content={"error": "Formato no válido."})
    if not email or "@" not in email:
        return JSONResponse(status_code=400, content={"error": "Email no válido."})

    from mailjet_rest import Client
    import base64

    api_key = os.getenv("MAILJET_API_KEY")
    secret_key = os.getenv("MAILJET_SECRET_KEY")
    mailjet = Client(auth=(api_key, secret_key), version="v3.1")

    fmt, contenido = _generar_contenido(cantidad, formato)
    contenido_bytes = contenido.encode("utf-8")
    contenido_b64 = base64.b64encode(contenido_bytes).decode("utf-8")

    data = {
        "Messages": [{
            "From": {
                "Email": "entropylabofficial@gmail.com",
                "Name": "EntropyLab"
            },
            "To": [{"Email": email}],
            "Subject": f"EntropyLab — tus {cantidad} claves",
            "TextPart": f"Adjunto encontrarás {cantidad} claves en formato {fmt.upper()}.",
            "Attachments": [{
                "ContentType": "text/plain",
                "Filename": f"claves.{fmt}",
                "Base64Content": contenido_b64
            }]
        }]
    }

    try:
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            total = await asyncio.to_thread(_get_total_sync)
            await _broadcast(total)
            return {"ok": True, "mensaje": f"Claves enviadas a {email}"}
        else:
            return JSONResponse(status_code=500, content={"error": result.json()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/keys/count")
def get_keys_count():
    import sqlite3
    from config import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM keys")
    total = cursor.fetchone()[0]
    conn.close()
    return {"total": total}
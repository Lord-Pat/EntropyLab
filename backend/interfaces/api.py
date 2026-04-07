from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import io
import csv

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

@app.post("/keys/generate")
def generate_keys(cantidad: int = 1, formato: str = "json"):
    if cantidad not in [1, 5, 10, 15, 20]:
        return JSONResponse(status_code=400, content={"error": "Cantidad no válida."})
    if formato not in ["json", "csv", "txt"]:
        return JSONResponse(status_code=400, content={"error": "Formato no válido."})

    claves = [key_svc.generate() for _ in range(cantidad)]

    if formato == "json":
        return [{"value": k.value} for k in claves]

    if formato == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["value"])
        for k in claves:
            writer.writerow([k.value])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=claves.csv"}
        )

    if formato == "txt":
        contenido = "\n".join([k.value for k in claves])
        return StreamingResponse(
            iter([contenido]),
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=claves.txt"}
        )
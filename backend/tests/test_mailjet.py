import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Prueba de envío de email via Mailjet.
# Envía un email de prueba a la dirección indicada.
# Uso: verificar que las credenciales de Mailjet funcionan y el email llega correctamente.

from dotenv import load_dotenv
load_dotenv()

from mailjet_rest import Client
import base64

api_key = os.getenv("MAILJET_API_KEY")
secret_key = os.getenv("MAILJET_SECRET_KEY")

if not api_key or not secret_key:
    print("✗ Credenciales Mailjet no encontradas en .env")
    exit(1)

mailjet = Client(auth=(api_key, secret_key), version="v3.1")

contenido = "Clave de prueba: test-entropylab-123"
contenido_b64 = base64.b64encode(contenido.encode("utf-8")).decode("utf-8")

data = {
    "Messages": [{
        "From": {
            "Email": "entropylabofficial@gmail.com",
            "Name": "EntropyLab"
        },
        "To": [{"Email": "entropylabofficial@gmail.com"}],
        "Subject": "EntropyLab — test de envío",
        "TextPart": "Email de prueba generado por test_smtp.py",
        "Attachments": [{
            "ContentType": "text/plain",
            "Filename": "test.txt",
            "Base64Content": contenido_b64
        }]
    }]
}

result = mailjet.send.create(data=data)
if result.status_code == 200:
    print("✓ Email enviado correctamente")
else:
    print(f"✗ Error: {result.json()}")
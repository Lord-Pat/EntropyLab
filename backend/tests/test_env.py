import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Verifica que las variables de entorno de Mailjet se cargan correctamente desde .env
# Uso: comprobar que el fichero .env existe y tiene las claves configuradas.

from dotenv import load_dotenv
load_dotenv()

mailjet_key = os.getenv("MAILJET_API_KEY")
mailjet_secret = os.getenv("MAILJET_SECRET_KEY")

print(f"MAILJET_API_KEY:    {'✓ cargada' if mailjet_key else '✗ no encontrada'}")
print(f"MAILJET_SECRET_KEY: {'✓ cargada' if mailjet_secret else '✗ no encontrada'}")
# test para comprobar si realmente lee las variables de entorno como toca

import os
from dotenv import load_dotenv

load_dotenv()

print("EMAIL =", repr(os.getenv("ENTROPYLAB_EMAIL")))
print("PASSWORD =", repr(os.getenv("ENTROPYLAB_PASSWORD")))
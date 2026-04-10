import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("Entropylab_Email", "").strip()
password = os.getenv("Entropylab_Password", "").strip()

print("USER:", repr(user))
print("PASS LEN:", len(password))
print("PASS PREVIEW:", repr(password[:4] + "..."))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
    servidor.login(user, password)
    print("LOGIN OK")
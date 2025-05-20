import os
import fdb
from dotenv import load_dotenv

load_dotenv()

def conectar():
    dsn = os.getenv("FIREBIRD_DSN")
    user = os.getenv("FIREBIRD_USER")
    password = os.getenv("FIREBIRD_PASSWORD")

    return fdb.connect(dsn=dsn, user=user, password=password)

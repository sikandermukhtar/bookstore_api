from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()

mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME") or "",
    MAIL_PASSWORD=SecretStr(os.getenv("MAIL_PASSWORD") or ""),
    MAIL_FROM=os.getenv("MAIL_FROM") or "",
    MAIL_PORT=int(os.getenv("MAIL_PORT") or 587),
    MAIL_SERVER=os.getenv("MAIL_SERVER") or "smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

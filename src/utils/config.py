from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)
print(f"✅ .env loaded from: {env_path}")

# === Yardımcı: Dinamik tarih hesaplama fonksiyonu ===
def generate_query_key():
    today = datetime.now()
    # Bugünün tarihi
    end_date = today.strftime("%d.%m.%Y")
    # Eğer yıl 2025 ise başlangıç 02.01.2025, değilse yılın ilk günü
    if today.year == 2025:
        start_date = "02.01.2025"
    else:
        start_date = f"02.01.{today.year}"
    tarih_araligi = f"{start_date} ile {end_date}"

    query_dict = {
        "items": [
            "Dönen_Varlıklar",
            "Kısa_Vadeli_Borçlar",
            "Net_Dönem_Karı",
            "Net_Satışlar",
            "Ortalama_Ticari_Alacaklar",
            "Toplam_Borçlar",
            "Toplam_Varlıklar",
            "Stok"
        ],
        "Tarih": tarih_araligi
    }
    return query_dict

#Settings(BaseSettings) sayesinde her değişken .env’den çekilip settings nesnesine aktarılıyor.
class Settings(BaseSettings):
    # API
    API_BASE_URL: str
    API_LOGIN_PATH: str = "/auth/login"
    API_QUERY_PATH: str = "/query/v2/run-basic"
    API_USERNAME: str
    API_PASSWORD: str
    API_TOKEN: Optional[str] = None

    # Query
    QUERY_KEY: dict = Field(default_factory=generate_query_key)

    # LLM / Groq
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str
    GROQ_MODEL: str = "mixtral-8x7b"
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"

    # Mail
    SMTP_SERVER: Optional[str] = "smtp.office365.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASS: str
    MAIL_FROM: str
    MAIL_TO: str
    MAIL_SUBJECT: str = "Chef Seasons Otomatik Rapor"

    # Logging
    LOG_LEVEL: str = "INFO"
    
    #.env’deki her satır otomatik olarak Settings sınıfına aktarılıyor.
    class Config:
        env_file = ".env"
        case_sensitive = False

    def recipients(self) -> List[str]:
        """Split comma-separated recipients"""
        if not self.MAIL_TO:
            return []
        return [r.strip() for r in self.MAIL_TO.split(",") if r.strip()]

settings = Settings()
print("🔹 Dinamik QUERY_KEY oluşturuldu:", settings.QUERY_KEY)
# Agentic Report Automation

## 📋 Genel Bakış

**Agentic Report Automation**, Chef Seasons için geliştirilmiş bir **tam otomatik aylık raporlama sistemidir.**  
Her ay sonunda sistem otomatik olarak:

- QueryRunner API üzerinden veriyi çeker
- Groq LLM (ör. _mixtral-8x7b_ veya _llama-3.1-8b-instant_) ile analiz eder
- Dinamik finansal özet raporu üretir
- E-posta yoluyla ilgili kişilere gönderir

Bu süreç tamamen **Docker container** içinde çalışır ve bir **ay sonu zamanlayıcı (scheduler)** tarafından tetiklenir.

---

## ⚙️ Özellikler

🔄 **Tam otomatik pipeline:**  
Veri → Analiz → Rapor → E-posta gönderimi

🤖 **LLM tabanlı analiz:**  
Groq API ile OpenAI uyumlu büyük dil modeli entegrasyonu

📧 **E-posta gönderimi:**  
Gmail App Password ile güvenli SMTP

🕒 **Planlı çalıştırma:**  
Docker + cron veya Task Scheduler ile ay sonu otomasyonu

🧩 **Ortam değişkenleri (.env):**  
Tüm konfigürasyon Pydantic `Settings` sınıfı üzerinden yönetilir

🧱 **Platform bağımsız:**  
Windows, Linux, veya Cloud Container ortamlarında çalışabilir

---

## 📁 Proje Yapısı

📦 Agentic-Report-Automation/
├─ src/
│ ├─ agents/
│ │ ├─ orchestrator.py # Ana pipeline akışı
│ │ ├─ data_agent.py # API'den veri çekme
│ │ ├─ analysis_agent.py # LLM çağrısı (Groq)
│ │ └─ mail_agent.py # SMTP ile e-posta gönderimi
│ ├─ utils/
│ │ ├─ config.py # Pydantic Settings (.env'den okur)
│ │ └─ logger.py # Log yapılandırması (Loguru)
│ └─ main.py # Giriş noktası
├─ prompts/
│ └─ report_prompt.txt # LLM analiz prompt şablonu
├─ .env # Ortam değişkenleri
├─ Dockerfile # Docker build tanımı
├─ docker-compose.yml # Container yönetimi
├─ requirements.txt # Python bağımlılıkları
└─ README.md # Proje dökümantasyonu

## 🔧 Kurulum

## 1️⃣ Ortam Hazırlığı

- Python 3.11+
- Docker ve Docker Compose (son sürüm)
- Gmail hesabında App Password oluşturulmuş olmalı

## 2️⃣ .env Dosyasını Oluştur

Kök dizine .env adında bir dosya ekle ve aşağıdaki örneği düzenle:

# QueryRunner API

API_BASE_URL=http://78.189.179.50:17487
API_LOGIN_PATH=/auth/login
API_QUERY_PATH=/query/v2/run-basic
API_USERNAME=testnilay
API_PASSWORD=123456

# LLM / Groq

LLM_PROVIDER=groq
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GROQ_MODEL=llama-3.1-8b-instant
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions

# Gmail SMTP

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seningmailadresin@gmail.com
SMTP_PASS=gmail_app_password
MAIL_FROM=seningmailadresin@gmail.com
MAIL_TO=nilay@chefseasons.com
MAIL_SUBJECT=Chef Seasons Otomatik Rapor

# Logging

LOG_LEVEL=INFO

## 3️⃣ Docker Image Oluştur

docker compose build
veya tek satırda çalıştırmak için:
docker compose up --build

🕒 Ay Sonu Otomatik Çalıştırma
🔹 Windows

1. Task Scheduler aç

2.“New Task” oluştur

3. Action:

docker compose up --build --abort-on-container-exit

4. Trigger:
   “Monthly” → Her ayın 30 veya 31’i → Saat 23:59
   🔹 Linux

crontab -e dosyasına şunu ekle:

59 23 28-31 \* \* cd /path/to/Agentic-Report-Automation && docker compose up --build --abort-on-container-exit

## 📊 Loglar

Tüm loglar konsola ve logs/ dizinine kaydedilir.

Örnek log satırları:
2025-10-31 23:59:01 | INFO | src.agents.orchestrator:run_pipeline - === Agentic pipeline started ===
2025-10-31 23:59:08 | INFO | src.agents.analysis_agent:generate_report - Report successfully generated.
2025-10-31 23:59:15 | INFO | src.agents.mail_agent:send_report - ✅ Email sent successfully.

🧠 Geliştirici Notları

.env dosyasındaki veriler pydantic_settings.BaseSettings ile otomatik okunur.

QUERY_KEY alanı çalışma tarihine göre dinamik olarak oluşturulur:

"Tarih": "02.01.2025 ile 31.10.2025"

LLM prompt metni src/prompts/report_prompt.txt içinden yüklenir.

Gmail SMTP TLS (port 587) üzerinden bağlanır.

🧩 Faydalı Komutlar
| Komut | Açıklama |
| ---------------------- | ------------------------------- |
| `docker compose up` | Container’ı başlatır |
| `docker compose down` | Container’ı durdurur |
| `docker compose logs` | Çalışma loglarını gösterir |
| `docker compose build` | Yeni imaj oluşturur |
| `python -m src.main` | Local ortamda test çalıştırması |

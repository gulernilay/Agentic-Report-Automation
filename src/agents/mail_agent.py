import smtplib
from email.mime.text import MIMEText
from ..utils.config import settings
from ..utils.logger import logger

def send_report(report_text: str):
    """Send the generated report via email using SMTP.

    Args:
        report_text (str): The content of the report to be sent in the email body.

    The function uses the following settings from the config:
        - MAIL_SUBJECT: Subject line of the email
        - MAIL_FROM: Sender's email address
        - SMTP_SERVER: SMTP server hostname
        - SMTP_PORT: SMTP server port
        - SMTP_USER: SMTP authentication username
        - SMTP_PASS: SMTP authentication password
        - recipients(): List of recipient email addresses

    Raises:
        smtplib.SMTPException: If there's an error in sending the email
    """
    msg = MIMEText(report_text, "plain", "utf-8")
    msg["Subject"] = settings.MAIL_SUBJECT
    msg["From"] = settings.MAIL_FROM
    msg["To"] = ", ".join(settings.recipients())

    logger.info(f"Sending email to: {msg['To']}")
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
        smtp.send_message(msg)
    logger.info("Email sent successfully.")

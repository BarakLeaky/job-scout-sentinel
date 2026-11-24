import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = "leakeybarak23@gmail.com"


def _send_message(msg):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        raise RuntimeError(
            "Email credentials are missing. Check GitHub repository secrets "
            "EMAIL_ADDRESS and EMAIL_PASSWORD."
        )

    # Gmail submission over STARTTLS (port 587).
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())


def send_email(new_jobs):
    if not new_jobs:
        return

    subject = f"{len(new_jobs)} New Job(s) Found at E2F Trustscale"
    body = "Hello,\n\nThe following new job(s) were found:\n\n"

    for job in new_jobs:
        body += f"Job Type: {job['job_type']}\n"
        body += f"Position: {job['title']}\n"
        body += f"Country: {job['country']}\n"
        body += f"Link: {job['url']}\n\n"

    body += "Good luck!\n— Job Alert Bot"

    msg = MIMEMultipart()
    msg["From"] = f"Job Alert Bot <{SENDER_EMAIL or 'unknown'}>"
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        _send_message(msg)
        print(f"Email sent with {len(new_jobs)} new job(s)! Recipient: {RECEIVER_EMAIL}")
    except Exception as exc:
        raise RuntimeError(f"Failed to send email: {exc}") from exc


def send_failure_alert(error_message):
    msg = MIMEMultipart()
    msg["From"] = f"Job Alert Bot <{SENDER_EMAIL or 'unknown'}>"
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Job Alert Bot FAILED"
    body = (
        "The Job Alert Bot run failed and could not complete.\n\n"
        f"Error:\n{error_message}\n\n"
        "Check the GitHub Actions logs for the full traceback."
    )
    msg.attach(MIMEText(body, "plain"))

    try:
        _send_message(msg)
        print("Failure alert email sent.")
    except Exception as exc:
        print(f"Could not send failure alert email either: {exc}")

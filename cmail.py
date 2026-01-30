import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load .env for local development (safe on Render too)
load_dotenv()

SENDER = os.environ["SENDER_EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]

def send_mail(to, subject, body):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = to
    msg["Subject"] = subject

    # Plain text fallback
    msg.set_content(body)

    # Extract OTP safely (last word)
    otp = body.strip().split()[-1]

    # HTML email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #050507;
                margin: 0;
                padding: 0;
                color: #f8fafc;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
            }}
            .logo {{
                font-size: 26px;
                font-weight: bold;
                color: #22d3ee;
                margin-bottom: 25px;
            }}
            .title {{
                font-size: 18px;
                color: #cbd5f5;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            .otp {{
                margin: 30px auto;
                font-size: 40px;
                font-weight: bold;
                letter-spacing: 10px;
                color: #ffffff;
                padding: 20px;
                border: 2px dashed #22d3ee;
                border-radius: 14px;
                width: fit-content;
            }}
            .footer {{
                margin-top: 40px;
                font-size: 12px;
                color: #94a3b8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">SMART NOTE MANAGEMENT</div>
            <div class="title">Verification Code</div>
            <p>Use the code below to complete your registration.</p>
            <div class="otp">{otp}</div>
            <p>This code will expire shortly. If you didn’t request it, ignore this email.</p>
            <div class="footer">
                © 2026 SNM Systems. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    # Send email securely
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, APP_PASSWORD)
        server.send_message(msg)

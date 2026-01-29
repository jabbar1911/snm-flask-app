import smtplib
from  email.message import EmailMessage
app_password='htjp rsnq luim bmfi'

SENDER = "2100031733cser@gmail.com"

def send_mail(to, subject, body):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER, app_password)
    msg = EmailMessage()
    msg['From'] = SENDER
    msg['Subject'] = subject
    msg['To'] = to
    
    # Text version
    msg.set_content(body)
    
    # HTML version for premium look
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Outfit', sans-serif; background-color: #050507; margin: 0; padding: 0; color: #f8fafc; }}
            .container {{ max-width: 600px; margin: 40px auto; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 40px; text-align: center; }}
            .logo {{ font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #22d3ee, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 30px; }}
            .title {{ font-size: 20px; color: #94a3b8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }}
            .otp-box {{ background: rgba(34, 211, 238, 0.1); border: 2px dashed #22d3ee; border-radius: 16px; padding: 20px; font-size: 42px; font-weight: 700; color: #ffffff; letter-spacing: 12px; margin: 30px 0; }}
            .footer {{ font-size: 12px; color: #64748b; margin-top: 40px; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 20px; }}
            .accent {{ color: #22d3ee; text-decoration: none; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">SMART NOTE MANAGEMENT</div>
            <div class="title">Verification Code</div>
            <p style="color: #94a3b8; line-height: 1.6;">Your security is our priority. Use the code below to complete your registration and access your premium workspace.</p>
            <div class="otp-box">{body.split()[-1]}</div>
            <p style="color: #64748b; font-size: 13px;">This code will expire shortly. If you did not request this, please ignore this email.</p>
            <div class="footer">
                &copy; 2026 <span class="accent">SNM</span> Systems. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')
    
    server.send_message(msg)
    server.close()
    
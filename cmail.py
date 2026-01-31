import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
load_dotenv()

# Brevo Configuration
BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
SENDER = os.environ.get('SENDER_EMAIL', 'your-verified-sender@example.com')

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY

def send_mail(to, subject, body):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    try:
        # Extract OTP from body
        otp = body.split()[-1] if body else ""
        
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
                <div class="otp-box">{otp}</div>
                <p style="color: #64748b; font-size: 13px;">This code will expire shortly. If you did not request this, please ignore this email.</p>
                <div class="footer">
                    &copy; 2026 <span class="accent">SNM</span> Systems. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to}],
            sender={"email": SENDER, "name": "SNM"},
            subject=subject,
            html_content=html_content
        )

        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Brevo API Response for {to}: {api_response}")
        return True
    except ApiException as e:
        print(f"EXCEPTION: Brevo API Error for {to}: {e}")
        return False
    except Exception as e:
        print(f"CRITICAL: Email Error for {to}: {e}")
        return False
    

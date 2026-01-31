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
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                    background-color: #f8fafc;
                    padding: 40px 20px;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    border-radius: 16px;
                    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
                    overflow: hidden;
                }}
                
                /* Header with Logo */
                .header {{
                    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                    padding: 50px 40px;
                    text-align: center;
                }}
                .logo {{
                    font-size: 32px;
                    font-weight: 800;
                    color: #ffffff;
                    letter-spacing: 3px;
                    margin-bottom: 8px;
                }}
                .tagline {{
                    font-size: 13px;
                    font-weight: 500;
                    color: rgba(255, 255, 255, 0.9);
                    letter-spacing: 2px;
                    text-transform: uppercase;
                }}
                
                /* Main Content */
                .content {{
                    padding: 50px 40px;
                }}
                .title {{
                    font-size: 24px;
                    font-weight: 700;
                    color: #0f172a;
                    margin-bottom: 16px;
                    text-align: center;
                }}
                .subtitle {{
                    font-size: 15px;
                    color: #64748b;
                    text-align: center;
                    margin-bottom: 40px;
                    line-height: 1.6;
                }}
                
                /* OTP Box */
                .otp-wrapper {{
                    background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%);
                    border: 2px solid #e0e7ff;
                    border-radius: 12px;
                    padding: 40px 30px;
                    text-align: center;
                    margin: 35px 0;
                }}
                .otp-label {{
                    font-size: 12px;
                    font-weight: 600;
                    color: #6366f1;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                    margin-bottom: 20px;
                }}
                .otp-code {{
                    font-size: 56px;
                    font-weight: 800;
                    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    letter-spacing: 16px;
                    font-family: 'Courier New', monospace;
                    margin: 10px 0;
                }}
                .otp-validity {{
                    font-size: 13px;
                    color: #64748b;
                    margin-top: 20px;
                    font-weight: 500;
                }}
                
                /* Info Section */
                .info-section {{
                    background: #fef3c7;
                    border-left: 4px solid #f59e0b;
                    padding: 20px 25px;
                    margin: 30px 0;
                    border-radius: 6px;
                }}
                .info-title {{
                    font-size: 14px;
                    font-weight: 600;
                    color: #92400e;
                    margin-bottom: 8px;
                }}
                .info-text {{
                    font-size: 13px;
                    color: #78350f;
                    line-height: 1.6;
                }}
                
                /* Security Section */
                .security-section {{
                    background: #f8fafc;
                    border-radius: 12px;
                    padding: 30px;
                    margin: 30px 0;
                }}
                .security-title {{
                    font-size: 16px;
                    font-weight: 700;
                    color: #0f172a;
                    margin-bottom: 16px;
                }}
                .security-list {{
                    list-style: none;
                    padding: 0;
                }}
                .security-list li {{
                    font-size: 14px;
                    color: #475569;
                    padding: 10px 0;
                    padding-left: 24px;
                    position: relative;
                    line-height: 1.5;
                }}
                .security-list li:before {{
                    content: "•";
                    position: absolute;
                    left: 8px;
                    color: #3b82f6;
                    font-weight: bold;
                    font-size: 18px;
                }}
                
                /* Divider */
                .divider {{
                    height: 1px;
                    background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
                    margin: 35px 0;
                }}
                
                /* Footer */
                .footer {{
                    background: #0f172a;
                    padding: 40px;
                    text-align: center;
                }}
                .footer-logo {{
                    font-size: 24px;
                    font-weight: 800;
                    color: #ffffff;
                    letter-spacing: 2px;
                    margin-bottom: 12px;
                }}
                .footer-text {{
                    font-size: 13px;
                    color: #94a3b8;
                    margin: 8px 0;
                    line-height: 1.6;
                }}
                .footer-link {{
                    color: #60a5fa;
                    text-decoration: none;
                    font-weight: 500;
                }}
                .footer-link:hover {{
                    color: #93c5fd;
                }}
                .copyright {{
                    font-size: 12px;
                    color: #64748b;
                    margin-top: 25px;
                    padding-top: 20px;
                    border-top: 1px solid #1e293b;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                
                <!-- Header with Logo -->
                <div class="header">
                    <div class="logo">SNM</div>
                    <div class="tagline">Smart Note Management</div>
                </div>
                
                <!-- Main Content -->
                <div class="content">
                    <h1 class="title">Verification Required</h1>
                    <p class="subtitle">
                        We received a request to access your account. Please use the verification code below to complete your authentication and access your secure workspace.
                    </p>
                    
                    <!-- OTP Section -->
                    <div class="otp-wrapper">
                        <div class="otp-label">Your Verification Code</div>
                        <div class="otp-code">{otp}</div>
                        <div class="otp-validity">Valid for 10 minutes</div>
                    </div>
                    
                    <!-- Important Info -->
                    <div class="info-section">
                        <div class="info-title">Important Notice</div>
                        <div class="info-text">
                            If you did not request this verification code, please ignore this email. Your account remains secure and no action is required.
                        </div>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <!-- Security Guidelines -->
                    <div class="security-section">
                        <div class="security-title">Security Guidelines</div>
                        <ul class="security-list">
                            <li>Never share your verification code with anyone, including SNM staff</li>
                            <li>SNM will never ask for your code via email, phone, or text message</li>
                            <li>Always verify the sender email address before entering any codes</li>
                            <li>If you suspect unauthorized access, contact our security team immediately</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <div class="footer-logo">SNM SYSTEMS</div>
                    <p class="footer-text">
                        Professional Note Management Solutions
                    </p>
                    <p class="footer-text">
                        Need help? <a href="mailto:support@snmsystems.com" class="footer-link">Contact Support</a>
                    </p>
                    <p class="footer-text">
                        Visit us at <a href="https://snmsystems.com" class="footer-link">www.snmsystems.com</a>
                    </p>
                    <div class="copyright">
                        © 2026 SNM Systems. All rights reserved.
                    </div>
                </div>
                
            </div>
        </body>
        </html>
        """
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to}],
            sender={"email": SENDER, "name": "SNM Systems"},
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

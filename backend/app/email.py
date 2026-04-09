import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.163.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


def send_reset_email(to_email: str, token: str) -> None:
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "重置您的密码 - 导航站"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    text_body = f"请访问以下链接重置密码（链接1小时内有效）：\n\n{reset_link}"
    html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: system-ui, Arial, sans-serif; background: #f4f4f4; padding: 40px;">
  <div style="max-width: 480px; margin: 0 auto; background: #fff; padding: 40px;">
    <h2 style="color: #171A20; font-weight: 500; margin: 0 0 16px;">重置密码</h2>
    <p style="color: #393C41; font-size: 14px; line-height: 1.6; margin: 0 0 24px;">
      您收到此邮件是因为有人请求重置您的账户密码。如果不是您本人操作，请忽略此邮件。
    </p>
    <a href="{reset_link}"
       style="display: inline-block; background: #3E6AE1; color: #fff; text-decoration: none;
              padding: 10px 24px; border-radius: 4px; font-size: 14px; font-weight: 500;">
      重置密码
    </a>
    <p style="color: #8E8E8E; font-size: 12px; margin: 24px 0 0;">
      链接有效期 1 小时。如无法点击，请复制以下地址到浏览器：<br>
      <span style="color: #5C5E62;">{reset_link}</span>
    </p>
  </div>
</body>
</html>
"""

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())

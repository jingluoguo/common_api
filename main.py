from typing import Union
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Email(BaseModel):
    title: str
    email: str
    content: str | None = None

@app.post("/send_email")
def send_email(email: Email):
    # 邮件配置
    smtp_server = 'smtp.office365.com'  # 邮件服务器
    smtp_port = 587  # 邮件服务器端口号
    sender_email = 'commonapi@outlook.com'  # 发件人邮箱
    sender_password = 'tezrIg-8serba-pojkym'  # 邮箱密码
    receiver_email = email.email  # 收件人邮箱

    # 构建邮件内容
    subject = email.title  # 邮件主题
    text_content = email.content or ""  # 文本内容

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(text_content, 'plain', 'utf-8'))

    # 发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return {"code": 0, "msg": "邮件发送成功"}
    except Exception as e:
        print('邮件发送失败:', str(e))
        return {"code": -1, "msg": "邮件发送失败"}

if __name__ == "__main__":
    # 使用 uvicorn 运行应用程序
    uvicorn.run(app, host="127.0.0.1", port=8000)
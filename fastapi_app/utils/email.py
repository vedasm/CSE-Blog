import os
from fastapi_mail import ConnectionConfig,FastMail,MessageSchema
async def send_contact_email(name,email,message):
    if not os.getenv('EMAIL_HOST'):return
    config=ConnectionConfig(MAIL_USERNAME=os.getenv('EMAIL_HOST_USER',''),MAIL_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD',''),MAIL_FROM=os.getenv('DEFAULT_FROM_EMAIL','cse@example.com'),MAIL_PORT=int(os.getenv('EMAIL_PORT','587')),MAIL_SERVER=os.getenv('EMAIL_HOST'),MAIL_STARTTLS=os.getenv('EMAIL_USE_TLS','true').lower()=='true',MAIL_SSL_TLS=False,USE_CREDENTIALS=True)
    await FastMail(config).send_message(MessageSchema(subject=f'New Contact Message from {name}',recipients=[os.getenv('CONTACT_NOTIFY_EMAIL','')],body=f'From: {name} <{email}>\n\n{message}',subtype='plain'))

# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
# from pydantic import BaseModel, BaseSettings, EmailStr
# from starlette.responses import JSONResponse


# class MailConfig(BaseSettings):
#     """
#     Mail settings.

#     These parameters can be configured
#     with environment variables.
#     """

#     mail_from_name: str = "App Name"
#     mail_username: str = "username"
#     mail_password: str = "**********"
#     mail_from: str = "test@email.com"
#     mail_port: int = 587
#     mail_server: str = "smtp.gmail.com"
#     mail_starttls: bool = False
#     mail_ssl_tls: bool = True
#     mail_use_credentials: bool = True
#     mail_validate_certs: bool = True

#     class Config:
#         env_file = "envs/dev.env"
#         env_file_encoding = "utf-8"


# mail_config = MailConfig()


# conf = ConnectionConfig(
#     MAIL_FROM_NAME=mail_config.mail_from_name,
#     MAIL_USERNAME=mail_config.mail_username,
#     MAIL_PASSWORD=mail_config.mail_password,
#     MAIL_FROM=EmailStr(mail_config.mail_from),
#     MAIL_PORT=mail_config.mail_port,
#     MAIL_SERVER=mail_config.mail_server,
#     MAIL_STARTTLS=mail_config.mail_starttls,
#     MAIL_SSL_TLS=mail_config.mail_ssl_tls,
#     USE_CREDENTIALS=mail_config.mail_use_credentials,
#     VALIDATE_CERTS=mail_config.mail_validate_certs,
# )  # type: ignore

# # print(conf)


# async def send_email_verification_mail(
#     to_email: EmailStr, name: str, token: str
# ) -> JSONResponse:
#     html = f"""
# <html>
#     <body>
#         <p>Hi {name},</p>
#         <p>Welcome to App,</p>
#         <p>Your email : {to_email},</p>
#         <!--# TODO pass token to one api that will update is_verified value-->
#         <p>You can verify your email by clicking on the <a href=http://192.168.1.237:8000/api/user/verify-email?token={token}>link</a>.</p>
#         <p>Regards,</p>
#         <p>App Team</p>
#     </body>
# </html>
# """

#     message = MessageSchema(
#         subject="Verify Your Email",
#         recipients=[to_email],
#         body=html,
#         subtype=MessageType.html,
#     )

#     fm = FastMail(conf)
#     result = await fm.send_message(message)
#     print(f"result :: {result}")
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})

import re

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from users.settings import Settings

def validate_email(email: str) -> bool:
    # Expressão regular para validar e-mail
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(regex, email):
        return True
    else:
        return False
    

def validate_password(password: str) -> bool:
    # Expressão regular para validar a senha
    regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[0-9])(?=.{8,})'
    
    if re.match(regex, password):
        return True
    else:
        return False
    

async def email( email:str, token: str):
    conf = ConnectionConfig(
        MAIL_USERNAME = 'seu_email@gmail.com',
        MAIL_PASSWORD = 'sua_senha',
        MAIL_FROM = 'email',
        MAIL_PORT = 587,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_TLS = True,
        MAIL_SSL = False
    )

    message = MessageSchema(
        subject="Recuperação de senha",
        recipients=[email],
        body=f"Use o seguinte token para recuperar sua senha: {token}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)






if __name__ == '__main__':
# Exemplos de uso
    print(validate_email("teste@example.com"))  # True
    print(validate_email("invalid-email"))      # False

    print(validate_password("Senha@123"))  # True
    print(validate_password("senha123"))   # False
    print(validate_password("SENHA123"))   # False
    print(validate_password("Senha123"))   # False
    print(validate_password("Senha@12"))   # True

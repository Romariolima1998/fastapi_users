import re

from fastapi_mail import FastMail,  ConnectionConfig

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
    

async def email():
    # va ate as configuracoes de seguranca do seu email authenticacao de 2 fatores
    # e crie uma senha para aplicativo
    conf = ConnectionConfig(
        MAIL_USERNAME = Settings().EMAIL,
        MAIL_PASSWORD = Settings().PASSWORD,
        MAIL_FROM = Settings().EMAIL,
        MAIL_PORT = 587,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False
    )    

    fm = FastMail(conf)

    return fm
    






if __name__ == '__main__':
# Exemplos de uso
    print(validate_email("teste@example.com"))  # True
    print(validate_email("invalid-email"))      # False

    print(validate_password("Senha@123"))  # True
    print(validate_password("senha123"))   # False
    print(validate_password("SENHA123"))   # False
    print(validate_password("Senha123"))   # False
    print(validate_password("Senha@12"))   # True

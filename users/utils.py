import re

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



if __name__ == '__main__':
# Exemplos de uso
    print(validate_email("teste@example.com"))  # True
    print(validate_email("invalid-email"))      # False

    print(validate_password("Senha@123"))  # True
    print(validate_password("senha123"))   # False
    print(validate_password("SENHA123"))   # False
    print(validate_password("Senha123"))   # False
    print(validate_password("Senha@12"))   # True

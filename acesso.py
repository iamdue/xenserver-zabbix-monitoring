import base64
import getpass

def geraCredenciais():
    user = getpass.getpass('User:')
    password = getpass.getpass('Password:')
    user_e = base64.b64encode(user.encode("utf-8"))
    password_e = base64.b64encode(password.encode("utf-8"))
    
    arq = open("credentials.txt", "w")
    arq.write(user_e+'\n')
    arq.write(password_e)
    arq.close()

def decode(codigo):
    codigo = base64.b64decode(codigo)
    return codigo

if __name__ == "__main__":
    geraCredenciais()

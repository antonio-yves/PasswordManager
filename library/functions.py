import getpass
import hashlib
import os

def validPassword(password):
  passwordHash = hashlib.md5(password.encode()).hexdigest()
  return passwordHash

def insertUser(cursor, username, password):
  passwordHash = validPassword(password)
  cursor.execute('''
    INSERT INTO user (username, password) VALUES ('{}', '{}');
  '''.format(username, passwordHash))
  return True

def firstExecution(cursor, conn, username, password):
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
      username text,
      password text
    );
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS service(
        serviceName text,
        username text,
        password text
      );
  ''')
  if (insertUser(cursor, username, password)):
    conn.commit()
    return True
  return False

def login(cursor, username, password):
  user = cursor.execute('''
    SELECT * FROM user WHERE username = '{}';
  '''.format(username)).fetchone()
  if (not user):
    return False
  if (user[1] == validPassword(password)):
    return True
  return "Senha incorreta, tente novamente"

def addService(cursor, serviceName, username, password):
  cursor.execute('''
    INSERT INTO service (serviceName, username, password) VALUES ('{}', '{}', '{}');
  '''.format(serviceName, username, password))
  return True

def indexServices(cursor):
  services = cursor.execute('''
    SELECT (serviceName) FROM service;
  ''').fetchall()
  return services

def recoveryPassword(cursor, serviceName):
  service = cursor.execute('''
    SELECT * FROM service WHERE serviceName = '{}';
  '''.format(serviceName)).fetchone()
  return service

def mainMenu(cursor, conn):
  print("***** GERENCIADOR DE SENHAS - MAIN MENU *****")
  print("1 - Adicionar serviço")
  print("2 - Listar serviços")
  print("3 - Recuperar senha")
  print("0 - Sair")
  op = input("Informe a opção desejada: ")
  if not op in ['1', '2', '3', '0']:
    return "Opção inválida! Informe uma opção válida.\n"
  elif op == "0":
    conn.commit()
    cursor.close()
    exit()
  elif op == "1":
    if (os.name == "nt"):
      os.system("cls")
    else:
      os.system("clear")
    print("***** ADICIONAR SERVIÇO *****\n")
    serviceName = input("Informe o nome do serviço: ")
    username = input("Informe o username: ")
    password = input("Informe a senha: ")
    if (addService(cursor, serviceName, username, password)):
      return "Serviço adicionado com sucesso!\n"
    return "Algo deu errado... Por favor, tente cadastrar novamente!"
  elif op == "2":
    if (os.name == "nt"):
      os.system("cls")
    else:
      os.system("clear")
    print("***** LISTA DE SERVIÇOS *****\n")
    services = indexServices(cursor)
    for service in services:
      print("Nome do serviço: {}\n".format(service[0]))
    return ""
  else:
    if (os.name == "nt"):
      os.system("cls")
    else:
      os.system("clear")
    print("***** RECUPERAR SENHA *****\n")
    serviceName = input("Informe o nome do serviço: ")
    service = recoveryPassword(cursor, serviceName)
    print("\nUsername: %s" % service[1])
    print("\nPassword: %s" % service[2])
    return ""

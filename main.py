import sqlite3
import os
from library import functions
import getpass

def menu(cursor, conn):
  while True:
    if (os.name == "nt"):
      os.system("cls")
    else:
      os.system("clear")
    print(functions.mainMenu(cursor, conn))
    os.system("PAUSE")

if (not os.path.exists('db.sqlite')):
  print("****** Bem-vindo(a), para começar, crie seu cadastro! ******")
  conn = sqlite3.connect('db.sqlite')
  cursor = conn.cursor()
  username = input('Informe o nome de usuário: ')
  password = getpass.getpass('Infome a senha: ')
  functions.firstExecution(cursor, conn, username, password)
  menu(cursor, conn)

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

while True:
  print("// Note que os campos diferenciam maiúsculas e minúsculas")
  username = input("Informe seu usuário: ")
  password = getpass.getpass("Informe sua senha: ")
  aux = functions.login(cursor, username, password)
  if (aux == True):
    break
  elif (aux == False):
    print("Usuário não encontrado... Tente novamente!")
  else:
    print(aux)

menu(cursor, conn)

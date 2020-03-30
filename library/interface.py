import tkinter as tk
from tkinter import messagebox
from . import functions
from PIL import Image, ImageTk

class LoginApplication(tk.Frame):
    def __init__(self, cursor, conn, master=None):
      super().__init__(master)
      self.master = master
      self.cursor = cursor
      self.conn = conn
      self.pack()
      self.createLoginWidgets()

    def createLoginWidgets(self):
      imagem = Image.open("assets/user_password.png")
      imagem = imagem.resize((150, 150))
      photo = ImageTk.PhotoImage(imagem)

      self.loginImageLabel = tk.Label(self, image = photo)
      self.loginImageLabel.image = photo
      self.loginImageLabel.grid(row = 0, column = 0, columnspan = 2, ipady = 30)

      self.loginLabel = tk.Label(self, text='Username')
      self.loginInput = tk.Entry(self, width = 25)

      self.passwordLabel = tk.Label(self, text='Password')
      self.passwordInput = tk.Entry(self, width = 25, show='*')

      self.loginLabel.grid(row = 1, column = 0, ipadx = 10)
      self.loginInput.grid(row = 1, column = 1)

      self.passwordLabel.grid(row = 2, column = 0, ipadx = 10, ipady = 15)
      self.passwordInput.grid(row = 2, column = 1)

      self.buttonLogin = tk.Button(self, text = "Login", width = 10, command = self.login)
      self.buttonLogin.grid(row = 4, column = 0, columnspan = 2)

    def errorBox(self, message):
      self.show_message = messagebox.showerror('Erro!', message)

    def login(self):
      if (functions.login(self.cursor, self.loginInput.get(), self.passwordInput.get()) == True):
        menu = tk.Tk()
        menu.geometry("600x400")
        menu.title("Gerenciador de Senhas")
        menu.iconbitmap(r'assets/favicon.ico')
        menu.resizable(0,0)
        cursor = self.cursor
        conn = self.conn
        self.master.destroy()
        app = MenuApplication(cursor, conn, menu)
      elif (self.passwordInput.get() == "" and self.loginInput.get() == ""):
        self.errorBox("Informe um usuário e senha para continuar.")
      elif (self.passwordInput.get() == ""):
        self.errorBox("Informe a senha para continuar.")
      elif (self.loginInput.get() == ""):
        self.errorBox("Informe seu usuário para continuar.")
      elif (not functions.login(self.cursor, self.loginInput.get(), self.passwordInput.get())):
        self.errorBox("Usuário não encontrado ou não cadastrado!")
      else:
        self.errorBox(functions.login(self.cursor, self.loginInput.get(), self.passwordInput.get()))

class MenuApplication(tk.Frame):
    def __init__(self, cursor, conn, master=None):
      super().__init__(master)
      self.master = master
      self.cursor = cursor
      self.conn = conn
      self.pack()
      self.createMenuWidgets()

    def createMenuWidgets(self):
      servico = functions.recoveryPassword(self.cursor, 'Spotify')
      self.infoLabel = tk.Label(self, text = 'Hello')
      self.infoLabel.pack()
      self.serviceName = tk.Label(self, text = servico[0])
      self.serviceName.pack()

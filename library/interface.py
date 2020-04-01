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
      self.menuBar = tk.Menu(self)
      self.menuFile = tk.Menu(self.menuBar, tearoff = 0)
      self.menuFile.add_command(label = 'Adicionar Serviço', command = lambda: self.addService(AddService))
      self.menuFile.add_command(label = 'Mostrar Serviços')
      self.menuFile.add_command(label = 'Recuperar Serviço')
      self.menuFile.add_separator()
      self.menuFile.add_command(label = 'Sair')
      self.menuBar.add_cascade(label = 'Arquivo', menu = self.menuFile)

      self.menuHelp = tk.Menu(self.menuBar, tearoff = 0)
      self.menuHelp.add_command(label = 'Documentação')
      self.menuHelp.add_separator()
      self.menuHelp.add_command(label = 'Sobre')
      self.menuBar.add_cascade(label = 'Ajuda', menu = self.menuHelp)

      self.master.config(menu = self.menuBar)

      imagem = Image.open("assets/user_password.png")
      imagem = imagem.resize((150, 150))
      photo = ImageTk.PhotoImage(imagem)

      self.ImageLabel = tk.Label(self, image = photo)
      self.ImageLabel.image = photo
      self.ImageLabel.grid(row = 0, column = 0, columnspan = 3, ipady = 100)

    def addService(self, _class):
      self.newWindow = tk.Toplevel(self.master)
      _class(self.newWindow, self.cursor, self.conn)

class AddService(tk.Frame):
  def __init__(self, root, cursor, conn):
    super().__init__(root)
    self.root = root
    self.root.geometry("400x200")
    self.root.iconbitmap(r'assets/favicon.ico')
    self.root.title("Gerenciador de Senhas - Adicionar Serviço")
    self.root.resizable(0,0)
    self.cursor = cursor
    self.conn = conn
    self.pack()
    self.createWidgets()

  def createWidgets(self):
    self.serviceLabel = tk.Label(self, text='Nome do Serviço')
    self.serviceInput = tk.Entry(self, width = 25)

    self.usernameLabel = tk.Label(self, text='Username')
    self.usernameInput = tk.Entry(self, width = 25)

    self.passwordLabel = tk.Label(self, text='Password')
    self.passwordInput = tk.Entry(self, width = 25, show='*')

    self.serviceLabel.grid(row = 0, column = 0, ipady = 15)
    self.serviceInput.grid(row = 0, column = 1)

    self.usernameLabel.grid(row = 1, column = 0, ipadx = 10)
    self.usernameInput.grid(row = 1, column = 1)

    self.passwordLabel.grid(row = 2, column = 0, ipadx = 10, ipady = 15)
    self.passwordInput.grid(row = 2, column = 1)

    self.buttonCadastrar = tk.Button(self, text = "Cadastrar", width = 10, command = self.cadastrarServico)
    self.buttonCadastrar.grid(row = 4, column = 0, columnspan = 2)

  def cadastrarServico(self):
    if ((self.serviceInput.get() == "") and (self.usernameInput.get() == "") and (self.passwordInput.get() == "")):
      self.errorBox('Por favor, informe os dados necessários antes de continuar!')
    elif (self.serviceInput.get() == ""):
      self.errorBox('Por favor, informe o nome do serviço!')
    elif (self.usernameInput.get() == ""):
      self.errorBox('Por favor, informe o Username para continuar!')
    elif (self.passwordInput.get() == ""):
      self.errorBox('Por favor, informe a senha para continuar!')
    else:
      if (functions.addService(self.cursor, self.serviceInput.get(), self.usernameInput.get(), self.passwordInput.get(), self.conn) == True):
        self.infoBox('Serviço cadastradado com sucesso.')
        self.master.destroy()
      else:
        self.errorBox('Erro ao cadastrar serviço!')

  def errorBox(self, message):
    self.show_message = messagebox.showerror('Erro!', message)

  def infoBox(self, message):
    self.show_message = messagebox.showinfo('Sucesso', message)

class ShowServices(tk.Frame):
  def __init__(self, root, cursor, conn):
    super().__init__(root)
    self.root = root
    self.root.geometry("400x200")
    self.root.iconbitmap(r'assets/favicon.ico')
    self.root.title("Gerenciador de Senhas - Mostrar Serviços")
    self.root.resizable(0,0)
    self.cursor = cursor
    self.conn = conn
    self.pack()
    self.createWidgets()

  def createWidgets(self):
    '''
    função ainda não implementada
    '''
    indexServices = functions.indexServices(self.cursor)
    index = 1

    self.id = tk.Label(self, text = 'ID')
    self.serviceName = tk.Label(self, text = 'Nome do Serviço')

    for service in indexServices:
      self.serviceLabelID = tk.Label(self, text='{}'.format(index))
      self.serviceLabelName = tk.Label(self, text = '{}'.format(service[0]))
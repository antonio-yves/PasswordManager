import tkinter as tk
from library import interface
import sqlite3
import os

root = tk.Tk()
root.geometry("600x400")
root.title("Gerenciador de Senhas")
root.iconbitmap(r'assets/favicon.ico')
root.resizable(0,0)

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
app = interface.MenuApplication(cursor, conn, master = root)
app.mainloop()
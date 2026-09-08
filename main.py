import tkinter as tk
from tkinter import messagebox

def fazer_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if usuario == "admin" and senha == "1234":
        messagebox.showinfo("Login", "Login realizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")


# Criação da janela principal
janela = tk.Tk()
janela.title("Sistema de Login")
janela.geometry("350x220")
janela.resizable(False, False)

# Título
titulo = tk.Label(
    janela,
    text="Login",
    font=("Arial", 20, "bold")
)
titulo.pack(pady=15)

# Usuário
label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack()

entrada_usuario = tk.Entry(janela, width=30)
entrada_usuario.pack(pady=5)

# Senha
label_senha = tk.Label(janela, text="Senha:")
label_senha.pack()

entrada_senha = tk.Entry(janela, width=30, show="*")
entrada_senha.pack(pady=5)

# Botão
botao_login = tk.Button(
    janela,
    text="Entrar",
    width=15,
    command=fazer_login
)
botao_login.pack(pady=15)

# Mantém a aplicação aberta
janela.mainloop()
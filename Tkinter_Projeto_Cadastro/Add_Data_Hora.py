# Inserir a data

import tkinter as tk
from tkinter import Entry, Button
from datetime import datetime

# Função para atualizar a data no Entry


def atualizar_data():
    data_atual = datetime.now().strftime("%d/%m/%Y")
    entry_data.delete(0, tk.END)  # Limpa o conteúdo atual
    entry_data.insert(0, data_atual)  # Insere a nova data


# Criação da janela principal
janela = tk.Tk()
janela.title("Data Atual")

# Criação do Entry
entry_data = Entry(janela, font=("Arial", 14), justify="center")
entry_data.pack(pady=10)

# Criação do Botão
btn_atualizar = Button(janela, text="Atualizar Data", command=atualizar_data)
btn_atualizar.pack(pady=10)

# Loop principal da interface
janela.mainloop()

# Função para atualizar o horário no Entry


def atualizar_horario():
    horario_atual = datetime.now().strftime("%H:%M:%S")
    entry_horario.delete(0, tk.END)  # Limpa o conteúdo atual
    entry_horario.insert(0, horario_atual)  # Insere o novo horário


# Criação da janela principal
janela = tk.Tk()
janela.title("Hora Atual")

# Criação do Entry
entry_horario = Entry(janela, font=("Arial", 14), justify="center")
entry_horario.pack(pady=10)

# Criação do Botão
btn_atualizar = Button(janela, text="Atualizar Hora",
                       command=atualizar_horario)
btn_atualizar.pack(pady=10)

# Loop principal da interface
janela.mainloop()

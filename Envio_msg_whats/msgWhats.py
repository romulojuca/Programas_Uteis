import tkinter as tk
from tkinter import messagebox
import pywhatkit
import datetime
import time

# Lista de contatos predefinida
contatos = [
    "+5535997660937",
    "+5535991528521"
]

# Função para envio individual agendado


def enviar_individual():
    numero = entrada_numero.get()
    mensagem = entrada_mensagem.get("1.0", tk.END).strip()
    hora = entrada_hora.get()
    minuto = entrada_minuto.get()

    if not numero.startswith("+"):
        messagebox.showwarning("Número inválido", "Use o formato +55...")
        return
    if not mensagem:
        messagebox.showwarning("Mensagem vazia", "Digite uma mensagem.")
        return
    if not hora.isdigit() or not minuto.isdigit():
        messagebox.showwarning(
            "Hora inválida", "Hora e minuto devem ser números.")
        return

    hora = int(hora)
    minuto = int(minuto)

    try:
        pywhatkit.sendwhatmsg(numero, mensagem, hora,
                              minuto, wait_time=8, tab_close=True)
        log.insert(
            tk.END, f"⏰ Agendado para {numero} às {hora:02d}:{minuto:02d}\n")
        log.see(tk.END)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Função para envio para todos agendado


def enviar_para_todos():
    mensagem = entrada_mensagem.get("1.0", tk.END).strip()
    hora = entrada_hora.get()
    minuto = entrada_minuto.get()

    if not mensagem:
        messagebox.showwarning("Mensagem vazia", "Digite uma mensagem.")
        return
    if not hora.isdigit() or not minuto.isdigit():
        messagebox.showwarning(
            "Hora inválida", "Hora e minuto devem ser números.")
        return

    hora = int(hora)
    minuto = int(minuto)

    try:
        for i, numero in enumerate(contatos):
            # Envio com diferença de 1 minuto entre contatos
            hora_envio = hora + ((minuto + i) // 60)
            minuto_envio = (minuto + i) % 60

            pywhatkit.sendwhatmsg(
                numero,
                mensagem,
                hora_envio,
                minuto_envio,
                wait_time=8,     # reduzido
                tab_close=True
            )

            log.insert(
                tk.END, f"⏰ Agendado para {numero} às {hora_envio:02d}:{minuto_envio:02d}\n")
            log.see(tk.END)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Criação da interface
janela = tk.Tk()
janela.title("WhatsApp - Agendamento de Mensagens")
janela.geometry("500x550")

# Número individual
tk.Label(janela, text="Número (+55...):").pack(pady=5)
entrada_numero = tk.Entry(janela, width=30)
entrada_numero.pack()

# Mensagem
tk.Label(janela, text="Mensagem:").pack(pady=5)
entrada_mensagem = tk.Text(janela, height=5, width=50)
entrada_mensagem.pack()

# Horário
frame_hora = tk.Frame(janela)
frame_hora.pack(pady=5)
tk.Label(frame_hora, text="Hora (0-23):").grid(row=0, column=0, padx=5)
entrada_hora = tk.Entry(frame_hora, width=5)
entrada_hora.grid(row=0, column=1)

tk.Label(frame_hora, text="Minuto (0-59):").grid(row=0, column=2, padx=5)
entrada_minuto = tk.Entry(frame_hora, width=5)
entrada_minuto.grid(row=0, column=3)

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_individual = tk.Button(
    frame_botoes, text="Agendar Individual", command=enviar_individual)
btn_individual.grid(row=0, column=0, padx=10)

btn_lista = tk.Button(
    frame_botoes, text="Agendar para Todos", command=enviar_para_todos)
btn_lista.grid(row=0, column=1, padx=10)

# Log
tk.Label(janela, text="Log de Agendamentos:").pack()
log = tk.Text(janela, height=12, width=60)
log.pack()

janela.mainloop()

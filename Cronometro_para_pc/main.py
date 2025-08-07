import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import os
import json
from cronometro import Cronometro


class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<Tab>', self.complete)  # Completa com Tab

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())
        texto = self.get().lower()
        self._hits = [
            item for item in self._completion_list if item.lower().startswith(texto)]

        if self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        if event.keysym == "BackSpace":
            self.position = self.index(tk.END)
        elif event.keysym == "Left":
            if self.position < self.index(tk.END):
                self.position = self.position - 1
        elif event.keysym == "Right":
            self.position = self.index(tk.END)
        else:
            self.autocomplete(0)

    def complete(self, event):
        self.autocomplete(1)
        return "break"  # Evita que Tab mude o foco


ARQUIVO_SALVO = "cronometros.json"
style = Style("cosmo")

janela = style.master
janela.title("Cronômetro")

frame_inputs = ttk.Frame(janela)
frame_inputs.pack(pady=10)

entrada_nome = ttk.Entry(frame_inputs, width=20)
entrada_nome.grid(row=0, column=0, padx=5)

entrada_minutos = ttk.Entry(frame_inputs, width=5)
entrada_minutos.grid(row=0, column=1, padx=5)

entrada_segundos = ttk.Entry(frame_inputs, width=5)
entrada_segundos.grid(row=0, column=2, padx=5)

figuras_path = "figuras"
os.makedirs(figuras_path, exist_ok=True)
figuras = [f for f in os.listdir(figuras_path) if f.endswith((".png", ".jpg"))]

figura_var = tk.StringVar()

combo_figuras = AutocompleteCombobox(
    frame_inputs, width=20, textvariable=figura_var)
combo_figuras.set_completion_list(figuras)
combo_figuras.grid(row=0, column=3, padx=5)


frame_canvas = ttk.Frame(janela)
frame_canvas.pack(fill="both", expand=True)

canvas = tk.Canvas(frame_canvas)
scrollbar = ttk.Scrollbar(
    frame_canvas, orient="vertical", command=canvas.yview)

scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_lista = scrollable_frame

cronometros = []


def salvar_dados():
    dados = [
        {
            "nome": c.nome,
            "tempo_restante": c.tempo_restante,
            "imagem": c.imagem_path
        } for c in cronometros
    ]
    with open(ARQUIVO_SALVO, "w") as f:
        json.dump(dados, f)


def remover_cronometro(cron):
    cronometros.remove(cron)
    cron.frame.destroy()
    salvar_dados()


def ordenar_cronometros():
    # Ordena a lista com base no tempo restante
    cronometros.sort(key=lambda c: c.tempo_restante)

    # Reposiciona os frames na interface
    for c in cronometros:
        c.frame.pack_forget()  # Remove temporariamente
        c.frame.pack(fill='x', padx=5, pady=2)  # Reinsere na ordem correta


def atualizar_ordem():
    ordenar_cronometros()
    janela.after(1000, atualizar_ordem)


def adicionar_cronometro():
    nome = entrada_nome.get()
    minutos = entrada_minutos.get()
    segundos = entrada_segundos.get()
    nome_imagem = figura_var.get().strip()
    figuras_lower = [f.lower() for f in figuras]

    if not nome_imagem or nome_imagem.lower() not in figuras_lower:
        print("Imagem inválida ou não selecionada!")
        return

    indice = figuras_lower.index(nome_imagem.lower())
    nome_imagem_corrigido = figuras[indice]
    imagem = os.path.join(figuras_path, nome_imagem_corrigido)

    try:
        tempo_total = int(minutos) * 60 + int(segundos)
    except ValueError:
        return

    cron = Cronometro(frame_lista, nome, tempo_total, imagem,
                      remover_callback=remover_cronometro)
    cron.iniciar()
    cronometros.append(cron)
    salvar_dados()

    entrada_nome.delete(0, tk.END)
    entrada_minutos.delete(0, tk.END)
    entrada_segundos.delete(0, tk.END)


btn_adicionar = ttk.Button(
    frame_inputs, text="Adicionar", command=adicionar_cronometro)
btn_adicionar.grid(row=0, column=4, padx=5)

# Carrega os cronômetros salvos, se houver
if os.path.exists(ARQUIVO_SALVO):
    with open(ARQUIVO_SALVO, "r") as f:
        try:
            dados_salvos = json.load(f)
            for dados in dados_salvos:
                cron = Cronometro(
                    frame_lista,
                    dados["nome"],
                    dados["tempo_restante"],
                    dados["imagem"],
                    remover_callback=remover_cronometro
                )
                cronometros.append(cron)
        except json.JSONDecodeError:
            pass

atualizar_ordem()
janela.mainloop()

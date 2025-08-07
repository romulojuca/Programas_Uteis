import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import pygame
import os

pygame.mixer.init()


class Cronometro:
    def __init__(self, master, nome, tempo_restante, imagem_path, remover_callback=None):
        self.master = master
        self.nome = nome
        self.tempo_restante = tempo_restante
        self.imagem_path = imagem_path
        self.remover_callback = remover_callback

        self.frame = ttk.Frame(master)
        self.frame.pack(fill='x', padx=5, pady=2)

        self.img = self.carregar_imagem(imagem_path)
        self.label_img = ttk.Label(self.frame, image=self.img)
        self.label_img.image = self.img
        self.label_img.pack(side='left', padx=5)

        self.label_nome = ttk.Label(self.frame, text=nome, width=20)
        self.label_nome.pack(side='left')

        self.label_tempo = ttk.Label(self.frame, text=self.formatar_tempo())
        self.label_tempo.pack(side='left', padx=10)

        self.btn_iniciar = ttk.Button(
            self.frame, text="▶", width=3, command=self.iniciar)
        self.btn_iniciar.pack(side="left")

        self.btn_pausar = ttk.Button(
            self.frame, text="⏸", width=3, command=self.pausar)
        self.btn_pausar.pack(side="left")

        self.btn_resetar = ttk.Button(
            self.frame, text="🔄", width=3, command=self.resetar)
        self.btn_resetar.pack(side="left")

        self.btn_excluir = ttk.Button(
            self.frame, text="🗑", width=3, command=self.deletar)
        self.btn_excluir.pack(side="right", padx=5)

        self.tempo_inicial = tempo_restante
        self.contando = False
        self.atualizar()

    def carregar_imagem(self, path):
        try:
            imagem = Image.open(path)
            imagem = imagem.resize((30, 30))
            return ImageTk.PhotoImage(imagem)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            return None

    def formatar_tempo(self):
        total_segundos = self.tempo_restante
        sinal = "-" if total_segundos < 0 else ""
        total_segundos = abs(total_segundos)

        minutos = total_segundos // 60
        segundos = total_segundos % 60

        return f"{sinal}{minutos:02}:{segundos:02}"

    def atualizar(self):
        if self.contando:
            self.tempo_restante -= 1
            if self.tempo_restante == 0:
                self.tocar_alarme()
        self.label_tempo.config(text=self.formatar_tempo())
        self.frame.after(1000, self.atualizar)

    def iniciar(self):
        self.contando = True

    def pausar(self):
        self.contando = False

    def resetar(self):
        self.tempo_restante = self.tempo_inicial
        self.label_tempo.config(text=self.formatar_tempo())
        self.contando = True

    def parar(self):
        self.contando = False

    def deletar(self):
        self.parar()
        if self.remover_callback:
            self.remover_callback(self)

    def tocar_alarme(self):
        caminho_som = os.path.join(os.getcwd(), "alarme.mp3")
        if os.path.exists(caminho_som):
            pygame.mixer.music.load(caminho_som)
            pygame.mixer.music.play()

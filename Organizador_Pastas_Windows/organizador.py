import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Dicionário de categorias e extensões
extensoes = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt"],
    "Compactados": [".zip", ".rar", ".7z"],
    "Executáveis": [".exe", ".msi"],
    "Planilhas": [".xls", ".xlsx", ".csv"]
}


# Função principal de organização
def organizar_pasta(pasta_alvo, log_widget):
    try:
        arquivos_organizados = 0  # Contador

        # Garante que as subpastas existem
        for pasta in extensoes:
            caminho = os.path.join(pasta_alvo, pasta)
            if not os.path.exists(caminho):
                os.makedirs(caminho)

        # Percorre todos os arquivos da pasta
        for arquivo in os.listdir(pasta_alvo):
            caminho_completo = os.path.join(pasta_alvo, arquivo)

            # Se for arquivo (ignora pastas)
            if os.path.isfile(caminho_completo):
                nome, ext = os.path.splitext(arquivo)

                # Procura a extensão no dicionário
                for pasta, lista_ext in extensoes.items():
                    if ext.lower() in lista_ext:
                        destino = os.path.join(pasta_alvo, pasta, arquivo)

                        if not os.path.exists(destino):
                            shutil.move(caminho_completo, destino)
                            arquivos_organizados += 1

                            # Exibe no campo de log o arquivo movido
                            log_widget.insert(
                                tk.END, f"Movido: {arquivo} → {pasta}\n")
                            log_widget.see(tk.END)  # Rola até o final
                        break

        # Mostra mensagem final
        messagebox.showinfo(
            "Sucesso", f"{arquivos_organizados} arquivos organizados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Função chamada ao clicar no botão


def escolher_pasta():
    pasta = filedialog.askdirectory()  # Abre seletor de pasta
    if pasta:
        log_text.delete(1.0, tk.END)   # Limpa o log anterior
        organizar_pasta(pasta, log_text)


# Criação da interface
janela = tk.Tk()
janela.title("Organizador de Arquivos")
janela.geometry("400x400")

# Título/instrução
label = tk.Label(janela, text="Escolha uma pasta para organizar", pady=10)
label.pack()

# Botão de ação
botao = tk.Button(janela, text="Selecionar Pasta", command=escolher_pasta)
botao.pack(pady=10)

# Área de log dos arquivos movidos (rolável)
log_text = tk.Text(janela, height=15, width=50)
log_text.pack(pady=10)

# Inicia o loop da interface
janela.mainloop()

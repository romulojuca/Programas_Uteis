from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from PIL import ImageTk, Image
import base64
from tkcalendar import Calendar, DateEntry


root = Tk()  # cria a janela do programa


class Validadores():
    # return True significa que pode fazer a ação
    # return False, ele nao deixa fazer a ação
    def validate_entry4(self, text):
        if text == '':
            return True
        try:
            # tenta converter para inteiro, se nao conseguir...
            value = int(text)
        except ValueError:  # usado para nao deixar o programa quebrar
            return False
        return 0 <= value <= 10000  # só deixa digitar de 1 a 9999 ou seja 4 numeros


class Relatorios():
    def printCliente(self):
        # chamar o browser
        webbrowser.open("cliente.pdf")

    def gerarRelatorio(self):
        self.c = canvas.Canvas("cliente.pdf")
        # criar uma variavel para cada entry que vai vim pro relatorio
        self.codigoRelatorio = self.codigo_entry.get()
        self.nomeRelatorio = self.nome_entry.get()
        self.telefoneRelatorio = self.telefone_entry.get()
        self.cidadeRelatorio = self.cidade_entry.get()
        # fonte do relatorio
        self.c.setFont("Helvetica-Bold", 24)
        # define largura x e y e passa o que vai ser escrito no pdf
        self.c.drawString(200, 790, 'Ficha do Cliente')
        # define posicao e escrito tambem
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone: ')
        self.c.drawString(50, 600, 'Cidade: ')
        # define a posicao e joga os valores:
        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRelatorio)
        self.c.drawString(150, 670, self.nomeRelatorio)
        self.c.drawString(150, 630, self.telefoneRelatorio)
        self.c.drawString(150, 600, self.cidadeRelatorio)
        # fill é se vai preencher o fundo F= nao
        self.c.rect(20, 590, 530, 240, fill=False,
                    stroke=True)

        # chamar o pdf e salvar a baixo
        self.c.showPage()
        self.c.save()
        self.printCliente()


class Funcs():
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect(
            'projetoclientes.bd')  # conecta e da o nome
        # disse que é pra ficar mais facil e dar uma melhorada
        self.cursor = self.conn.cursor()
        print('Conectando ao BD')

    def desconecta_bd(self):
        self.conn.close()
        print('Desconectando ao BD')

    def montaTabelas(self):
        self.conecta_bd()
        # Criar tabela, not null nao pode ter o campo sem nada,
        # tipos e tamanhos dos campos, primary key alimenta sozinho com numeros
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS projetoclientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit()
        print('Banco de dados criado')
        self.desconecta_bd()

    def variaveis(self):
        # pega os valores e atribui a variavel
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.cidade = self.cidade_entry.get()
        self.telefone = self.telefone_entry.get()

    def add_cliente(self):
        self.variaveis()
        if self.nome_entry.get() == "":
            msg = "É necessario um nome!"
            messagebox.showinfo("ERRO !!", msg)
        else:
            self.conecta_bd()

        self.cursor.execute(
            """ INSERT INTO projetoclientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def select_lista(self):
        self.listaCliente.delete(*self.listaCliente.get_children())
        self.conecta_bd()
        # pegando os dados do Banco de DADOS
        lista = self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone,
            cidade FROM projetoclientes ORDER BY nome_cliente ASC;  """)
        for i in lista:
            self.listaCliente.insert("", END, values=i)
        self.desconecta_bd()

    def onDoubleClick(self, event):
        # teve que passar o parametro event porque
        # há interação com essa def e ai se vc nao colocar ela nao roda
        self.limpar_tela()
        self.listaCliente.selection()

        for n in self.listaCliente.selection():
            col1, col2, col3, col4 = self.listaCliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(
            """ DELETE FROM projetoclientes WHERE cod = ? """, (self.codigo,))
        # passa essa virgula no final do execute para dizer que é uma tupla
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE projetoclientes SET nome_cliente = ?,
        telefone = ?, cidade = ?
        WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCliente.delete(*self.listaCliente.get_children())
        # insere a % no nome, pois o sistema usa ela para buscar
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        # da um execute e passa o nome das tabelas
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone,
                cidade FROM projetoclientes WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC """ % nome
        )
        # fetchall recolhe as informações do BD e tras em tuplos
        buscanomeCliente = self.cursor.fetchall()
        for i in buscanomeCliente:
            self.listaCliente.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()

    def imagens_base64(self):
        self.btnovo_base64 = 'R0lGODlhLwAbAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAAAvABsAAAj/AAEIHEiwoMGDCBMqXMiwocOHEBcqIzaxIsWLFjNi3JhRIcdPFJVlUiaSJLFPE1FSBKmMZcmXFA+SHMmS4siMI0PazFhyY02DHE9qdHmxpkmjKTsW7Kky5UmdII1GxTgyZ9KRQE0qowUASMVdFqyGvElVa0WxygwmJabohoBTE4M9qGj0qVa7QqESM5iMoqatRgjNJbYOAkV9hAS+3QphGCjEXhErhmtVLcVhyhQZmbciFKhdcxFDILlLQDR2ponlW3FKNGnTFdMW/EsM1FavtBLsC1ZBNQu4qqvc0UcljrJdCaLN+61smD7hTtVipqiZGHEgu0ajjnaY0B1ikCAg4Ta+vbvxkGqT0vKqDPWlucujoXweKtnyZ8zj26bfE6ht6kbUJtlorhEDGneIxTAYYnMNc2BIw1jWF2AX5aNCY8oQJxAC0VQUDADGYaYhAMkRk4wyf1kGSm0XTRiSJhNatGJFK84YkkV9GcRSX33ZBiOKE8LIojI8XkYSZsn85ZhjMRV00X/N8aRTlLT5WBFtsb0o3URJKjNjTizd9NeEEzJZJiiYKSkbQV5ihFlsf+HoF4pZtgmliU1m5dhEaAK5E5O2TdelY2TuRKdCXGIkJZGKBjWjRRFFKumklFZq6UEBAQA7'

    def calendario(self):
        # cria a função calendario dentro da aba 2
        self.calendario1 = Calendar(self.aba2, fg="gray75", bg="blue", font=(
            "Times", 9, 'bold'), locale='pt_br')
        self.calendario1.place(relx=0.5, rely=0.1)
        self.calData = Button(self.aba2, text='Inserir Data',
                              command=self.print_calendario)
        self.calData.place(relx=0.55, rely=0.85, height=25, width=100)

    def print_calendario(self):
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entry_data.delete(0, END)
        self.entry_data.insert(END, dataIni)
        self.calData.destroy()


class Application(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.root = root  # faz uma equivalencia porque o root nao ta dentro da class
        self.imagens_base64()
        self.validaEntradas()
        self.tela()  # inicializa a def tela
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menu()
        root.mainloop()  # cria o loot para a janela do programa nao fechar

    def tela(self):
        self.root.title('Cadastro de Clientes')
        self.root.configure(background='#062530')
        self.root.geometry("700x500")  # Horizontal x Vertical
        # Vai permitir mecher no tamanho da tela em X ou em Y
        self.root.resizable(True, True)
        # dita o tamanho maximo da tela
        self.root.maxsize(width=900, height=700)
        # dita o tamanho minimo da tela
        self.root.minsize(width=400, height=300)

    def frames_da_tela(self):
        # os locais aonde vao aparecer os botoes e as exibições(2 retangulos na tela)
        # bd BORDA, bg COR FUNDO, highlightbackground CorDaBorda, highlightthickness TAMANHO BORDA
        self.frame_1 = Frame(self.root, bd=1, bg='#d1e8f0',
                             highlightbackground='#113642',
                             highlightthickness='3')
        # POSICIONAR O FRAME relxy 0 seria 0% e 1 seria 100%, esquerda para direita, cima para baixo
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        # bd BORDA, bg COR FUNDO, highlightbackground CorDaBorda, highlightthickness TAMANHO BORDA
        self.frame_2 = Frame(self.root, bd=1, bg='#d1e8f0',
                             highlightbackground='#113642',
                             highlightthickness='3')
        # POSICIONAR O FRAME relxy 0 seria 0% e 1 seria 100%, esquerda para direita, cima para baixo
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.48)

    def widgets_frame1(self):
        # criando ABAS
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba1.configure(background='#d1e8f0')
        self.aba2.configure(background='lightgray')
        # da o nov pra elas
        self.abas.add(self.aba1, text='Aba 1')
        self.abas.add(self.aba2, text='Aba 2')
        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        # cria um canvas... uma telinha atras dos botões
        self.canvas_bt1 = Canvas(self.aba1, bd=0, bg='black', highlightbackground='grey',
                                 highlightthickness=3)
        self.canvas_bt1.place(relx=0.244, rely=0.08,
                              relwidth=0.315, relheight=0.18)
        # cria um canvas... uma telinha atras dos botões
        self.canvas_bt2 = Canvas(self.aba1, bd=0, bg='black', highlightbackground='grey',
                                 highlightthickness=3)
        self.canvas_bt2.place(relx=0.645, rely=0.08,
                              relwidth=0.212, relheight=0.18)
        # Botão Limpar, bd = tipo do botao, bg=cor de fundo do botao,
        # fg= cor da letra, font=('font', 'tamanho', 'estilo negrito italico, sublindado etc')
        # active fore e back são as cores quando vc clicar no blotão
        self.bt_limpar = Button(self.aba1, text='Limpar', bd=3, activebackground='blue',
                                activeforeground='yellow',
                                bg='white', fg='black', font=('', 9, 'bold'),
                                command=self.limpar_tela)
        self.bt_limpar.place(relx=0.456, rely=0.1,
                             relwidth=0.1, relheight=0.15)
        # Botão Buscar
        self.bt_buscar = Button(self.aba1, text='Buscar', bd=3,
                                bg='white', fg='black', font=('', 9, 'bold'),
                                command=self.janela_botao_buscar)
        self.bt_buscar.place(relx=0.353, rely=0.1,
                             relwidth=0.1, relheight=0.15)
        # Botão Novo
        # cria uma variavel para receber a imagem que vem do codigo da
        # funçao def imagens_base64
        self.btnovo = PhotoImage(data=base64.b64decode(self.btnovo_base64))
        # sub sample da a cordenada do tamanho do botao que quer que fique
        self.btnovo = self.btnovo.subsample(1, 1)
        self.bt_novo = Button(self.aba1, bd=0, image=self.btnovo,
                              command=self.add_cliente)
        self.bt_novo.place(relx=0.25, rely=0.1, relwidth=0.1, relheight=0.15)
        # Botão Alterar
        self.bt_alterar = Button(self.aba1, text='Alterar', bd=3,
                                 bg='white', fg='black', font=('', 9, 'bold'),
                                 command=self.altera_cliente)
        self.bt_alterar.place(relx=0.65, rely=0.1,
                              relwidth=0.1, relheight=0.15)
        # Botão Apagarr
        self.bt_apagar = Button(self.aba1, text='Apagar', bd=3,
                                bg='white', fg='black', font=('', 9, 'bold'),
                                command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.753, rely=0.1,
                             relwidth=0.1, relheight=0.15)

        # Criação e posição da label no frame 1 e entrada do CÓDIGO no frame 1
        self.lb_codigo = Label(
            self.aba1, text="Código", background='#d1e8f0')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(
            self.aba1, validate='key', validatecommand=self.vcmd2)
        self.codigo_entry.place(relx=0.06, rely=0.15, relwidth=0.08)
        # Criação da label e entrada do NOME no frame 1
        self.lb_nome = Label(
            self.aba1, text="Nome", background="#d1e8f0")
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.aba1)
        self.nome_entry.place(relx=0.06, rely=0.45, relwidth=0.5)
        # Criação da label e entrada do TELEFONER no frame 1
        self.lb_telefone = Label(
            self.aba1, text="Telefone", background="#d1e8f0")
        self.lb_telefone.place(relx=0.05, rely=0.65)

        self.telefone_entry = Entry(self.aba1)
        self.telefone_entry.place(relx=0.06, rely=0.75, relwidth=0.3)
        # Criação da label e entrada do CIDADE no frame 1
        self.lb_cidade = Label(
            self.aba1, text="Cidade", background="#d1e8f0")
        self.lb_cidade.place(relx=0.5, rely=0.65)

        self.cidade_entry = Entry(self.aba1)
        self.cidade_entry.place(relx=0.51, rely=0.75, relwidth=0.4)

        # DROP DOWN BUTTON
        self.Tipvar = StringVar()
        self.TipV = ('Solteiro', 'Casado', 'Divorciado', 'Viuvo')
        self.Tipvar.set('Solteiro')
        self.popupMenu = OptionMenu(self.aba2, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.2)
        self.estado_civil = self.Tipvar.get()
        print(self.estado_civil)

        # Calendario
        self.bt_calendario = Button(
            self.aba2, text="Data", command=self.calendario)
        self.bt_calendario.place(relx=0.5, rely=0.02)
        self.entry_data = Entry(self.aba2, width=10)
        self.entry_data.place(relx=0.5, rely=0.2)

    def lista_frame2(self):
        self.listaCliente = ttk.Treeview(self.frame_2, height=3, columns=(
            'col1', 'col2', 'col3', 'col4'))  # cria a lista no frame 2 e coloca os nomes
        self.listaCliente.heading("#0", text="")
        self.listaCliente.heading('#1', text='Código')
        self.listaCliente.heading('#2', text='Nome')
        self.listaCliente.heading('#3', text='Telefone')
        self.listaCliente.heading('#4', text='Cidade')
        # define o tamanho de cada parte da lista
        self.listaCliente.column('#0', width=1)
        self.listaCliente.column('#1', width=50)
        self.listaCliente.column('#2', width=200)
        self.listaCliente.column('#3', width=125)
        self.listaCliente.column('#4', width=125)
        # Posiciona ela
        self.listaCliente.place(relx=0.01, rely=0.1,
                                relwidth=0.95, relheight=0.85)
        # cria a barra de rolagem nela
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCliente.configure(
            yscroll=self.scroolLista.set)  # coloca ela na tela
        self.scroolLista.place(relx=0.96, rely=0.1,
                               relheight=0.85, relwidth=0.03)  # posiciona ela
        # fazer interação com a lista
        self.listaCliente.bind("<Double-1>", self.onDoubleClick)

    def Menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        # criando as variaveis para cada menu bar que for colocar
        filemenu1 = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()
        # aqui diz que opções vai estar dentro de filemenu
        menubar.add_cascade(label="Opções", menu=filemenu1)
        menubar.add_cascade(label='Relatorio', menu=filemenu2)
        # comand é pra ir adicioanndo as opções dentro do menu
        filemenu1.add_command(label="Sair", command=Quit)
        filemenu1.add_command(label="Limpa Cliente", command=self.limpar_tela)
        filemenu2.add_command(label="Gerar Relatório",
                              command=self.gerarRelatorio)

    def janela_botao_buscar(self):
        self.root2 = Toplevel()
        self.root2.title("Janela 2")
        self.root2.configure(background='lightblue')
        self.root2.geometry("400x200")
        self.root2.resizable(False, False)
        # aqui fala que ela ta vindo da janela principal
        self.root2.transient(self.root)
        # para deixar a segudna janela sempre em primeiro lugar
        self.root2.focus_force()
        # impedir que qualquer coisa seja digitada na outra janela
        # até fechar a segunda
        self.root2.grab_set()

    def validaEntradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry4), '%P')


Application()  # chama a class e inicia tudo

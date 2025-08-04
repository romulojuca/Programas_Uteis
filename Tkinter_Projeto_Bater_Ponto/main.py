import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


root = tk.Tk()


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
    def gerar_relatorio_pdf(self):
        # 1️⃣ Conectar ao banco de dados
        conn = sqlite3.connect('horas.bd')
        cursor = conn.cursor()

        # 2️⃣ Selecionar os dados da tabela 'horas'
        cursor.execute("SELECT * FROM horas")
        dados = cursor.fetchall()
        print(dados)

        # 3️⃣ Definir nome do arquivo e criar o Canvas
        nome_arquivo = f'relatorio_horas_{datetime.today().strftime("%Y-%m-%d")}.pdf'
        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        largura, altura = A4

        # 4️⃣ Cabeçalho do relatório
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, altura - 40, "Relatório de Horas Trabalhadas")

        # 5️⃣ Cabeçalho das colunas
        c.setFont("Helvetica-Bold", 10)
        colunas = ["Código", "Data", "Início", "Parada Alm.",
                   "Retorno Alm.", "Saída", "Total Horas"]
        espacamento = 100
        y = altura - 60

        for coluna in colunas:
            c.drawString(espacamento, y, coluna)
            espacamento += 70

        # 6️⃣ Listar os dados no PDF
        c.setFont("Helvetica", 10)
        y -= 20
        for linha in dados:
            espacamento = 100
            for dado in linha:
                c.drawString(espacamento, y, str(dado))
                espacamento += 70
            y -= 20

            # Quebra de página se não houver mais espaço
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = altura - 40

        # 7️⃣ Finaliza e salva o PDF
        try:
            c.save()
            print(f'Relatório "{nome_arquivo}" gerado com sucesso!')
        except Exception as e:
            print("Erro ao salvar o PDF:", e)
        conn.close()
        print(f'Relatório "{nome_arquivo}" gerado com sucesso!')


class Funcs():
    def conecta_bd(self):
        self.conn = sqlite3.connect(
            'horas.bd')  # conecta e da o nome
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
            CREATE TABLE IF NOT EXISTS horas (
                cod INTEGER PRIMARY KEY,
                data INTEGER(40) NOT NULL,
                inicio STRING(40),
                paradaalm STRING(40),
                retornoalm STRING(40),
                saida STRING(40),
                totalhoras STRING(40)
            );
        """)
        self.conn.commit()
        print('Banco de dados criado')
        self.desconecta_bd()

    def variaveis(self):
        # pega os valores e atribui a variavel
        self.cod = self.codigo_entry.get()
        self.data = self.data_entry.get()
        self.inicio = self.inicio1_entry.get()
        self.paradaalm = self.parada1_entry.get()
        self.retornoalm = self.inicio2_entry.get()
        self.saida = self.parada2_entry.get()

    def add_cliente(self):
        self.variaveis()
        if self.data_entry.get() == "":
            msg = "É necessario uma data!"
            messagebox.showinfo("Preencha a Data", msg)
        else:
            self.conecta_bd()

        self.cursor.execute(
            """ INSERT INTO horas (data, inicio, paradaalm, retornoalm, saida)
            VALUES (?, ?, ?, ?, ?)""", (self.data, self.inicio, self.paradaalm, self.retornoalm, self.saida))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def select_lista(self):
        self.listaCliente.delete(*self.listaCliente.get_children())
        self.conecta_bd()
        # pegando os dados do Banco de DADOS
        lista = self.cursor.execute(
            """ SELECT cod, data, inicio, paradaalm, retornoalm, saida, totalhoras FROM horas ORDER BY data ASC;  """)
        for i in lista:
            self.listaCliente.insert("", END, values=i)
        self.desconecta_bd()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCliente.delete(*self.listaCliente.get_children())
        # insere a % no nome, pois o sistema usa ela para buscar
        self.data_entry.insert(END, '%')
        data = self.data_entry.get()
        # da um execute e passa o nome das tabelas
        self.cursor.execute(
            """ SELECT cod, data, inicio, paradaalm, retornoalm, saida FROM horas WHERE data LIKE '%s' ORDER BY data ASC """ % data
        )
        # fetchall recolhe as informações do BD e tras em tuplos
        buscanomeCliente = self.cursor.fetchall()
        for i in buscanomeCliente:
            self.listaCliente.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()

    def atualizar_horario1(self):
        horario_atual = datetime.now().strftime("%H:%M:%S")
        self.inicio1_entry.delete(0, tk.END)  # Limpa o conteúdo atual
        self.inicio1_entry.insert(0, horario_atual)  # Insere o novo horário

    def atualizar_horario2(self):
        horario_atual = datetime.now().strftime("%H:%M:%S")
        self.parada1_entry.delete(0, tk.END)  # Limpa o conteúdo atual
        self.parada1_entry.insert(0, horario_atual)  # Insere o novo horário

    def atualizar_horario3(self):
        horario_atual = datetime.now().strftime("%H:%M:%S")
        self.inicio2_entry.delete(0, tk.END)  # Limpa o conteúdo atual
        self.inicio2_entry.insert(0, horario_atual)  # Insere o novo horário

    def atualizar_horario4(self):
        horario_atual = datetime.now().strftime("%H:%M:%S")
        self.parada2_entry.delete(0, tk.END)  # Limpa o conteúdo atual
        self.parada2_entry.insert(0, horario_atual)  # Insere o novo horário

    def atualizar_data(self):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.data_entry.delete(0, tk.END)  # Limpa o conteúdo atual
        self.data_entry.insert(0, data_atual)  # Insere a nova data

    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.inicio1_entry.delete(0, END)
        self.parada1_entry.delete(0, END)
        self.inicio2_entry.delete(0, END)
        self.parada2_entry.delete(0, END)

    def onDoubleClick(self, event):
        # teve que passar o parametro event porque
        # há interação com essa def e ai se vc nao colocar ela nao roda
        self.limpar_tela()
        self.listaCliente.selection()

        for n in self.listaCliente.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.listaCliente.item(
                n, 'values')
            self.codigo_entry.insert(END, col1)
            self.data_entry.insert(END, col2)
            self.inicio1_entry.insert(END, col3)
            self.parada1_entry.insert(END, col4)
            self.inicio2_entry.insert(END, col5)
            self.parada2_entry.insert(END, col6)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(
            """ DELETE FROM horas WHERE cod = ? """, (self.cod,))
        # passa essa virgula no final do execute para dizer que é uma tupla
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE horas SET data = ?,
        inicio = ?, paradaalm = ?, retornoalm = ?, saida = ?
        WHERE cod = ? """, (self.data, self.inicio, self.paradaalm, self.retornoalm, self.saida, self.cod))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def atualiza_horas(self):
        self.variaveis()
        if self.data_entry.get() == "":
            msg = "Todos os campos precisam estar preenchidos!"
            messagebox.showinfo("Preencha os campos", msg)
        elif self.inicio1_entry.get() == "":
            msg = "Todos os campos precisam estar preenchidos!"
            messagebox.showinfo("Preencha os campos", msg)
        elif self.parada1_entry.get() == "":
            msg = "Todos os campos precisam estar preenchidos!"
            messagebox.showinfo("Preencha os campos", msg)
        elif self.inicio2_entry.get() == "":
            msg = "Todos os campos precisam estar preenchidos!"
            messagebox.showinfo("Preencha os campos", msg)
        elif self.parada2_entry.get() == "":
            msg = "Todos os campos precisam estar preenchidos!"
            messagebox.showinfo("Preencha os campos", msg)
        else:
            self.conecta_bd()

        # Garante que tenha 6 dígitos (com zeros à esquerda se necessário)

        a1 = datetime.strptime(self.inicio, "%H:%M:%S")
        a2 = datetime.strptime(self.paradaalm, "%H:%M:%S")
        total_manha = a2 - a1
        a3 = datetime.strptime(self.retornoalm, "%H:%M:%S")
        a4 = datetime.strptime(self.saida, "%H:%M:%S")
        total_tarde = a4 - a3
        total_horas_dia = total_manha + total_tarde

        self.cursor.execute(""" UPDATE horas SET data = ?, inicio = ?, paradaalm = ?, retornoalm = ?, saida = ?, totalhoras = ?
        WHERE cod = ? """, (self.data, self.inicio, self.paradaalm, self.retornoalm, self.saida, str(total_horas_dia), self.cod))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()


class Application(Validadores, Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.validaEntradas()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menu()
        root.mainloop()

    def tela(self):
        self.root.title(
            '                                                                                                                Cadastro de Horas - R & R Prisma')
        self.root.configure(background='#062530')
        self.root.geometry("900x700")  # Horizontal x Vertical
        self.root.resizable(False, False)

    def frames_da_tela(self):
        # os locais aonde vao aparecer os botoes e as exibições(2 retangulos na tela)
        # bd BORDA, bg COR FUNDO, highlightbackground CorDaBorda, highlightthickness TAMANHO BORDA
        self.frame_1 = Frame(self.root, bd=1, bg='#d1e8f0',
                             highlightbackground='#113642',
                             highlightthickness='3')
        # POSICIONAR O FRAME relxy 0 seria 0% e 1 seria 100%, esquerda para direita, cima para baixo
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        # bd BORDA, bg COR FUNDO, highlightbackground CorDaBorda, highlightthickness TAMANHO BORDA
        self.frame_2 = Frame(self.root, bd=1, bg='#5093ab',
                             highlightbackground='#113642',
                             highlightthickness='3')
        # POSICIONAR O FRAME relxy 0 seria 0% e 1 seria 100%, esquerda para direita, cima para baixo
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.48)

        # Criação e posição da label no frame 1 e entrada do CÓDIGO no frame 1
        self.lb_codigo = Label(text="Código", background='#d1e8f0')

        self.codigo_entry = Entry(validate='key', validatecommand=self.vcmd2)

        # Criação da label e entrada do NOME no frame 1
        self.data_entry = Entry(justify="center")
        self.data_entry.place(relx=0.38, rely=0.22, relwidth=0.1)

        self.lb_inicio1 = Label(text="Início do Dia", background="#d1e8f0")
        self.lb_inicio1.place(relx=0.23, rely=0.27)

        self.inicio1_entry = Entry()
        self.inicio1_entry.place(relx=0.24, rely=0.3, relwidth=0.1)
        # Criação da label e entrada do TELEFONER no frame 1
        self.lb_parada1 = Label(
            text="Parada para Almoço", background="#d1e8f0")
        self.lb_parada1.place(relx=0.53, rely=0.27)

        self.parada1_entry = Entry()
        self.parada1_entry.place(relx=0.54, rely=0.3, relwidth=0.1)
        # Criação da label e entrada do CIDADE no frame 1
        self.lb_inicio2 = Label(text="Volta do Almoço", background="#d1e8f0")
        self.lb_inicio2.place(relx=0.23, rely=0.37)

        self.inicio2_entry = Entry()
        self.inicio2_entry.place(relx=0.24, rely=0.4, relwidth=0.1)

        self.lb_parada2 = Label(text="Finaliza o Dia", background="#d1e8f0")
        self.lb_parada2.place(relx=0.53, rely=0.37)

        self.parada2_entry = Entry()
        self.parada2_entry.place(relx=0.54, rely=0.4, relwidth=0.1)

    def widgets_frame1(self):
        # Criação do Botão
        self.bt_atualizarData = Button(root, text="Data",
                                       command=self.atualizar_data)
        self.bt_atualizarData.place(relx=0.41, rely=0.17,
                                    relwidth=0.037, relheight=0.037)
        self.bt_atualizar1 = Button(root, text="Add",
                                    command=self.atualizar_horario1)
        self.bt_atualizar1.place(relx=0.19, rely=0.29,
                                 relwidth=0.037, relheight=0.037)
        self.bt_atualizar2 = Button(root, text="Add",
                                    command=self.atualizar_horario2)
        self.bt_atualizar2.place(relx=0.49, rely=0.29,
                                 relwidth=0.037, relheight=0.037)
        self.bt_atualizar3 = Button(root, text="Add",
                                    command=self.atualizar_horario3)
        self.bt_atualizar3.place(relx=0.19, rely=0.39,
                                 relwidth=0.037, relheight=0.037)
        self.bt_atualizar4 = Button(root, text="Add",
                                    command=self.atualizar_horario4)
        self.bt_atualizar4.place(relx=0.49, rely=0.39,
                                 relwidth=0.037, relheight=0.037)

        # botao Atualizar
        self.bt_atualizar = Button(text='Atualizar', bd=3,
                                   bg='white', fg='black', font=('', 9, 'bold'), command=self.atualiza_horas)
        self.bt_atualizar.place(relx=0.683, rely=0.025,
                                relwidth=0.07, relheight=0.07)

        # botao Limpar
        self.bt_limpar = Button(text='Limpar', bd=3,
                                bg='white', fg='black', font=('', 9, 'bold'), command=self.limpar_tela)
        self.bt_limpar.place(relx=0.613, rely=0.025,
                             relwidth=0.07, relheight=0.07)
        # Botão Buscar
        self.bt_buscar = Button(text='Buscar', bd=3,
                                bg='white', fg='black', font=('', 9, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.541, rely=0.025,
                             relwidth=0.07, relheight=0.07)
        # Botão Novo
        # cria uma variavel para receber a imagem que vem do codigo da
        # funçao def imagens_base64

        self.bt_dataatual = Button(text='Salvar', bd=3,
                                   bg='white', fg='black', font=('', 9, 'bold'), command=self.add_cliente)
        self.bt_dataatual.place(relx=0.325, rely=0.025,
                                relwidth=0.07, relheight=0.07)
        # Botão Alterar
        self.bt_alterar = Button(text='Editar', bd=3,
                                 bg='white', fg='black', font=('', 9, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.397, rely=0.025,
                              relwidth=0.07, relheight=0.07)
        # Botão Apagarr
        self.bt_apagar = Button(text='Excluir', bd=3,
                                bg='white', fg='black', font=('', 9, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.469, rely=0.025,
                             relwidth=0.07, relheight=0.07)

    def lista_frame2(self):
        self.listaCliente = ttk.Treeview(self.frame_2, height=3, columns=(
            # cria a lista no frame 2 e coloca os nomes
            'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'))
        self.listaCliente.heading("#0", text="")
        self.listaCliente.heading("#1", text="Cod")
        self.listaCliente.heading('#2', text='Data')
        self.listaCliente.heading('#3', text='Entrada')
        self.listaCliente.heading('#4', text='Parada Alm.')
        self.listaCliente.heading('#5', text='Retorno Alm.')
        self.listaCliente.heading('#6', text='Saida')
        self.listaCliente.heading('#7', text='Total Horas')

        # define o tamanho de cada parte da lista
        self.listaCliente.column('#0', width=10)
        self.listaCliente.column('#1', width=10)
        self.listaCliente.column('#2', width=100)
        self.listaCliente.column('#3', width=100)
        self.listaCliente.column('#4', width=100)
        self.listaCliente.column('#5', width=100)
        self.listaCliente.column('#6', width=100)
        self.listaCliente.column('#7', width=100)

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
        menubar.add_cascade(label='Relatorio',
                            command=self.gerar_relatorio_pdf)
        # comand é pra ir adicioanndo as opções dentro do menu
        filemenu1.add_command(label="Sair", command=Quit)

    def validaEntradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry4), '%P')


Application()

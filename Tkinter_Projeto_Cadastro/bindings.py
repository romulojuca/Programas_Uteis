from tkinter import *
from tkinter import ttk

root = Tk()

l = ttk.Label(root, text='Começando...')
l.grid()

l.bind('<Enter>', lambda e: l.configure(text='movido o mouse para dentro'))
l.bind('<Leave>', lambda e: l.configure(text='movido o mouse para fora'))
l.bind('<1>', lambda e: l.configure(text='clicou botao esquerdo'))
l.bind('<Double-1>', lambda e: l.configure(text='clique duplo'))
l.bind('<B3-Motion>',
       lambda e: l.configure(text="Arrastou c direito na posição %d, %d" % (e.x, e.y)))

root.mainloop()

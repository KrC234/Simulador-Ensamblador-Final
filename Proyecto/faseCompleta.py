import tkinter as tk
from tkinter import filedialog, messagebox, END
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview


class ventana(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master, width=1150, height=600)
        self.master = master
        self.pack()
        self.pack_propagate(False)
        self.create_widgets()
        self.filepath = ""
        # Paginación para el panel txtArchivo
        self.page_txtArchivo = 0
        self.items_por_page_txtArchivo = 20
        self.lineas_archivo = []  # Inicializar como lista vacía
        #AJUSTAR LAS COLUMNAS
        self.master.bind("<Configure>", self.ajustar_columnas)
        
    def create_widgets(self):
        #BARRA DE MENUS
        barra_menus = tk.Menu(self.master, tearoff=0)
        self.master.config(menu=barra_menus)
        
        archivo_menu = tk.Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Opciones", menu=archivo_menu)
        self.icn1 = tk.PhotoImage(file="asm.png")
        archivo_menu.add_command(label="Archivo", command=self.abrirArchivo, image=self.icn1, compound="left")
        self.icn2 = tk.PhotoImage(file="cerrar-sesion.png")
        archivo_menu.add_command(label="Salir", command=self.master.quit, image=self.icn2, compound="left")
        
        self.menu_bar_frame = tk.Frame(self, bg='#2D5336')
        self.menu_bar_frame.pack(side=tk.TOP, fill=tk.X)
        self.menu_bar_frame.pack_propagate(False)
        self.menu_bar_frame.config(height=30)
        
        # Botones estilizados
        button_style = {
            "bg": "#EEDEAB",        # Color de fondo
            "fg": "#383838",       # Color del texto
            "font": ("Arial", 9, "normal"),  # Fuente
            "activebackground": "#F9F4E3",  # Color de fondo al pasar el ratón
            "activeforeground": "#2D5336",  # Color del texto al pasar el ratón
            #"bd": 3,             # Grosor del borde
            "relief": "flat",  # Estilo del borde
            "cursor": "hand2"    # Cursor tipo mano
        }
        
        button_style1 = {
            "bg": "#336633",        # Color de fondo
            "fg": "white",       # Color del texto
            "font": ("Arial", 9, "bold"),  # Fuente
            "activebackground": "#F9F4E3",  # Color de fondo al pasar el ratón
            "activeforeground": "#2D5336",  # Color del texto al pasar el ratón
            #"bd": 3,             # Grosor del borde
            "relief": "flat",  # Estilo del borde
            "cursor": "hand2"    # Cursor tipo mano
        }
        
        # Botones en la barra superior
        btn_frame1 = tk.Button(self.menu_bar_frame, text="Fase 1", command=self.show_frame1, **button_style)
        btn_frame1.pack(side=tk.LEFT, padx=10, pady=5)
        
        btn_frame2 = tk.Button(self.menu_bar_frame, text="Fase 2", command=self.show_frame2, **button_style)
        btn_frame2.pack(side=tk.LEFT, padx=10, pady=5)
        
        # CONTENEDORES PARA LOS FRAMES DINÁMICOS
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Frame 1
        self.frame1 = tk.Frame(self.container, bg="#7C7731")
        self.frame1.place(relwidth=1, relheight=1)  # Ocupa todo el espacio del contenedor
        
        
        # Frame 2
        self.frame2 = tk.Frame(self.container, bg="#7C7731")
        self.frame2.place(relwidth=1, relheight=1)  # Ocupa todo el espacio del contenedor
        
        
        # Mostrar inicialmente Frame 1
        self.show_frame1()
        
        #TODOS LOS ELEMETOS DE LA FASE 1
        
        #TEXT de archivos
        self.lblArchivo = tk.Label(self.frame1, text="ARCHIVO", font=("Times New Roman",16), bg=self.frame1.cget("bg"), fg="white")
        self.lblArchivo.place(x=105, y=30, width=150, height=30)
        
        self.txtArchivo = tk.Text(self.frame1, wrap=tk.WORD, font=("Times New Roman", 10), state="disabled")
        self.txtArchivo.config(bg="#EFDFAC")
        self.txtArchivo.place(x=30, y=70, height=400, width=300)
        
        #BOTONES PRINCIPALES
        self.smb = tk.Button(self.frame1, text="Separar", **button_style1)
        self.smb.place(x=390, y=70, width=100, height=30)
        
        self.slr = tk.Button(self.frame1, text="Simbolo", **button_style1)
        self.slr.place(x=390, y=120, width=100, height=30)
        
        #PAGINACION IZQUIERDA Y DERECHA DE ARCHIVO
        self.imgPagI = tk.PhotoImage(file="flecha-izquierda.png")
        self.imgPagD = tk.PhotoImage(file="flecha-derecha.png")
        
        
        self.pagIzq = tk.Button(self.frame1, image=self.imgPagI)
        self.pagIzq.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagIzq.place(x=87, y=490, width=64, height=64)
        
        self.pagDer = tk.Button(self.frame1, image=self.imgPagD)
        self.pagDer.config(
            activebackground="#7C7731", 
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagDer.place(x=209, y=490, width=64, height=64)
        
        #ELEMENTO-SIMBOLO
        self.txtSimobolo = tk.Text(self.frame1, state="disabled")
        self.txtSimobolo.config(
            font=("Times New Roman",15),
            bg="#EFDFAC"
        )
        self.txtSimobolo.place(x=550, y=70, width=200, height=400)
        
        #ELEMENTO-TIPO
        self.txtTipo = tk.Text(self.frame1, state="disabled")
        self.txtTipo.config(
            font=("Times New Roman",15),
            bg="#EFDFAC"
        )
        self.txtTipo.place(x=800, y=70, width=300, height=400)
        
        #PAGINACION IZQUIERDA Y DERECHA DE TIPO Y SIMBOLO
        self.pagIzqS = tk.Button(self.frame1, image=self.imgPagI)
        self.pagIzqS.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagIzqS.place(x=720, y=490, width=64, height=64)
        
        self.pagDerS = tk.Button(self.frame1, image=self.imgPagD)
        self.pagDerS.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagDerS.place(x=880, y=490, width=64, height=64)   
        
        #TODOS LOS ELEMENTOS DE LA FASE 2    
        #TEXT de archivos
        self.txtArchivo2 = tk.Text(self.frame2, wrap=tk.WORD, font=("Times New Roman", 10), state="disabled")
        self.txtArchivo2.config(bg="#EFDFAC")
        self.txtArchivo2.place(x=30, y=20, height=400, width=300)
        
        self.pagIzq = tk.Button(self.frame1, image=self.imgPagI)
        self.pagIzq.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagIzq.place(x=87, y=490, width=64, height=64)
        
        self.pagDer = tk.Button(self.frame1, image=self.imgPagD)
        self.pagDer.config(
            activebackground="#7C7731", 
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagDer.place(x=209, y=490, width=64, height=64)
        
        #BOTONES PRINCIPALES
        self.smb2 = tk.Button(self.frame2, text="simbolos", **button_style1)
        self.smb2.place(x=355, y=20, width=100, height=30)
        
        #ELEMENTO Y ERROR
        self.txtElemento = tk.Text(self.frame2, state="disabled")
        self.txtElemento.config(font=("Times New Roman",10), bg="#EFDFAC")
        self.txtElemento.place(x=480, y=20, width=300, height=200)
        
        self.txtErrores = tk.Text(self.frame2, state="disabled")
        self.txtErrores.config(font=("Times New Roman",10), bg="#EFDFAC")
        self.txtErrores.place(x=825, y=20, width=300, height=200)
        
        self.pagIzq2 = tk.Button(self.frame2, image=self.imgPagI)
        self.pagIzq2.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagIzq2.place(x=87, y=460, width=64, height=64)
        
        self.pagDer2 = tk.Button(self.frame2, image=self.imgPagD)
        self.pagDer2.config(
            activebackground="#7C7731", 
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagDer2.place(x=209, y=460, width=64, height=64)
        
        # Crear el Treeview para la tabla
        self.tabla = Treeview(self.frame2, columns=("Columna1", "Columna2", "Columna3", "Columna4", "Columna5"), show="headings")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.place(x=480, y=230, width=645, height=230)
        
        # Configurar encabezados
        self.tabla.heading("Columna1", text="Nombre")
        self.tabla.heading("Columna2", text="Tipo")
        self.tabla.heading("Columna3", text="Valor")
        self.tabla.heading("Columna4", text="Tamaño(Bytes)")
        self.tabla.heading("Columna5", text="Direccion")
        
        #PAGINACION IZQUIERDA Y DERECHA DE TIPO Y SIMBOLO
        self.pagIzqS2 = tk.Button(self.frame2, image=self.imgPagI)
        self.pagIzqS2.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagIzqS2.place(x=720, y=490, width=64, height=64)
        
        self.pagDerS2 = tk.Button(self.frame2, image=self.imgPagD)
        self.pagDerS2.config(
            activebackground="#7C7731", 
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat",
            bg=self.frame1.cget("bg")
        )
        self.pagDerS2.place(x=880, y=490, width=64, height=64)   
        
        
    def show_frame1(self):
        self.frame1.tkraise()  # Lleva el Frame 1 al frente
    
    def show_frame2(self):
        self.frame2.tkraise()  # Lleva el Frame 2 al frente
        
    def abrirArchivo(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Archivos ENS", "*.ens"), ("Archvos TXT", ".*txt"), ("Otro", "*?")], title=("Explorador de archivos"))
        if self.filepath:
            if self.filepath.lower().endswith(".ens"):
                with open(self.filepath, 'r') as archivo:
                    self.lineas_archivo = archivo.readlines()
                    self.page_txtArchivo = 0
                    self.mostrar_contenido_txtArchivo()
            else:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo con extensión .ens")
    
    def ajustar_columnas(self, event=None):
        ancho_total = self.tabla.winfo_width()
        num_columnas = len(self.tabla["columns"])
        ancho_columna = ancho_total // num_columnas
        for col in self.tabla["columns"]:
            self.tabla.column(col, width=ancho_columna)

    def mostrar_contenido_txtArchivo(self):
        start_line = self.page_txtArchivo * self.items_por_page_txtArchivo
        end_line = start_line + self.items_por_page_txtArchivo

        self.txtArchivo.config(state="normal")
        self.txtArchivo.delete("1.0", END)
        self.txtArchivo2.config(state="normal")
        self.txtArchivo2.delete("1.0", END)

        contenido_pagina = self.lineas_archivo[start_line:end_line]
        
        self.txtArchivo.insert(END, ''.join(contenido_pagina))
        self.txtArchivo.config(state="disabled")
        
        self.txtArchivo2.insert(END, ''.join(contenido_pagina))
        self.txtArchivo2.config(state="disabled")
        
        self.pagIzq.config(command=self.paginar_izquierda)
        self.pagDer.config(command=self.paginar_derecha)
        self.pagIzq2.config(command=self.paginar_izquierda)
        self.pagDer2.config(command=self.paginar_derecha)
    
    def paginar_izquierda(self):
        if self.page_txtArchivo > 0:
            self.page_txtArchivo -= 1
            self.mostrar_contenido_txtArchivo()

    def paginar_derecha(self):
        if (self.page_txtArchivo + 1) * self.items_por_page_txtArchivo < len(self.lineas_archivo):
            self.page_txtArchivo += 1
            self.mostrar_contenido_txtArchivo()
    
    
vent = tk.Tk()
app = ventana(vent)
vent.title("PROYECTO FINAL DE ENSAMBLADOR")
app.mainloop()
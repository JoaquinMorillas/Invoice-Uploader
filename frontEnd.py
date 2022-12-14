from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
import tkinter.font as tkFont

from backEnd import cargarDatos, consulta, borrarDatosTree, borrarDato

class Window(Frame):
    
    def __init__(self, root, width, height ):
        super().__init__()
        self.root = root
        self.width = width
        self.height = height
        self.root.title("Calculadora de Facturación")
        self.root.geometry(f"{self.height}x{self.width}")
        self.calc_frame= Frame(self.root,relief="raised", borderwidth=5 )
        self.tree_frame=Frame(self.calc_frame)
        self.sumaFrame = Frame(self.root,relief="raised", borderwidth=5 )

        helv20 = tkFont.Font(family='Helvetica', size=15)

        self.agentes = ["Amedey", "Casanova", "Strumia"]
        self.agente_facturacion = StringVar()
        self.agente_facturacion.set(self.agentes[0])
        self.agente_consulta = StringVar()
        self.agente_consulta.set(self.agentes[0])
        self.dias = [x for x in range(1,32)]
        self.dia = IntVar()
        self.dia.set(self.dias[0])
        self.meses = [x for x in range(1,13)]
        self.mes= IntVar()
        self.desdeMes = IntVar()
        self.hastaMes = IntVar()
        self.mes.set(self.meses[0])
        self.desdeMes.set(self.meses[0])
        self.hastaMes.set(self.meses[0])
        self.años = [x for x in range(2015, 2041)]
        self.año = IntVar()
        self.hastaAño = IntVar()
        self.desdeAño = IntVar()
        self.año.set(self.años[7])
        self.desdeAño.set(self.años[7])
        self.hastaAño.set(self.años[7])
        self.monto = DoubleVar()

        columns=["Id de Factura","Fecha", "Monto"]
        self.treeview = ttk.Treeview(self.tree_frame, columns=columns, show="headings",selectmode="browse")
        self.treeview.heading("Id de Factura", text="Id de Factura")
        self.treeview.column("Id de Factura", stretch=NO, minwidth=0, width=0)
        self.treeview.heading("Fecha", text="Fecha (YYYY-MM-DD)")
        self.treeview.column("Fecha", anchor=CENTER)
        self.treeview.heading("Monto", text="Monto")
        self.treeview.column("Monto", anchor=CENTER)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand = self.scrollbar.set)
        self.calc_frame.grid(row=0, column=1)
        self.inputs_frame = self.inputsFrame()
        self.views = self.views()

        self.tree_frame.grid(row=1, column=1)

        self.sumaFrame.grid(row=2, column=1, pady=10)
        self.treeview.pack(side= LEFT, fill= BOTH)
        self.scrollbar.pack(side= RIGHT, fill= BOTH)
        

        self.suma_de_montos = DoubleVar()
        
        self.suma_de_montos_label = Label(self.sumaFrame, textvariable=self.suma_de_montos, font= helv20)
        self.suma_de_montos_label.grid(row=0, column=1)
        self.label = Label(self.sumaFrame, text="Suma de montos = ", font= helv20).grid(row=0,column=0)
    

    def inputsFrame(self):
        inputs_frame = Frame(self.root, padx= 10, 
            height = self.height,
             relief="groove", borderwidth=5)

        inputs_frame.grid(row=0, column=0,sticky = N, padx = 5)
        
        helv20 = tkFont.Font(family='Helvetica', size=15)

        drop = OptionMenu(inputs_frame , self.agente_facturacion , *self.agentes)
        drop.config(font=helv20)
        drop.grid(row=1, column=1,pady=10)

        facturador_label = Label(inputs_frame, 
	    	text = "Nombre del Facturador: ", font=helv20)
        facturador_label.grid(row=1, column=0,pady=10)
	    
        datos_label = Label(inputs_frame, 
	    	text="Datos de la Factura:", font= helv20)
        datos_label.grid(row=2, column=0,pady=10)

        dia_label = Label(inputs_frame, text= "Dia:", font= helv20)
        dia_label.grid(row=3, column=0,pady=10)
        dia_drop = OptionMenu(inputs_frame , self.dia , *self.dias)
        dia_drop.config(font=helv20)
        dia_drop.grid(row=3, column=1,pady=10)

        mes_label = Label(inputs_frame, text= "Mes:", font= helv20)
        mes_label.grid(row=4, column=0,pady=10)
        mes_drop = OptionMenu(inputs_frame , self.mes , *self.meses)
        mes_drop.config(font=helv20)
        mes_drop.grid(row=4, column=1,pady=10)

        año_label = Label(inputs_frame, text= "Año:", font= helv20)
        año_label.grid(row=5, column=0,pady=10)
        año_drop = OptionMenu(inputs_frame , self.año , *self.años)
        año_drop.config(font=helv20)
        año_drop.grid(row=5, column=1,pady=10)

        monto_label = Label(inputs_frame, text= "Monto:", 
	    	font= helv20)
        monto_label.grid(row=6, column=0,pady=10)
        monto_entry = Entry(inputs_frame, textvariable= self.monto, 
	    	font=helv20)
        monto_entry.grid(row=6, column=1,pady=10)

        cargar_button= Button(inputs_frame, text= "Cargar Factura", command= lambda: cargarDatos(self),
	   	font= helv20)
        cargar_button.grid(row=7, column=1,pady=10)	


    def views(self):
        helv20 = tkFont.Font(family='Helvetica', size=15)
        views_frame = Frame(self.calc_frame, padx= 10,
         height = self.height//2, width= self.width//2, 
         relief="groove", borderwidth=5 )
        views_frame.grid(row=0, column=1)

        drop = OptionMenu(views_frame , self.agente_consulta , *self.agentes)
        drop.config(font=helv20)
        drop.grid(row=1, column=1)

        facturador_label = Label(views_frame, 
	    	text = "Nombre del Facturador: ", font=helv20)
        facturador_label.grid(row=1, column=0)

        desde_label = Label(views_frame, text= "Desde: ",font=helv20)
        desde_label.grid(row=2, column=0)
        mes_label = Label(views_frame, text= "Mes: ",font=helv20)
        mes_label.grid(row=2, column=1)
        desde_mes = OptionMenu(views_frame , self.desdeMes , *self.meses)
        desde_mes.config(font=helv20)
        desde_mes.grid(row=2, column=2)
        año_label = Label(views_frame, text= "Año: ",font=helv20)
        año_label.grid(row=2, column=3)

        desde_año = OptionMenu(views_frame , self.desdeAño , *self.años)
        desde_año.config(font=helv20)
        desde_año.grid(row=2, column=4)

        hasta_label = Label(views_frame, text= "Hasta: ",font=helv20)
        hasta_label.grid(row=3, column=0)
        mes_label = Label(views_frame, text= "Mes: ",font=helv20)
        mes_label.grid(row=3, column=1)
        hasta_mes = OptionMenu(views_frame , self.hastaMes , *self.meses)
        hasta_mes.config(font=helv20)
        hasta_mes.grid(row=3, column=2)
        año_label = Label(views_frame, text= "Año: ",font=helv20)
        año_label.grid(row=3, column=3)

        hasta_año = OptionMenu(views_frame , self.hastaAño , *self.años)
        hasta_año.config(font=helv20)
        hasta_año.grid(row=3, column=4)

        consulta_button = Button(views_frame, text= "Consultar",font= helv20, command= lambda: consulta(self))
        consulta_button.grid(row=4, column=0)

        borrar_button = Button(views_frame, text= "Limpiar Tabla", font= helv20, command= lambda: borrarDatosTree(self))
        borrar_button.grid(row=4, column= 1)

        borrar_dato = Button(views_frame, text= "Borrar factura seleccionada", font= helv20, command= lambda: borrarDato(self))
        borrar_dato.grid(row=4, column=2, columnspan=3,padx = 15)
        
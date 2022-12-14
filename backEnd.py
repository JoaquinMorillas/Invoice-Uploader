import sqlite3
from datetime import date
from tkinter import *
from tkinter import messagebox as msg
def cargarDatos(win):
	try:
		monto = win.monto.get()
		if monto <= 0:
			msg.showerror("Monto no Valido", "Solo se pueden poner numero mayores a 0 en el monto")
			return
	except TclError:
		msg.showerror("Monto no Valido", "Solo se pueden poner numero mayores a 0 en el monto")
		return
	res = msg.askquestion('Cargar Factura', f'¿Queres cargar la factura por monto $ {win.monto.get()} con fecha {win.dia.get()}-{win.mes.get()}-{win.año.get()}?')
	if res == 'yes':
		agente = win.agente_facturacion.get()
		
		
		dia = win.dia.get()
		mes = win.mes.get()
		año = win.año.get()
		try:
			fecha = date(año,mes,dia)
		except ValueError:
			msg.showerror("Fecha no Valida", f"El mes {mes}, no contiene {dia} dias")
			return
		conn = sqlite3.connect("facturacion.db")
		curr = conn.cursor()

		curr.execute(f"INSERT into {agente} (fecha, monto) VALUES (?,?)", (fecha, monto))

		conn.commit()
		conn.close()

def consulta(win):
	borrarDatosTree(win)
	agente = win.agente_consulta.get()
	mes_inicial= win.desdeMes.get()
	mes_inicial_str= str(mes_inicial)
	if len(mes_inicial_str) == 1:
		mes_inicial_str = f"0{mes_inicial}"
	año_inicial = win.desdeAño.get()
	mes_final = win.hastaMes.get()
	mes_final_str= str(mes_final)
	if len(mes_final_str) == 1:
		mes_final_str = f"0{mes_final}"
	año_final = win.hastaAño.get()

	conn = sqlite3.connect("facturacion.db")
	curr = conn.cursor()

	curr.execute(f"""
	SELECT id_factura, fecha, monto
	FROM {agente}
	
	WHERE fecha BETWEEN DATE('{año_inicial}-{mes_inicial_str}-01') AND 
	DATE('{año_final}-{mes_final_str}-01','+1 month','-1 day')
	ORDER BY fecha DESC""")
	

	data = curr.fetchall()
	montos = []
	for row in data:
		win.treeview.insert("", END, values=row)
		montos.append(row[-1])
	conn.close()
	suma_de_montos = sum(montos)
	win.suma_de_montos.set(suma_de_montos)


def borrarDatosTree(win):
	items = win.treeview.get_children()
	for item in items:
		win.treeview.delete(item)
	win.suma_de_montos.set(0.0)

def borrarDato(win):

	item = win.treeview.focus()
	selected = win.treeview.item(item)
	id_to_delete = selected["values"][0]
	fecha_to_delete = selected["values"][1]
	monto_to_delete = selected["values"][2]
	agente = win.agente_consulta.get()
	
	res = msg.askquestion('Borrar Factura', f'¿Queres borrar la factura de {agente} por monto $ {monto_to_delete} con fecha {fecha_to_delete}?')
	if res == 'yes':
	
		conn = sqlite3.connect("facturacion.db")
		curr = conn.cursor()

		curr.execute(f"""
		DELETE FROM {agente} 
		WHERE id_factura = {id_to_delete}""")

		conn.commit()
		conn.close()

		borrarDatosTree(win)
		consulta(win)
	

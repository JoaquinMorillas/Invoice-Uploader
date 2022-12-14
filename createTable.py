import sqlite3

conn = sqlite3.connect("facturacion.db")

curr = conn.cursor()

curr.execute("CREATE TABLE Amedey (id_factura INTEGER PRIMARY KEY AUTOINCREMENT, Fecha TEXT, Monto REAL)")
curr.execute("CREATE TABLE Casanova (id_factura INTEGER PRIMARY KEY AUTOINCREMENT, Fecha TEXT, Monto REAL)")
curr.execute("CREATE TABLE Strumia (id_factura INTEGER PRIMARY KEY AUTOINCREMENT, Fecha TEXT, Monto REAL)")

conn.commit


from tkinter import ttk
from tkinter import *

import sqlite3

class Producto:

    db_name= 'database.db'

    def __init__(self, ventana):
        self.vent = ventana
        self.vent.title("Productos")
        
        #creando un contenedor
        cuadro = LabelFrame(self.vent, text= 'Registra un nuevo producto')
        cuadro.grid(row=0, column=0, columnspan=3, pady=20)
        
        #nombre input
        Label(cuadro, text='Nombre: ').grid(row=1, column=0)
        self.nombre = Entry(cuadro)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        
        #precio input
        Label(cuadro, text='Precio: ').grid(row=2, column=0)
        self.precio = Entry(cuadro)
        self.precio.grid(row=2, column=1)
        
        #boton agregar
        ttk.Button(cuadro, text='agregar', command=self.add_product).grid(row=3, columnspan=2, sticky=W+E)

        #area de mensajes
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W+E)
        
        #tabla
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor= CENTER)
        self.tree.heading('#1', text='Precio', anchor= CENTER)

        #botones del y edit
        ttk.Button(text='Eliminar', command=self.del_product).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text='Editar', command=self.edit_product).grid(row=5, column=1, sticky=W+E)

        #llenando las columnas
        self.get_product()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parameters)
            conn.commit()
        return resultado

    def get_product(self):
        #limpiando la tabla
        records = self.tree.get_children()
        for elemento in records:
            self.tree.delete(elemento)
        #consultando data    
        query  = 'SELECT * from producto ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def validation(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get())

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get())
            self.run_query(query, parametros)
            self.mensaje['text'] = 'Base de datos actualizada'
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.mensaje['text'] = 'campos requeridos'
        self.get_product()

    def del_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor seleccione un elemento'
            return
        self.mensaje['text'] = ''
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.run_query(query, (nombre,))
        self.mensaje['text'] = 'Base de datos actualizada'
        self.get_product()

    def edit_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor seleccione un elemento'
            return
        self.mensaje['text'] = ''
        nombre = self.tree.item(self.tree.selection())['text']
        precio_ant = self.tree.item(self.tree.selection())['values'][0]
        self.edit_ventana = Toplevel()
        self.edit_ventana.title = 'Editar'

        #nombre anterior
        Label(self.edit_ventana, text='Nombre original: ').grid(row=0, column=1)
        Entry(self.edit_ventana, textvariable=StringVar(self.edit_ventana, value=nombre), state='readonly').grid(row=0, column=2)
        
        #nombre nuevo
        Label(self.edit_ventana, text='Nuevo: ').grid(row=1, column=1)
        nombre_actual = Entry(self.edit_ventana)
        nombre_actual.grid(row=1, column=2)

        #precio anterior
        Label(self.edit_ventana, text='Precio original: ').grid(row=2, column=1)
        Entry(self.edit_ventana, textvariable=StringVar(self.edit_ventana, value=precio_ant), state='readonly').grid(row=2, column=2)

        #precio nuevo
        Label(self.edit_ventana, text='Nuevo: ').grid(row=3, column=1)
        precio_actual = Entry(self.edit_ventana)
        precio_actual.grid(row=3, column=2)

        Button(self.edit_ventana, text='Actualizar', command=lambda: self.update_product(nombre_actual.get(), nombre, precio_actual.get(), precio_ant)).grid(row=4, column=2, sticky=W)

    def update_product(self, nombre_actual, nombre, precio_actual, precio):
        query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parametros = (nombre_actual, precio_actual, nombre, precio)
        self.run_query(query, parametros)
        self.edit_ventana.destroy()
        self.mensaje['text'] = 'Base de datos actualizada'
        self.get_product()


if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Producto(ventana)
    ventana.mainloop()

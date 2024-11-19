# cursos_view.py
import tkinter as tk
from tkinter import ttk, messagebox

from centrar_ventana import centrar

class cursos_view():
    def __init__(self, container) -> None:
        '''Constructor de la clase'''
        self.container = container

        self.frame2 = ttk.Frame(self.container, border=1)
        self.frame2.grid(padx=5, pady=5, row=1, column=0, sticky='nsew')

        #Aplicamos estilos y los modificamos para la cabecera del treeview.
        self.style = ttk.Style(self.container)
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", background='grey', foreground='white')

        # Define el Nombre y el ancho en píxeles de las columnas.
        columns = {'Id': 50, 'Nombre': 300, 'Nivel': 80, 'Carrera_id': 80, 'Carrera': 150}

        self.treeview = ttk.Treeview(self.frame2, columns=tuple(columns.keys()), show='headings', height=14, selectmode='browse')

        # Define las cabeceras
        for clave, valor in columns.items():
            self.treeview.heading(clave, text=clave)
            self.treeview.column(clave, width=valor)


        self.treeview.grid(row=0, column=0, sticky='nsew')

        #Añade un barra lateral de scroll (enrollado).
        scrollbar = ttk.Scrollbar(self.frame2, orient=tk.VERTICAL, command=self.treeview.yview)
        #self.treeview.configure(yscroll=scrollbar.set)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.frame3 = ttk.Frame(self.container, border=0)
        self.frame3.grid(padx=5, pady=5, row=2, column=0, sticky='nsesw')

        self.buttonAdd = ttk.Button(self.frame3, text='Añadir')
        self.buttonAdd.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.buttonUpdate = ttk.Button(self.frame3, text='Actualizar')
        self.buttonUpdate.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.buttonRemove = ttk.Button(self.frame3, text='Eliminar')
        self.buttonRemove.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.buttonExit = ttk.Button(self.frame3, text='Salir')
        self.buttonExit.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    def getCursorId(self) -> int:
        '''getCursorId obtiene el valor de Id del cursor.

        Returns:
            str: devuelve el valor de Id del cursor.
        '''
        selectedLbData = self.treeview.selection()[0]
        Id = self.treeview.item(selectedLbData)['values'][0]
        return int(Id)

    def getCursorNombre(self) -> str:
        '''getCursorNombre obtiene el valor de Nombre del cursor.

        Returns:
            str: devuelve el valor de Nombre del cursor.
        '''
        selectedLbData = self.treeview.selection()[0]
        nombre = self.treeview.item(selectedLbData)['values'][1]
        return nombre

    def getCursorNivel(self) -> int:
        selectedLbData = self.treeview.selection()[0]
        nivel = self.treeview.item(selectedLbData)['values'][2]
        return int(nivel)

    def getCursorCarreras_id(self) -> int:
        selectedLbData = self.treeview.selection()[0]
        Carreras_id = self.treeview.item(selectedLbData)['values'][3]
        return int(Carreras_id)

    def getCursorCarreras_nombre(self) -> str:
        selectedLbData = self.treeview.selection()[0]
        Carreras_nombre = self.treeview.item(selectedLbData)['values'][4]
        '''Preselecciona el nombre de la carrera en el combobox'''
        return Carreras_nombre

    def setTreeview(self, data: list):
        '''setTreeview pones datos en el treeview

        Args:
            data (list): recibe datos como lista.
        '''
        #Sale si no trae datos y evita la asignación de datos vacios.
        if not data: return

        #Elimina los datos anteriores.
        self.treeview.delete(*self.treeview.get_children())
        #Asigna los datos del data.
        for row in data:
            #Inserta una row en el treeview.
            self.treeview.insert('', tk.END, text=row[0], values=row)

    def showMessageBox(self, message: str, title: str, type: str):
        '''showMessageBox muestra un mensaje en una ventana emergente.

        Args:
            message (str): mensaje a mostrar.
            title (str): Nombre de la ventana.
            type (str): tipo de ventana.
        '''
        if type == 'info':
            messagebox.showinfo(title, message)
        elif type == 'warning':
            messagebox.showwarning(title, message)
        elif type == 'error':
            messagebox.showerror(title, message)

class modalWindow:
    def __init__(self, parent, titulo_ventana: str = '', datos: tuple = (), carreras: list = []) -> None:
        self.parent = parent
        self.carreras = carreras

        self.modal = tk.Toplevel(self.parent)
        self.modal.geometry(centrar(alto=200, ancho=420, app=self.parent))
        self.modal.title(titulo_ventana)

        # Fija el redimensionamiento de la ventana
        self.modal.resizable(False, False)
        # Hacer que la ventana modal sea transitoria y modal
        self.modal.transient(parent)
        # Bloquea el enfoque en la ventana modal
        self.modal.grab_set()

        self.frame1 = ttk.Frame(self.modal, border=2, relief='groove')
        self.frame1.grid(padx=10, pady=10, row=0, column=0, sticky='nsew')

        self.labelId = ttk.Label(self.frame1, text='Id: ')
        self.labelId.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.intvarId = tk.IntVar()
        self.entryId = ttk.Entry(self.frame1, textvariable=self.intvarId, state='disabled')
        self.entryId.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.labelNombre = ttk.Label(self.frame1, text='Nombre: ')
        self.labelNombre.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.textvarNombre = tk.StringVar()
        self.entryNombre = ttk.Entry(self.frame1, textvariable=self.textvarNombre, width=50)
        self.entryNombre.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.labelNivel = ttk.Label(self.frame1, text='Nivel: ')
        self.labelNivel.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.intvarNivel = tk.IntVar()
        self.entryNivel = ttk.Entry(self.frame1, textvariable=self.intvarNivel, width=50)
        self.entryNivel.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.labelCarreras = ttk.Label(self.frame1, text='Carreras: ')
        self.labelCarreras.grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.intvarCarreras_id = tk.IntVar()
        self.textvarCarreras_nombre = tk.StringVar()
        self.comboboxCarreras = ttk.Combobox(self.frame1, textvariable=self.textvarCarreras_nombre, width=50, state='readonly')
        self.comboboxCarreras['values'] = [x[1] for x in carreras]
        self.comboboxCarreras.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.frame2 = tk.Frame(self.modal)
        self.frame2.grid(padx=5, pady=5, row=2, column=0, sticky='nsesw')

        self.aceptarButton = tk.Button(self.frame2, text="Aceptar", command=lambda: self.close_modal(True))
        #self.aceptarButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.aceptarButton.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.cancelarButton = tk.Button(self.frame2, text="Cancelar", command=lambda: self.close_modal(False))
        #self.cancelarButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='e')
        self.cancelarButton.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)

        # Si vienen datos en la tupla se copian en los StingVar del formulario.
        # Da Falso cuando datos es None.
        if datos:
            self.setId(datos[0])
            self.setNombre(datos[1])
            self.setNivel(datos[2])
            self.setCarreras_id(datos[3])
            self.setCarreras_nombre(datos[4])

        # Establece el enfoque en la ventana modal.
        self.modal.focus_set()
        # Establecer el enfoque en el botón de cierre.
        self.entryNombre.focus_set()
        self.modal.wait_window(self.modal)

    def close_modal(self, buttonClicked = False) -> None:
        # DeCarreras_ide la propiedad buttonCliked para guardar el boton pulsado.
        self.buttonClicked = buttonClicked
        # Liberar el bloqueo del enfoque
        self.modal.grab_release()
        # Eliminación completa del widget
        self.modal.destroy()

    def getId(self) -> int:
        '''getId Obtiene el valor de intvarId

        Returns:
            str: retorna el valor de intvarId
        '''
        return self.intvarId.get()

    def setId(self, Id: int) -> None:
        '''setId establece el valor de intvarId.

        Args:
            id (str): valor de intvarId.
        '''
        self.intvarId.set(Id)

    def getNombre(self) -> str:
        return self.textvarNombre.get()

    def setNombre(self, nombre: str) -> None:
        self.textvarNombre.set(nombre)

    def getNivel(self) -> int:
        return self.intvarNivel.get()

    def setNivel(self, nivel: int) -> None:
        self.intvarNivel.set(nivel)

    def getCarreras_id(self) -> int:
        for x in self.carreras:
            if x[1] == self.textvarCarreras_nombre.get():
                return x[0]

    def setCarreras_id(self, Carreras_id: int) -> None:
        self.intvarCarreras_id.set(Carreras_id)

    def getCarreras_nombre(self) -> str:
        return self.textvarCarreras_nombre.get()

    def setCarreras_nombre(self, Carreras_nombre: str) -> None:
        self.textvarCarreras_nombre.set(Carreras_nombre)





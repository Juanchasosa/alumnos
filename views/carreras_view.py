# carreras_views.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from tkcalendar import DateEntry

from centrar_ventana import centrar

class carreras_view():
    def __init__(self, container) -> None:
        '''Constructor de la clase'''
        self.container = container

        self.frame2 = ttk.Frame(self.container, border=1)
        self.frame2.grid(padx=0, pady=0, row=1, column=0, sticky='nsew')

        #Aplicamos estilos y los modificamos para la cabecera del treeview.
        self.style = ttk.Style(self.container)
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", background='grey', foreground='white')

        #Define el Nombre y el ancho en píxeles de las columnas.
        columns = {'Id': 50, 'Nombre': 300, 'Inicio': 80, 'Fin': 80, 'Duración': 60}
        self.treeview = ttk.Treeview(self.frame2, columns=tuple(columns.keys()), show='headings', height=14, selectmode='browse')
        #Define las cabeceras
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
        selectedLbData = self.treeview.selection()[0]
        Id = self.treeview.item(selectedLbData)['values'][0]
        return int(Id)

    def getCursorNombre(self) -> str:
        '''getCursorNombre obtiene el valor de Nombre del cursor.

        Returns:
            str: devuelve el valor de Nombre del cursor.
        '''
        selectedLbData = self.treeview.selection()[0]
        Nombre = self.treeview.item(selectedLbData)['values'][1]
        return Nombre

    def getCursorInicio(self) -> date:
        selectedLbData = self.treeview.selection()[0]
        inicio = self.treeview.item(selectedLbData)['values'][2]
        return datetime.strptime(inicio, '%d-%m-%Y')

    def getCursorFin(self) -> date:
        selectedLbData = self.treeview.selection()[0]
        fin = self.treeview.item(selectedLbData)['values'][3]
        return datetime.strptime(fin, '%d-%m-%Y')

    def getCursorDuracion(self):
        selectedLbData = self.treeview.selection()[0]
        duracion = self.treeview.item(selectedLbData)['values'][4]
        return int(duracion)

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
            # Inserta una row en el treeview.
            inicio_fmt = datetime.strptime(row[2], '%Y-%m-%d').strftime('%d-%m-%Y')
            fin_fmt = datetime.strptime(row[3], '%Y-%m-%d').strftime('%d-%m-%Y')
            self.treeview.insert('', tk.END, text=row[0], values=(row[0], row[1], inicio_fmt, fin_fmt, row[4]))
            #self.treeview.insert('', tk.END, text=row[0], values=row)

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
    def __init__(self, parent, titulo_ventana: str = '', datos: tuple = ()) -> None:
        self.parent = parent

        self.modal = tk.Toplevel(self.parent)
        self.modal.geometry(centrar(alto=230, ancho=410, app=self.parent))
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

        self.labelInicio = ttk.Label(self.frame1, text='Inicio: ')
        self.labelInicio.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        hoy = datetime.now().strftime('%d-%m-%Y')
        self.textvarInicio = tk.StringVar(value=hoy)
        self.dateEntryInicio = DateEntry(self.frame1, width=12,  background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy', state='readonly')
        self.dateEntryInicio.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.labelFin = ttk.Label(self.frame1, text='Fin: ')
        self.labelFin.grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.textvarFin = tk.StringVar()
        self.dateEntryFin = DateEntry(self.frame1, width=12,  background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy', state='readonly')
        self.dateEntryFin.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.labelDuracion = ttk.Label(self.frame1, text='Duración: ')
        self.labelDuracion.grid(row=4, column=0, padx=5, pady=5, sticky='e')

        self.intvarDuracion = tk.IntVar()
        self.entryDuracion = ttk.Entry(self.frame1, textvariable=self.intvarDuracion)
        self.entryDuracion.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        self.frame2 = tk.Frame(self.modal)
        self.frame2.grid(padx=5, pady=5, row=2, column=0, sticky='nsesw')

        self.aceptarButton = tk.Button(self.frame2, text="Aceptar", command=lambda: self.close_modal(True))
        #self.aceptarButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.aceptarButton.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.cancelarButton = tk.Button(self.frame2, text="Cancelar", command=lambda: self.close_modal(False))
        #self.cancelarButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='e')
        self.cancelarButton.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)

        self.dateEntryInicio.bind("<<DateEntrySelected>>", self.actualizar_textvarInicio)
        self.dateEntryFin.bind("<<DateEntrySelected>>", self.actualizar_textvarFin)
    # Vincular el evento <<DateEntrySelected>> con la función de actualización

        # Si vienen datos en la tupla se copian en los StingVar del formulario.
        # Da Falso cuando datos es None.
        if datos:
            self.setId(datos[0])
            self.setNombre(datos[1])
            self.setInicio(datos[2])
            self.setFin(datos[3])
            self.setDuracion(datos[4])

            self.dateEntryInicio.set_date(datos[2])
            self.dateEntryFin.set_date(datos[3])


        # Establece el enfoque en la ventana modal.
        self.modal.focus_set()
        # Establecer el enfoque en el botón de cierre.
        self.entryNombre.focus_set()
        self.modal.wait_window(self.modal)

    # Función que actualiza el StringVar con la fecha seleccionada
    def actualizar_textvarInicio(self, event):
        fecha_seleccionada = self.dateEntryInicio.get()  # Obtener la fecha seleccionada como texto
        self.textvarInicio.set(fecha_seleccionada)  # Actualizar el StringVar con la fecha seleccionada

    def actualizar_textvarFin(self, event):
        fecha_seleccionada = self.dateEntryFin.get()  # Obtener la fecha seleccionada como texto
        self.textvarFin.set(fecha_seleccionada)  # Actualizar el StringVar con la fecha seleccionada

    def close_modal(self, buttonClicked=False) -> None:
        # Define la propiedad buttonCliked para guardar el boton pulsado.
        self.buttonClicked = buttonClicked
        # Liberar el bloqueo del enfoque
        self.modal.grab_release()
        # Eliminación completa del widget
        self.modal.destroy()

    def getId(self) -> int:
        '''getId Obtiene el valor de textvarId

        Returns:
            str: retorna el valor de textvarId
        '''
        return self.intvarId.get()

    def setId(self, Id: int) -> None:
        self.intvarId.set(Id)

    def getNombre(self) -> str:
        return self.textvarNombre.get()

    def setNombre(self, Nombre: str) -> None:
        self.textvarNombre.set(Nombre)

    def getInicio(self) -> date:
        return datetime.strptime(self.textvarInicio.get(), '%d-%m-%Y')

    def setInicio(self, inicio: date) -> None:
        self.textvarInicio.set(inicio.strftime('%d-%m-%Y'))

    def getFin(self) -> date:
        return datetime.strptime(self.textvarFin.get(), '%d-%m-%Y')

    def setFin(self, Fin: date) -> None:
        self.textvarFin.set(Fin.strftime('%d-%m-%Y'))

    def getDuracion(self) -> int:
        return self.intvarDuracion.get()

    def setDuracion(self, year: int) -> None:
        self.intvarDuracion.set(year)

'''
alumnos_views.py: Es la vista de alumnos.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from centrar_ventana import centrar

class alumnos_view():
    def __init__(self, container) -> None:
        '''Constructor de la clase'''
        self.container = container

        self.frame2 = ttk.Frame(self.container, border=1)
        self.frame2.grid(padx=5, pady=5, row=1, column=0, sticky='nsew')

        #Aplicamos estilos y los modificamos para la cabecera del treeview.
        self.style = ttk.Style(self.container)
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", background='grey', foreground='white')

        #Definimos el Nombre y el ancho en píxeles de las columnas.
        columns = {'Id': 50, 'Apellido': 200, 'Nombre': 200, 'Inscripción': 100, 'Cursos_id': 50, 'Curso': 150, 'Carrera_id': 50, 'Carrera': 200}
        self.treeview = ttk.Treeview(self.frame2, columns=tuple(columns.keys()), show='headings', height=14, selectmode='browse')

        #Definimos las cabeceras
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

    def getCursorApellido(self) -> str:
        '''getCursorNombre obtiene el valor de Nombre del cursor.

        Returns:
            str: devuelve el valor de Nombre del cursor.
        '''
        selectedLbData = self.treeview.selection()[0]
        apellido = self.treeview.item(selectedLbData)['values'][1]
        return apellido

    def getCursorNombre(self) -> str:
        selectedLbData = self.treeview.selection()[0]
        nombre = self.treeview.item(selectedLbData)['values'][2]
        return nombre

    def getCursorInscripcion(self) -> datetime:
        selectedLbData = self.treeview.selection()[0]
        inscripcion = self.treeview.item(selectedLbData)['values'][3]
        return datetime.strptime(inscripcion, '%d-%m-%Y %H:%M')

    def getCursorCursos_id(self):
        selectedLbData = self.treeview.selection()[0]
        cursos_id = self.treeview.item(selectedLbData)['values'][4]
        return int(cursos_id)

    def getCursorCursos_nombre(self) -> str:
        selectLbData = self.treeview.selection()[0]
        cursos_nombre = self.treeview.item(selectLbData)['values'][5]
        return cursos_nombre


    def setTreeview(self, data: list):
        '''setTreeview pones datos en el treeview
        Args:
            data (list): recibe datos como lista.
        '''
        #Sale si no trae datos y evita la asignación de datos vacios.
        if not data:
            return

        #Elimina los datos anteriores.
        self.treeview.delete(*self.treeview.get_children())
        #Asigna los datos del data.
        for row in data:
            #Inserta una row en el treeview.
            fecha_fmt = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M')
            self.treeview.insert('', tk.END, text=row[0], values=(row[0], row[1], row[2], fecha_fmt, row[4], row[5], row[6], row[7]))
            # self.treeview.insert('', tk.END, text=row[0], values=row)

class modalWindow:
    def __init__(self, parent, titulo_ventana: str = "", datos: tuple = (), cursos:list = []) -> None:
        self.parent = parent
        self.cursos = cursos
        self.buttonClicked = False

        self.modal = tk.Toplevel(self.parent)
        self.modal.geometry(centrar(alto=230, ancho=420, app=self.parent))
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

        self.labelApellido = ttk.Label(self.frame1, text='Apellido: ')
        self.labelApellido.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.textvarApellido = tk.StringVar()
        self.entryApellido = ttk.Entry(self.frame1, textvariable=self.textvarApellido, validate='key', width=50)
        self.entryApellido['validatecommand']=(self.entryApellido.register(self.validateApellido), '%S')
        self.entryApellido.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.labelNombre = ttk.Label(self.frame1, text='Nombre: ')
        self.labelNombre.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.textvarNombre = tk.StringVar()
        self.entryNombre = ttk.Entry(self.frame1, textvariable=self.textvarNombre, width=50)
        self.entryNombre.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.labelInscripcion = ttk.Label(self.frame1, text='Inscripcion: ')
        self.labelInscripcion.grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.textvarInscripcion = tk.StringVar()
        self.entryInscripcion = ttk.Entry(self.frame1, textvariable=self.textvarInscripcion, width=50, state='readonly')
        self.entryInscripcion.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.labelCursos_id = ttk.Label(self.frame1, text='Cursos_id: ')
        self.labelCursos_id.grid(row=4, column=0, padx=5, pady=5, sticky='e')

        self.intvarCursos_id = tk.IntVar()
        self.textvarCursos_nombre = tk.StringVar()
        self.comboboxCursos = ttk.Combobox(self.frame1, textvariable=self.textvarCursos_nombre, width=50, state='readonly')
        self.comboboxCursos['values'] = [x[1] for x in cursos]
        self.comboboxCursos.grid(row=4, column=1, padx=5, pady=5, sticky='w')


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
            self.setApellido(datos[1])
            self.setNombre(datos[2])
            self.setInscripcion(datos[3])
            self.setCursos_id(datos[4])
            self.setCursos_nombre(datos[5])
        else:
            fechaActual = datetime.now()
            self.setInscripcion(fechaActual)

        # Establece el enfoque en la ventana modal.
        self.modal.focus_set()
        # Establecer el enfoque en el botón de cierre.
        self.entryApellido.focus_set()
        self.modal.wait_window(self.modal)

    def validateApellido(self, new_text: str) -> bool:
        if not new_text.isalpha() and not new_text.isspace():
            return False
    # Función para validar solo letras
    def validar_solo_letras(self, texto):
        return texto.isalpha() or texto == ''  # Solo permite letras o vacío (para borrar)

    # Función para validar solo números
    def validar_solo_numeros(self, texto):
        return texto.isdigit() or texto == ''  # Solo permite números o vacío
        return True

    def close_modal(self, buttonClicked: bool) -> bool:
        # Según sea el bottón, la función es la misma para aceptar y cancelar, pero aceptar es true.
        if buttonClicked:
            # Valida que el apellido no esté vacío.
            if self.textvarApellido == '':
                showMessageBox('El campo del evento no puede estar vacío.', 'Error', 'error' )
                return False

            # Valida que el nombre no esté vacío.

            # Valida la fecha de inscripción que tenga un formato definido en getInscription().
            try:
                self.getInscripcion()
            except ValueError as e:
                showMessageBox(f'Fecha de inicio no válida:\n{e}', 'Error', 'error')
                return False

            # Validamos cursos_id, hay que ver si existe en la tabla cursos o mejor obtenrlo de un combo con los currosos válidos.

            # Otras validaciones.

        # Define la propiedad buttonCliked para guardar el boton pulsado.
        self.buttonClicked = buttonClicked
        # Liberar el bloqueo del enfoque
        self.modal.grab_release()
        # Eliminación completa del widget
        self.modal.destroy()

        return buttonClicked

    def getId(self) -> int:
        '''getId Obtiene el valor de textvarId

        Returns:
            str: retorna el valor de textvarId
        '''
        return self.intvarId.get()

    def setId(self, Id: int) -> None:
        '''setId establece el valor de textvarId.

        Args:
            id (str): valor de textvarId.
        '''
        self.intvarId.set(Id)

    def getApellido(self) -> str:
        return self.textvarApellido.get()

    def setApellido(self, Apellido: str) -> None:
        self.textvarApellido.set(Apellido)

    def getNombre(self) -> str:
        return self.textvarNombre.get()

    def setNombre(self, Nombre: str) -> None:
        self.textvarNombre.set(Nombre)

    def getInscripcion(self) -> datetime:
        return datetime.strptime(self.textvarInscripcion.get(), '%d-%m-%Y %H:%M')

    def setInscripcion(self, Inscripcion: datetime) -> None:
        self.textvarInscripcion.set(Inscripcion.strftime('%d-%m-%Y %H:%M'))

    # def getCursos_id(self) -> int:
    #     return self.intvarCursos_id.get()

    # def setCursos_id(self, cursos_id: int) -> None:
    #     self.intvarCursos_id.set(cursos_id)

    def getCursos_id(self) -> int:
        for x in self.cursos:
            if x[1] == self.textvarCursos_nombre.get():
                return x[0]

    def setCursos_id(self, Cursos_id: int) -> None:
        self.intvarCursos_id.set(Cursos_id)


    def getCursos_nombre(self) -> str:
        return self.textvarCursos_nombre.get()

    def setCursos_nombre(self, Cursos_nombre: str) -> None:
        self.textvarCursos_nombre.set(Cursos_nombre)



def showMessageBox(message: str, title: str, type_window: str):
    '''showMessageBox muestra un mensaje en una ventana emergente.

    Args:
        message (str): mensaje a mostrar.
        title (str): Nombre de la ventana.
        type (str): tipo de ventana.
    '''
    if type_window == 'info':
        messagebox.showinfo(title, message)
    elif type_window == 'warning':
        messagebox.showwarning(title, message)
    elif type_window == 'error':
        messagebox.showerror(title, message)

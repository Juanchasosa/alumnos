'''
alumnos_controler.py: Es el controlador de Alumnos.
'''
from datetime import datetime

from views.alumnos_view import alumnos_view, modalWindow, showMessageBox
from models.alumnos_model import alumnos_model

class alumnos_controler():
    '''alumnos_controller se encarga de manejar la vista y el modelo.
    '''
    def __init__(self, root: object) -> None:
        self.root = root

        # Instancia el modelo.
        self.model = alumnos_model()
        # Crea  un istancia la vista.
        self.view = alumnos_view(self.root)
        # Añade la función addToTreeview al botón de agregar.
        self.view.buttonAdd["command"] = self.addToTreeview
        # Añade la función removeFromTreeview al botón de eliminar.
        self.view.buttonUpdate["command"] = self.updateFromTreeview
        # Añade la función updateFromTreeview al botón de actualizar.
        self.view.buttonRemove["command"] = self.removeFromTreeview
        # Añade la función loadTreeviewToEntry al evento de selección de fila.
        self.view.buttonExit["command"] = self.__del__

        # Añade la función loadTreeviewToEntry al evento de selección de fila.
        #self.view.treeview.bind('<<TreeviewSelect>>', self.loadTreeviewToEntry)
        # Carga los datos de la base de datos al treeview.
        self.loadToTreeview()
        self.loadCursosToCombobox()

        # Anotación de tipo, self.modal debe ser del tipo modalWindows.
        self.modal : modalWindow

        self.id : int
        self.apellido : str
        self.nombre : str
        self.inscripcion : datetime
        self.cursos_id : int
        self.cursos_nombre : str

    def loadToTreeview(self):
        '''loadToTreeview Carga los datos de la base de datos al treeview.
        '''
        data = self.model.getAllData()
        print(data)
        self.view.setTreeview(data)

    def addToTreeview(self):
        '''addToTreeview Agrega un registro a la base de datos y al treeview.'''
        # Crea una instancia de la ventana modal, observar que aquí no se llama loadTreeviewToEntry porque es un alta.
        self.modal = modalWindow(self.root, 'Alta de Alumno', (), self.loadCursosToCombobox())
        #Solo si hay un registro seleccionado el el treeview.
        if self.modal.buttonClicked:
            if self.modal.textvarApellido.get() != '' and \
                self.modal.textvarNombre.get() != '' and \
                self.modal.textvarInscripcion.get() != '' and \
                self.modal.textvarCursos_nombre.get() != '' :

                self.addToDB()
                self.loadToTreeview()
                self.clearForm()
            else:
                showMessageBox(message='Debe llenar todos los campos.', title='Error', type_window='error')

    def removeFromTreeview(self):
        '''removeFromTreeview Elimina un registro de la base de datos y del treeview.'''
        # Crea una instancia de la ventana modal
        self.modal = modalWindow(self.root, 'Bajas de Alumnos', self.loadTreeviewToEntry(), self.loadCursosToCombobox())

        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            if self.modal.buttonClicked:
                self.removeFromDB()
                self.loadToTreeview()
                self.clearForm()

    def updateFromTreeview(self):
        '''updateFromTreeview Actualiza un registro de la base de datos y del treeview.'''
        # Crea una instancia de la ventana modal
        self.modal = modalWindow(self.root, 'Modificación de Alumno', self.loadTreeviewToEntry(), self.loadCursosToCombobox())

        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            if self.modal.buttonClicked:
                self.updateDB()
                self.loadToTreeview()
                self.clearForm()

    def loadTreeviewToEntry(self):
        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            self.id = self.view.getCursorId()
            self.apellido = self.view.getCursorApellido()
            self.nombre = self.view.getCursorNombre()
            self.inscripcion = self.view.getCursorInscripcion()
            self.cursos_id = self.view.getCursorCursos_id()
            self.cursos_nombre = self.view.getCursorCursos_nombre()

            return (self.id,
                    self.apellido,
                    self.nombre,
                    self.inscripcion,
                    self.cursos_id,
                    self.cursos_nombre)
        else:
            return ()

    def loadCursosToCombobox(self) -> list:
        '''Carga la lista de cursos disponibles para el combobox

        Returns:
            list: Lista de tuplas (id, nombre) de los cursos
        '''
        return self.model.getAllCursos()

    def addToDB(self):
        self.apellido = self.modal.getApellido()
        self.nombre = self.modal.getNombre()
        self.inscripcion = self.modal.getInscripcion()
        self.cursos_id = self.modal.getCursos_id()
        self.model.create(self.apellido, self.nombre, self.inscripcion, self.cursos_id)

    def updateDB(self):
        self.id = self.modal.getId()
        self.apellido = self.modal.getApellido()
        self.nombre = self.modal.getNombre()
        self.inscripcion = self.modal.getInscripcion()
        self.cursos_id = self.modal.getCursos_id()
        self.model.update(self.id, self.apellido, self.nombre, self.inscripcion, self.cursos_id)

    def removeFromDB(self):
        self.id = self.view.getCursorId()
        self.model.delete(self.id)

    def clearForm(self):
        self.modal.setId(0)
        self.modal.setApellido('')
        self.modal.setNombre('')
        self.modal.setInscripcion(datetime.now())
        self.modal.setCursos_id(0)

        #Deselecciona fila de treeview.
        self.view.treeview.selection_remove(self.view.treeview.selection())

        return

    def __del__(self) -> None:
        self.view.frame2.destroy()
        self.view.frame3.destroy()

        del self

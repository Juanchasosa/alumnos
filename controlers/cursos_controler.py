'''
cursos_controler.py: Contiene el controlador de cursos.
'''
from views.cursos_view import cursos_view, modalWindow
from models.cursos_model import cursos_model

class cursos_controler():
    '''Nombres_controller se encarga de manejar la vista y el modelo.
    '''
    def __init__(self, root: object) -> None:
        self.root = root
        # Instancia el modelo.
        self.model = cursos_model()
        # Crea  un istancia la vista.
        self.view = cursos_view(self.root)
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

        # Crea una instancia de la ventana modal
        self.modal: modalWindow

        self.id : int
        self.nombre : str
        self.nivel : int
        self.carreras_id : int
        self.carreras_nombre : str

    def loadToTreeview(self):
        '''loadToTreeview Carga los datos de la base de datos al treeview.
        '''
        data = self.model.getAllData()
        self.view.setTreeview(data)

    def addToTreeview(self):
        '''addToTreeview Agrega un registro a la base de datos y al treeview.'''
        # Crea una instancia de la ventana modal, observar que aquí no se llama loadTreeviewToEntry porque es un alta.
        self.modal = modalWindow(self.root, 'Alta de Curso', (), self.loadCarrerasToCombobox())

        #Solo si hay un registro seleccionado el el treeview.
        if self.modal.buttonClicked:
                if self.modal.textvarNombre.get() != '' and \
                    self.modal.intvarNivel.get() != 0 and \
                    self.modal.textvarCarreras_nombre.get() != '' :

                    self.addToDB()
                    self.loadToTreeview()
                    self.clearForm()
        else:
            self.view.showMessageBox(message='Debe llenar todos los campos.', title='Error', type='error')

    def removeFromTreeview(self):
        '''removeFromTreeview Elimina un registro de la base de datos y del treeview.'''

        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            # Crea una instancia de la ventana modal
            self.modal = modalWindow(self.root, 'Bajas de Curso', self.loadTreeviewToEntry(), self.loadCarrerasToCombobox())
            if self.modal.buttonClicked:
                self.removeFromDB()
                self.loadToTreeview()
                self.clearForm()
        else:
        # Mostrar advertencia si no se seleccionó ningún curso
            self.view.showMessageBox(
            message="Debe seleccionar un curso para eliminar.",
            title="Advertencia",
            type="warning"
            )

    def updateFromTreeview(self):
        '''updateFromTreeview Actualiza un registro de la base de datos y del treeview.'''
        # Crea una instancia de la ventana modal
        self.modal = modalWindow(self.root, 'Modificación de Curso', self.loadTreeviewToEntry(), self.loadCarrerasToCombobox())

        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            if self.modal.buttonClicked:
                self.updateDB()
                self.loadToTreeview()
                self.clearForm()

    def loadTreeviewToEntry(self) -> tuple:
        #Solo si hay un registro seleccionado en el treeview.
        if self.view.treeview.selection():
            self.id = self.view.getCursorId()
            self.nombre = self.view.getCursorNombre()
            self.nivel = self.view.getCursorNivel()
            self.carreras_id = self.view.getCursorCarreras_id()
            self.carreras_nombre = self.view.getCursorCarreras_nombre()

            return (self.id,
                        self.nombre,
                        self.nivel,
                        self.carreras_id,
                        self.carreras_nombre)
        else:
            return ()

    def loadCarrerasToCombobox(self) -> list:
        return self.model.getAllCarreras()


    def addToDB(self):
        nombre = self.modal.getNombre()
        nivel = self.modal.getNivel()
        carreras_id = self.modal.getCarreras_id()

        self.model.create(nombre, nivel, carreras_id)

    def updateDB(self):
        Id = self.view.getCursorId()
        nombre = self.modal.getNombre()
        nivel = self.modal.getNivel()
        carreras_id = self.modal.getCarreras_id()
        self.model.update(Id, nombre, nivel, carreras_id)

    def removeFromDB(self):
        Id = self.view.getCursorId()
        resultado = self.model.delete(Id)
        # Retornar el mensaje del modelo
        if "eliminada correctamente" in resultado:
            self.view.showMessageBox(message=resultado, title="Éxito", type="info")
        else:
            self.view.showMessageBox(message=resultado, title="Error", type="error")

    def clearForm(self):
        self.modal.setId(0)
        self.modal.setNombre('')
        self.modal.setNivel(0)
        self.modal.setCarreras_id(0)

        #Deselecciona fila de treeview.
        self.view.treeview.selection_remove(self.view.treeview.selection())

        return

    def __del__(self) -> None:
        self.view.frame2.destroy()
        self.view.frame3.destroy()

        del self

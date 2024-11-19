'''
carreras_controler.py: Contiene el controlador de Carreras.
'''
from datetime import date, datetime

from views.carreras_view import carreras_view, modalWindow
from models.carreras_model import carreras_model

class carreras_controler():
    '''Nombres_controller se encarga de manejar la vista y el modelo.
    '''
    def __init__(self, root: object) -> None:
        self.root = root
        # Instancia el modelo.
        self.model = carreras_model()
        # Crea  un istancia la vista.
        self.view = carreras_view(self.root)
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

        # Anotación de tipo, self.modal debe ser del tipo modalWindows.
        self.modal : modalWindow

        self.Id : int
        self.nombre : str
        self.inicio : date
        self.fin : date
        self.duracion : int

    def loadToTreeview(self):
        '''loadToTreeview Carga los datos de la base de datos al treeview.
        '''
        data = self.model.getAllData()
        self.view.setTreeview(data)

    def addToTreeview(self):
        '''addToTreeview Agrega un registro a la base de datos y al treeview.'''
        self.modal = modalWindow(self.root, 'Alta de Carrera')

        #Solo si hay un registro seleccionado el el treeview.
        if self.modal.buttonClicked:
            if self.modal.textvarNombre.get() != '' and \
                self.modal.textvarInicio.get() != '' and \
                self.modal.textvarFin.get() != '' and \
                self.modal.intvarDuracion.get() != 0 :

                self.addToDB()
                self.loadToTreeview()
                self.clearForm()
            else:
                self.view.showMessageBox(message='Debe llenar todos los campos.', title='Error', type='error')

    def removeFromTreeview(self):
        '''removeFromTreeview Elimina un registro de la base de datos y del treeview.'''
        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            self.modal = modalWindow(self.root, 'Baja de Carrera', self.loadTreeviewToEntry())

            if self.modal.buttonClicked:
                self.removeFromDB()
                self.loadToTreeview()
                self.clearForm()
        else:
        # Mostrar advertencia si no se seleccionó ninguna carrera
            self.view.showMessageBox(
            message="Debe seleccionar una carrera para eliminar.",
            title="Advertencia",
            type="warning"
            )

    def updateFromTreeview(self):
        '''updateFromTreeview Actualiza un registro de la base de datos y del treeview.'''
        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            self.modal = modalWindow(self.root, 'Modificación de Carrera', self.loadTreeviewToEntry())

            if self.modal.buttonClicked:
                self.updateDB()
                self.loadToTreeview()
                self.clearForm()

    def loadTreeviewToEntry(self) -> tuple:
        #Solo si hay un registro seleccionado el el treeview.
        if self.view.treeview.selection():
            self.Id = self.view.getCursorId()
            self.nombre = self.view.getCursorNombre()
            self.inicio = self.view.getCursorInicio()
            self.fin = self.view.getCursorFin()
            self.duracion = self.view.getCursorDuracion()

            # Retorna datos solo si se ha seleccionado una fila del Treeview.
            return (self.Id,
                    self.nombre,
                    self.inicio,
                    self.fin,
                    self.duracion)
        else:
            return ()

    def addToDB(self):
        self.nombre = self.modal.getNombre()
        self.inicio = self.modal.getInicio()
        self.fin = self.modal.getFin()
        self.duracion = self.modal.getDuracion()

        self.model.create(self.nombre, self.inicio, self.fin, self.duracion)

    def updateDB(self):
        self.Id = self.modal.getId()
        self.nombre = self.modal.getNombre()
        self.inicio = self.modal.getInicio()
        self.fin = self.modal.getFin()
        self.duracion = self.modal.getDuracion()
        self.model.update(self.Id, self.nombre, self.inicio, self.fin, self.duracion)

    def removeFromDB(self):
        self.Id = self.view.getCursorId()
        resultado = self.model.delete(self.Id)
        # Retornar el mensaje del modelo
        if "eliminada correctamente" in resultado:
            self.view.showMessageBox(message=resultado, title="Éxito", type="info")
        else:
            self.view.showMessageBox(message=resultado, title="Error", type="error")

    def clearForm(self):
        self.modal.setId(0)
        self.modal.setNombre('')
        self.modal.setInicio(datetime.now())
        self.modal.setFin(datetime.now())
        self.modal.setDuracion(0)

        #Deselecciona fila de treeview.
        self.view.treeview.selection_remove(self.view.treeview.selection())

        return

    def __del__(self) -> None:
        self.view.frame2.destroy()
        self.view.frame3.destroy()

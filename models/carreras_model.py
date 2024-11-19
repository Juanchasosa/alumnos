#carreras_models.py
from datetime import date

from database import dbConn

class carreras_model():
    '''carrerasModel Modelo de la tabla carreras.
    '''
    def __init__(self) -> None:
        '''__init__ Constructor de la clase, establece la conexión a la base
        de datos e intenta crear la tabla si no existe..
        '''
        self.nombre : str
        self.inicio : str
        self.fin : str
        self.duracion : int

        #Abre la conexión con la base de datos alumnos y si no existe la crea.
        self.conn = dbConn.dbConn('database\\alumnos.sqlite3')
        #Crea la tabla carreras si no existe.
        tableName = 'carreras'
        fieldsDescripcion = '('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'nombre TEXT NOT NULL UNIQUE, '\
            'inicio DATE NOT NULL, '\
            'fin DATE NOT NULL, '\
            'duracion INTEGER NOT NULL)'
        #Ejecuta el comando en la base de datos.
        self.conn.createTable(tableName=tableName, fieldsDescripcion=fieldsDescripcion)

    def create(self, nombre: str, inicio: date, fin: date, duracion: int) -> list:
        command = 'INSERT INTO carreras (nombre, inicio, fin, duracion) VALUES (?, date(?), date(?), ?)'
        values = (nombre, inicio, fin, duracion)
        return self.conn.execute(command, values)

    def read(self, Id: int) -> list:
        '''read Lee un registro de la base de datos.

        Args:
            id (int): Id del registro a leer.

        Returns:
            list: Retorna el registro leído.
        '''
        command = 'SELECT * FROM carreras WHERE Id = ?'
        values = (Id,)
        return self.conn.execute(command, values)

    def update(self, Id: int, nombre: str, inicio: date, fin: date, duracion: int) -> list:
        command = "UPDATE carreras SET nombre = ?, inicio = date(?), fin = date(?), duracion = ? WHERE Id = ?"
        values = (nombre, inicio, fin, duracion, Id)
        return self.conn.execute(command, values)

    def delete(self, Id: int) -> list:
        '''delete Borra un registro de la base de datos.

        Args:
            id (str): Id del registro a borrar.

        Returns:
            list: Devuelve el registro borrado.
        '''
        # Verificar si hay cursos asociados a la carrera
        CheckearCursos = 'SELECT COUNT(*) FROM cursos WHERE carreras_id = ?'
        cursos_count = self.conn.execute(CheckearCursos, (Id,))[0][0]
        if cursos_count > 0:
            return "No se puede eliminar la carrera porque tiene cursos asociados."

        # Verificar si hay alumnos asociados a la carrera a través de los cursos
        CheckearAlumnos = '''
            SELECT COUNT(*)
            FROM alumnos a
            INNER JOIN cursos c ON a.cursos_id = c.id
            WHERE c.carreras_id = ?
        '''
        alumnos_count = self.conn.execute(CheckearAlumnos, (Id,))[0][0]
        if alumnos_count > 0:
            return "No se puede eliminar la carrera porque tiene alumnos asociados."

        # Si no hay dependencias, proceder con la eliminación
        command = 'DELETE FROM carreras WHERE Id = ?'
        values = (Id,)
        self.conn.execute(command, values)
        return "Carrera eliminada correctamente."

    def getAllData(self) -> list:
        '''getAllData Recupera todos los registros de la base de datos.

        Returns:
            list: devuelve una lista de carreras.
        '''
        command = 'SELECT * FROM carreras'
        return self.conn.execute(command)

    def __del__(self) -> None:
        '''__del__ Destructor de la clase.'''
        del self.conn
        del self

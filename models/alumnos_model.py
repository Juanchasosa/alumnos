'''
alumnos_model.py: Es el model de alumnos.
'''
from datetime import date, datetime

from database import dbConn

class alumnos_model():
    '''alumnosModel Modelo de la tabla alumnos.
    '''
    def __init__(self) -> None:
        '''__init__ Constructor de la clase, establece la conexión a la base
        de datos e intenta crear la tabla si no existe..
        '''
        self.Id : int
        self.apellido : str
        self.nombre : str
        self.inscripcion : date
        self.cursos_id : int

        #Abre la conexión con la base de datos alumnos y si no existe la crea.
        self.conn = dbConn.dbConn('database\\alumnos.sqlite3')
        #Crea la tabla alumnos si no existe.
        tableName = 'alumnos'
        fieldsDescripcion = '('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'apellido TEXT NOT NULL, '\
            'nombre TEXT NOT NULL, '\
            'inscripcion DATETIME NOT NULL, '\
            'cursos_id INTEGER NOT NULL)'

        #Ejecuta el comando en la base de datos.
        self.conn.createTable(tableName=tableName, fieldsDescripcion=fieldsDescripcion)

    def create(self, apellido: str, nombre: str, inscripcion: datetime, cursos_id: int) -> list:
        command = 'INSERT INTO alumnos (apellido, nombre, inscripcion, cursos_id) VALUES (?, ?, ?, ?)'
        values = (apellido, nombre, inscripcion, cursos_id)
        return self.conn.execute(command, values)

    def read(self, Id: int) -> list:
        '''read Lee un registro de la base de datos.

        Args:
            id (int): Id del registro a leer.

        Returns:
            list: Retorna el registro leído.
        '''
        command = 'SELECT * FROM alumnos WHERE Id = ?'
        values = (Id,)
        return self.conn.execute(command, values)

    def update(self, Id: int, apellido: str, nombre: str, inscripcion: datetime, cursos_id: int) -> list:
        command = 'UPDATE alumnos SET apellido = ?, nombre = ?, inscripcion = ?, cursos_id = ? WHERE Id = ?'
        values = (apellido, nombre, inscripcion, cursos_id, Id )
        return self.conn.execute(command, values)

    def delete(self, Id: int) -> list:
        '''delete Borra un registro de la base de datos.

        Args:
            id (int): Id del registro a borrar.

        Returns:
            list: Devuelve el registro borrado.
        '''
        command = 'DELETE FROM alumnos WHERE Id = ?'
        values = (Id,)
        return self.conn.execute(command, values)

    def getAllData(self) -> list:
        '''getAllData Recupera todos los registros de alumnos con sus cursos y carreras correspondientes.

        Returns:
            list: devuelve una lista de alumnos con cursos y carreras.
        '''
        command = '''
        SELECT a.id, a.apellido, a.nombre, a.inscripcion, c.id, c.nombre, ca.id, ca.nombre
        FROM alumnos a
        INNER JOIN cursos c ON a.cursos_id = c.id
        INNER JOIN carreras ca ON c.carreras_id = ca.id
        '''
        result = self.conn.execute(command)
        print(result)
        return result

    def getAllCursos(self) -> list:
        '''getAllCursos Recupera todos los cursos con sus respectivos Id y nombres de la base de datos.

        Returns:
            list: devuelve una lista de cursos.
        '''
        command = '''
            SELECT id, nombre
            FROM cursos
        '''
        result = self.conn.execute(command)
        return result

    def __del__(self) -> None:
        '''__del__ Destructor de la clase.'''
        del self.conn
        del self

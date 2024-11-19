#cursos_models.py
from database import dbConn

class cursos_model():
    '''cursosModel Modelo de la tabla cursos.
    '''
    def __init__(self) -> None:
        '''__init__ Constructor de la clase, establece la conexión a la base
        de datos e intenta crear la tabla si no existe..
        '''
        self.nombre : str
        self.nivel : int
        self.carreras_id : int

        #Abre la conexión con la base de datos alumnos y si no existe la crea.
        self.conn = dbConn.dbConn('database\\alumnos.sqlite3')
        #Crea la tabla cursos si no existe.
        tableName = 'cursos'
        fieldsDescripcion = '('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '\
            'nombre TEXT NOT NULL UNIQUE, '\
            'nivel TEXT NOT NULL, '\
            'carreras_id INTEGER NOT NULL)'
        #Ejecuta el comando en la base de datos.
        self.conn.createTable(tableName=tableName, fieldsDescripcion=fieldsDescripcion)

    def create(self, nombre: str, nivel: int, carreras_id: int) -> list:
        command = 'INSERT INTO cursos (nombre, nivel, carreras_id) VALUES (?, ?, ?)'
        values = (nombre, nivel, carreras_id)
        return self.conn.execute(command, values)

    def read(self, Id: int) -> list:
        '''read Lee un registro de la base de datos.

        Args:
            id (int): Id del registro a leer.

        Returns:
            list: Retorna el registro leído.
        '''
        command = 'SELECT * FROM cursos WHERE Id = ?'
        values = (Id,)
        return self.conn.execute(command, values)

    def update(self, Id: int, nombre: str, nivel: int, carreras_id: int) -> list:
        command = 'UPDATE cursos SET nombre = ?, nivel = ?, carreras_id = ? WHERE Id = ?'
        values = (nombre, nivel, carreras_id, Id )
        return self.conn.execute(command, values)

    def delete(self, Id: int) -> list:
        '''delete Borra un registro de la base de datos.

        Args:
            id (int): Id del registro a borrar.

        Returns:
            list: Devuelve el registro borrado.
        '''
        # Primero verificamos si hay alumnos asociados al curso
        checkearAlumnos = '''
            SELECT COUNT(*)
            FROM alumnos
            WHERE cursos_id = ?
        '''
        result = self.conn.execute(checkearAlumnos, (Id,))[0][0]
        # Si hay alumnos asociados, levantamos una excepción
        if result > 0:
            return "No se puede eliminar el curso porque tiene alumnos asociados."
        # Si no hay alumnos asociados, procedemos con la eliminación
        command = 'DELETE FROM cursos WHERE Id = ?'
        self.conn.execute(command, (Id,))
        return "Carrera eliminada correctamente."

    def getAllData(self) -> list:
        '''getAllData Recupera todos los registros de la base de datos.

        Returns:
            list: devuelve una lista de cursos.
        '''
        command = '''
            SELECT c.id, c.nombre, c.nivel, c.carreras_id, ca.nombre AS carrera
            FROM cursos c
            INNER JOIN carreras ca ON c.carreras_id = ca.id
        '''
        result = self.conn.execute(command)
        return result

    def getAllCarreras (self) -> list:
        '''getAllCarreras Recupera todas las carreras con sus respectivos Id y nombres de la base de datos.

        Returns:
            list: devuelve una lista de carreras.
        '''
        command = '''
            SELECT id, nombre
            FROM carreras
        '''
        result = self.conn.execute(command)
        return result

    def __del__(self) -> None:
        '''__del__ Destructor de la clase.'''
        del self.conn
        del self

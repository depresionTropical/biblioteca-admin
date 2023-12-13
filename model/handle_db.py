import mysql.connector

class Autor():

    def __init__(self) -> None:
        self._conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin1234"
        )
        self._cursor = self._conn.cursor()

    def __del__(self) -> None:
        self._conn.close()

    def get_all(self):
        try:
            self._cursor.execute("SELECT * FROM Biblioteca.Autor")
            return self._cursor.fetchall()
        except Exception as e:
            print("Error al obtener los datos de clientes:", e)
            return []
    
    def get_by_id(self,id:int):
        self._cursor.execute(f"SELECT * FROM Biblioteca.Autor WHERE idAutor={id}")
        return self._cursor.fetchone()
    
    def insert(self,autor:dict):
        self._cursor.execute("INSERT INTO Biblioteca.Autor (Nombre,Apellido,Nacionalidad) VALUES ('{}','{}','{}')".format(
            autor['nombre'],
            autor['apellido'],
            autor['nacionalidad']
        ))
        self._conn.commit()
        return self._cursor.rowcount
    
    def get_id(self, autor:dict):
        self._cursor.execute("SELECT idCliente FROM Biblioteca.Autor WHERE Nombre = '{}' AND '{}' = 'Apellido';".format(
            autor['nombre'],
            autor['apellido']
        ))
        return self._cursor.fetchone()[0]
    

class Cliente():

    def __init__(self) -> None:
        self._conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin1234"
        )
        self._cursor = self._conn.cursor()

    def __del__(self) -> None:
        self._conn.close()

    def get_all(self):
        try:
            self._cursor.execute("SELECT * FROM Biblioteca.Cliente")
            return self._cursor.fetchall()
        except Exception as e:
            print("Error al obtener los datos de los libros:", e)
            return []
    
    def get_by_id(self,id):
        self._cursor.execute(f"SELECT * FROM Biblioteca.Cliente WHERE idCliente={id}")
        return self._cursor.fetchone()
    
    def insert(self,cliente:dict):
        self._cursor.execute("INSERT INTO Biblioteca.Cliente (Nombre,Apellido,fechaAlta) VALUES ('{}','{}','{}')".format(
            cliente['nombre'],
            cliente['apellido'],
            cliente['fecha_alta']
        ))
        self._conn.commit()
        return self._cursor.rowcount
    
    def get_id(self, autor:dict):
        self._cursor.execute("SELECT idCliente FROM Biblioteca.Cliente WHERE Nombre = '{}' AND '{}';".format(
            autor['nombre'],
            autor['apellido']
        ))
        result = self._cursor.fetchone()
        if result is not None:
            return result[0]  # Acceder al primer elemento del resultado
        else:
            return None  # Manejar el caso en que no haya resultados
            
    
class Libro():

    def __init__(self) -> None:
        self._conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin1234"
        )
        self._cursor = self._conn.cursor()

    def __del__(self) -> None:
        self._conn.close()

    def get_all(self):
        try:
            self._cursor.execute("SELECT * FROM Biblioteca.Libro")
            return self._cursor.fetchall()
        except Exception as e:
            print("Error al obtener los datos de los libros:", e)
            return []
        
    def get_all_not_devolved(self): 
        pass

    def get_by_id(self,id):
        self._cursor.execute(f"SELECT * FROM Biblioteca.Libro WHERE idLibro={id}")
        return self._cursor.fetchone()
    
    def insert(self,libro:dict):
        self._cursor.execute("INSERT INTO Biblioteca.Libro (Titulo,idAutor,fechaPublicacion) VALUES ('{}','{}','{}')".format(
            libro['titulo'],
            libro['idAutor'],
            libro['fecha_publicacion']
        ))
        self._conn.commit()
        return self._cursor.rowcount
    
    
    def get_id(self, libro):
        self._cursor.execute("SELECT idLibro FROM Biblioteca.Libro WHERE Titulo = '{}';".format(
            libro,
        ))
        return self._cursor.fetchone()[0]
    
class Prestamo():

    def __init__(self) -> None:
        self._conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin1234"
        )
        self._cursor = self._conn.cursor()

    def __del__(self) -> None:
        self._conn.close()

    def get_all(self):
        try:
            self._cursor.execute('''
    SELECT CONCAT(Cliente.Nombre, ' ', Cliente.Apellido) AS cliente,
           Libro.Titulo AS libro,
           Prestamo.fechaPrestamos,
           Prestamo.estatus
    FROM Biblioteca.Prestamo
    JOIN Biblioteca.Cliente ON Prestamo.idCliente = Cliente.idCliente
    JOIN Biblioteca.Libro ON Prestamo.idLibro = Libro.idLibro;
''')
            prestamos = self._cursor.fetchall()
            return prestamos
        except Exception as e:
            print("Error al obtener los datos de Prestamos:", e)
            return []

    
    def get_by_id(self,id):
        self._cursor.execute(f"SELECT * FROM Biblioteca.Prestamo WHERE idPrestamo={id}")
        return self._cursor.fetchone()
    
    def insert(self,prestamo:dict):
        self._cursor.execute("INSERT INTO Biblioteca.Prestamo (idCliente,idLibro,fechaPrestamos) VALUES ('{}','{}','{}')".format(
            prestamo['cliente'],
            prestamo['libro'],
            prestamo['fecha_prestamo']
        ))
        self._conn.commit()
        return self._cursor.rowcount
    
    def get_id(self, autor:dict):
        self._cursor.execute("SELECT idCliente FROM Biblioteca.Cliente WHERE Nombre = '{}' AND '{}' = 'Apellido';".format(
            autor['nombre'],
        ))
        return self._cursor.fetchone()[0]

    def update_status(self, nombre_libro, nombre_cliente, fecha_devolucion):
        try:
            nombre_cliente , apellido_cliente= nombre_cliente.split()
            query_get_ids = """
            SELECT Libro.idLibro, Cliente.idCliente
            FROM Biblioteca.Libro AS Libro
            JOIN Biblioteca.Cliente AS Cliente ON 1=1
            WHERE Libro.Titulo = %s AND Cliente.Nombre = %s AND Cliente.Apellido = %s;
            """
            self._cursor.execute(query_get_ids, (nombre_libro, nombre_cliente,apellido_cliente))
            result = self._cursor.fetchone()

            if not result:
                print("*No se encontró el libro o el cliente.")
                return -1  # O algún valor para manejar la falta de libro o cliente

            id_libro, id_cliente = result
            print(f"*Se encontró el libro y el cliente: {id_libro}, {id_cliente}")
            query_select = """
            SELECT Prestamo.idPrestamos 
            FROM Biblioteca.Prestamo AS Prestamo
            WHERE Prestamo.idLibro = %s AND Prestamo.idCliente = %s AND Prestamo.estatus = 0;
            """
            self._cursor.execute(query_select, (id_libro, id_cliente))
            id_prestamo = self._cursor.fetchone()

            if not id_prestamo:
                print("No se encontró un préstamo pendiente para el libro y cliente proporcionados.")
                return 0  # O algún valor para manejar la falta de préstamo pendiente

            query_update = "UPDATE Biblioteca.Prestamo SET estatus = 1, fecha_devolucion = %s WHERE idPrestamos = %s;"
            self._cursor.execute(query_update, (fecha_devolucion, id_prestamo[0]))
            self._conn.commit()

            if self._cursor.rowcount > 0:
                return self._cursor.rowcount  # Número de filas afectadas por la actualización
            else:
                print("No se realizaron cambios en la tabla.")
                return 0  # O algún valor para manejar el caso donde no se realizan cambios


        except Exception as e:
            print("Error al actualizar el estatus:", e)
            self._conn.rollback()
            return -1  # O algún valor para manejar el error
    # En tu archivo de manejo de base de datos
# Agrega un nuevo método en tu clase Prestamo para obtener los préstamos no devueltos
    def get_not_devolved(self):
        try:
            query = """
            SELECT Cliente.Nombre, Cliente.Apellido, Libro.Titulo, Prestamo.fechaPrestamos
            FROM Biblioteca.Prestamo AS Prestamo
            JOIN Biblioteca.Cliente AS Cliente ON Prestamo.idCliente = Cliente.idCliente
            JOIN Biblioteca.Libro AS Libro ON Prestamo.idLibro = Libro.idLibro
            WHERE Prestamo.estatus = 0;
            """
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            return result

        except Exception as e:
            print("Error al obtener préstamos no devueltos:", e)
            return []



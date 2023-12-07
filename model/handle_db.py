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
        self._cursor.execute("SELECT idCliente FROM Biblioteca.Cliente WHERE Nombre = '{}' AND '{}' = 'Apellido';".format(
            autor['nombre'],
            autor['apellido']
        ))
        return self._cursor.fetchone()[0]
    
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
    
    
    def get_id(self, autor:dict):
        self._cursor.execute("SELECT idLibro FROM Biblioteca.Libro WHERE Nombre = '{}';".format(
            autor['titulo'],
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
            self._cursor.execute('''SELECT Cliente.Nombre AS cliente, Libro.Titulo AS libro, Prestamo.fechaPrestamos, Prestamo.estatus FROM Biblioteca.Prestamo JOIN Biblioteca.Cliente ON Prestamo.idCliente = Cliente.idCliente JOIN Biblioteca.Libro ON Prestamo.idLibro = Libro.idLibro;''')
            prestamos = self._cursor.fetchall()
            print(prestamos)
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
        self._cursor.execute("SELECT idLibro FROM Biblioteca.prestamo WHERE Nombre = '{}';".format(
            autor['idPrestamo'],
        ))
        return self._cursor.fetchone()[0]

    def update_status(self, id_prestamo):
        print(id_prestamo)
        # try:
        #     self._cursor.execute("UPDATE Biblioteca.Prestamo SET estatus = 1 WHERE idPrestamo = {}".format(id_prestamo))
        #     self._conn.commit()
        #     return self._cursor.rowcount
        # except Exception as e:
        #     print("Error al actualizar el estatus:", e)
        #     self._conn.rollback()
        #     return -1  # O algún valor para manejar el error

# db = Libro()
# data={
#     'titulo':'Las novelas de la selva',
#     'idAutor':'30',
#     'fecha_publicacion':'2023-12-05'
# }
# db.insert(data)
# print(db.get_all())

# #print(Libro().get_all())
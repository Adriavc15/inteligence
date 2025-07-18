import sqlite3

class Objeto:
    def __init__(self, id_objeto,posicion, nombre):
        self.id_objeto = id_objeto
        self.posicion = posicion
        self.nombre = nombre

class BaseDatosObjetos:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_objetos()

    def crear_tabla_objetos(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS objetos (
                                idObjeto INTEGER PRIMARY KEY,
                                Posicion TEXT,
                                Nombre TEXT)''')
        self.conexion.commit()


    def consultar_objeto_por_id(self, Posicion):
        self.cursor.execute("SELECT * FROM objetos WHERE Posicion = ?", (Posicion,))
        resultado = self.cursor.fetchone()
        if resultado:
            return Objeto(resultado[0], resultado[1], resultado[2])
        else:
            return None



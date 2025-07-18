import sqlite3
from datetime import datetime
class Pertenencia:
    def __init__(self, codigo_pertenencia, tipo_objeto, imagen_pertenencia, id_estudiante,id_ultimo_estado,fecha_ultima_actividad,estado_text,objeto_text):
        self.codigo_pertenencia = codigo_pertenencia
        self.tipo_objeto = tipo_objeto
        self.imagen_pertenencia = imagen_pertenencia
        self.id_estudiante = id_estudiante
        self.id_ultimo_estado = id_ultimo_estado
        self.fecha_ultima_actividad = fecha_ultima_actividad
        self.estado_text = estado_text
        self.objeto_text=objeto_text

class PertenenciaEstudiante:
    def __init__(self, codigo_pertenencia, tipo_objeto, imagen_pertenencia, id_estudiante,id_ultimo_estado,fecha_ultima_actividad,estado_text,objeto_text,codigo_estudiante,nombres_estudiante,carrera_estudiante,plan_estudiante):
        self.codigo_pertenencia = codigo_pertenencia
        self.tipo_objeto = tipo_objeto
        self.imagen_pertenencia = imagen_pertenencia
        self.id_estudiante = id_estudiante
        self.id_ultimo_estado = id_ultimo_estado
        self.fecha_ultima_actividad = fecha_ultima_actividad
        self.estado_text = estado_text
        self.objeto_text=objeto_text
        self.codigo_estudiante=codigo_estudiante
        self.nombres_estudiante=nombres_estudiante
        self.carrera_estudiante=carrera_estudiante
        self.plan_estudiante=plan_estudiante


class BaseDatosPertenencia:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_pertenencias()

    def crear_tabla_pertenencias(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pertenencias (
                                codigoPertenencia INTEGER PRIMARY KEY AUTOINCREMENT,
                                tipoObjeto INTEGER,
                                imagenPertenencia TEXT,
                                idEstudiante INTEGER,
                                idUltimoEstado INTEGER,
                                FechaUltimaActividad INTEGER,
                                FOREIGN KEY (idUltimoEstado) REFERENCES estado_pertenencias(id),
                                FOREIGN KEY (idEstudiante) REFERENCES estudiantes(idEstudiante))''')
        self.conexion.commit()

    def registrar_pertenencia(self, tipo_objeto, imagen_pertenencia, id_estudiante, id_ultimo_estado, fecha_ultima_actividad):
        try:
            self.cursor.execute('''INSERT INTO pertenencias (tipoObjeto, imagenPertenencia, idEstudiante, idUltimoEstado, FechaUltimaActividad) 
                                    VALUES (?, ?, ?, ?, ?)''', 
                                (tipo_objeto, imagen_pertenencia, id_estudiante, id_ultimo_estado, fecha_ultima_actividad))
            self.conexion.commit()
            return self.cursor.lastrowid  # Devolver el ID del registro recién insertado
        except sqlite3.Error as e:
            print(f"Error al guardar la pertenencia: {e}")
            self.conexion.rollback()
            return -1  # Error al guardar la pertenencia

    def actualizar_pertenencia_por_actividad(self, codigo_pertenencia, nuevo_estado, nueva_fecha_actividad):
        try:
            self.cursor.execute('''UPDATE pertenencias 
                                SET idUltimoEstado = ?, FechaUltimaActividad = ? 
                                WHERE codigoPertenencia = ?''', 
                                (nuevo_estado, nueva_fecha_actividad, codigo_pertenencia))
            self.conexion.commit()
            return self.cursor.rowcount  # Devolver el número de filas afectadas
        except sqlite3.Error as e:
            print(f"Error al actualizar la pertenencia: {e}")
            self.conexion.rollback()
            return -1  # Error al actualizar la pertenencia


    def consultar_pertenencias_codigos(self, resultados_finales):
        lista_codigos = [resultado['codigo'] for resultado in resultados_finales]
        placeholders = ','.join(['?' for _ in lista_codigos])
        
        # Consulta para obtener las pertenencias según los códigos proporcionados
        query = f"""
            SELECT p.codigoPertenencia, p.tipoObjeto, p.imagenPertenencia, p.idEstudiante, p.idUltimoEstado, p.fechaUltimaActividad,ep.estado
            FROM pertenencias p
            JOIN estado_pertenencias ep ON p.idUltimoEstado = ep.id
            WHERE p.codigoPertenencia IN ({placeholders})
            ORDER BY CASE p.codigoPertenencia
            {''.join([f' WHEN {codigo} THEN {i}' for i, codigo in enumerate(lista_codigos)])}
            END
        """

        self.cursor.execute(query, lista_codigos)
        resultados = self.cursor.fetchall()
        pertenencias = []

        for resultado in resultados:
            pertenencia = Pertenencia(
                codigo_pertenencia=resultado[0],
                tipo_objeto=resultado[1],
                imagen_pertenencia=resultado[2],
                id_estudiante=resultado[3],
                id_ultimo_estado=resultado[4],
                fecha_ultima_actividad=resultado[5],
                estado_text=resultado[6],
                objeto_text=""
            )
            pertenencias.append(pertenencia)

        return pertenencias
    


    
    def cambiar_estado_pertenencias(self, codPertenencia, idEstado,fecha_hora_actual):
        try:
            self.cursor.execute('''UPDATE pertenencias 
                                SET idUltimoEstado = ?, FechaUltimaActividad = ?
                                WHERE codigoPertenencia = ?''',
                                (idEstado, fecha_hora_actual, codPertenencia))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al cambiar el estado de la pertenencia: {e}")
            self.conexion.rollback()
            return False

    def actualizar_pertenencia(self, codigo_pertenencia, tipo_objeto, imagen_pertenencia, id_estudiante):
        try:
            self.cursor.execute('''UPDATE pertenencias
                                   SET tipoObjeto = ?, imagenPertenencia = ?, idEstudiante = ?
                                   WHERE codigoPertenencia = ?''',
                                (tipo_objeto, imagen_pertenencia, id_estudiante, codigo_pertenencia))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar la pertenencia: {e}")
            self.conexion.rollback()
            return False


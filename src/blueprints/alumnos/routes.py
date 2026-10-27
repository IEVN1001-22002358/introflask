from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@alumnos_bp.route('/alumnos', methods=['GET'])
def lista_alumnos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT matricula,nombre,apaterno,amaterno,correo FROM alumnos""")

        datos = cursor.fetchall()
        alumnos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error al consultar los alumnos: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route('/alumnos', methods=['POST'])
def registrar_alumno():
    cursor = None
    try:
        datos = request.get_json()
        
        matricula = datos.get('matricula')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        correo = datos.get('correo')

        cursor = mysql.connection.cursor()
        
        sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (matricula, nombre, apaterno, amaterno, correo))
        
        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Alumno registrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al registrar el alumno: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route('/alumnos', methods=['PUT'])
def actualizar_alumno():
    cursor = None
    try:
        datos = request.get_json()
        
        matricula = datos.get('matricula')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        correo = datos.get('correo')

        if not matricula:
            return jsonify({
                'mensaje': 'La matrícula es obligatoria para actualizar',
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()
        
        sql = """UPDATE alumnos 
                 SET nombre = %s, apaterno = %s, amaterno = %s, correo = %s 
                 WHERE matricula = %s"""
        
        cursor.execute(sql, (nombre, apaterno, amaterno, correo, matricula))
        
        mysql.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({
                'mensaje': 'Alumno actualizado correctamente',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se encontró ningún alumno con esa matrícula',
                'exito': False
            }), 404

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al actualizar el alumno: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route('/alumnos/<matricula>', methods=['DELETE'])
def eliminar_alumno(matricula):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (matricula,))
        
        mysql.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({
                'mensaje': 'Alumno eliminado correctamente',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se encontró ningún alumno con esa matrícula',
                'exito': False
            }), 404

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al eliminar el alumno: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
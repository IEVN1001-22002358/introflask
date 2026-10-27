from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@maestros_bp.route('/maestros', methods=['GET'])
def lista_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT Idmaestro,nombre,apaterno,amaterno,correo FROM maestros""")

        datos = cursor.fetchall()
        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error al consultar los profes: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/maestros', methods=['POST'])
def registrar_maestro():
    cursor = None
    try:
        datos = request.get_json()
        
        idmaestro = datos.get('Idmaestro')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        correo = datos.get('correo')

        cursor = mysql.connection.cursor()
        
        sql = """INSERT INTO maestros (Idmaestro, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (idmaestro, nombre, apaterno, amaterno, correo))
        
        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro registrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al registrar el maestro: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/maestros', methods=['PUT'])
def actualizar_maestro():
    cursor = None
    try:
        datos = request.get_json()
        
        idmaestro = datos.get('Idmaestro')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        correo = datos.get('correo')

        if not idmaestro:
            return jsonify({
                'mensaje': 'El Idmaestro es obligatorio para actualizar',
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()
        
        sql = """UPDATE maestros 
                 SET nombre = %s, apaterno = %s, amaterno = %s, correo = %s 
                 WHERE Idmaestro = %s"""
        
        cursor.execute(sql, (nombre, apaterno, amaterno, correo, idmaestro))
        mysql.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({
                'mensaje': 'Maestro actualizado correctamente',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se encontró ningún maestro con ese ID',
                'exito': False
            }), 404

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al actualizar el maestro: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/maestros/<idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM maestros WHERE Idmaestro = %s"
        
        cursor.execute(sql, (idmaestro,))
        
        mysql.connection.commit()
        if cursor.rowcount > 0:
            return jsonify({
                'mensaje': 'Maestro eliminado correctamente',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se encontró ningún maestro con ese ID',
                'exito': False
            }), 404

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al eliminar el maestro: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
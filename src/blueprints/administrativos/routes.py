from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@administrativos_bp.route('/administrativos', methods=['GET'])
def lista_administrativos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT numempleado, nombre, apaterno, amaterno, telefono, correo, departamento FROM administrativos""")

        datos = cursor.fetchall()
        administrativos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error al consultar los administrativos: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/administrativos', methods=['POST'])
def registrar_administrativo():
    cursor = None
    try:
        datos = request.get_json()
        
        numempleado = datos.get('numempleado')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        telefono = datos.get('telefono')
        correo = datos.get('correo')
        departamento = datos.get('departamento')

        cursor = mysql.connection.cursor()
        
        sql = """INSERT INTO administrativos (numempleado, nombre, apaterno, amaterno, telefono, correo, departamento) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (numempleado, nombre, apaterno, amaterno, telefono, correo, departamento))
        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Administrativo registrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al registrar el administrativo: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/administrativos', methods=['PUT'])
def actualizar_administrativo():
    cursor = None
    try:
        datos = request.get_json()
        
        numempleado = datos.get('numempleado')
        nombre = datos.get('nombre')
        apaterno = datos.get('apaterno')
        amaterno = datos.get('amaterno')
        telefono = datos.get('telefono')
        correo = datos.get('correo')
        departamento = datos.get('departamento')

        if not numempleado:
            return jsonify({
                'mensaje': 'El número de empleado es obligatorio para actualizar',
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()
        
        sql = """UPDATE administrativos 
                 SET nombre = %s, apaterno = %s, amaterno = %s, telefono = %s, correo = %s, departamento = %s 
                 WHERE numempleado = %s"""
        
        cursor.execute(sql, (nombre, apaterno, amaterno, telefono, correo, departamento, numempleado))
        mysql.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({
                'mensaje': 'Administrativo actualizado correctamente',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se encontró ningún administrativo con ese número de empleado',
                'exito': False
            }), 404

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al actualizar el administrativo: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/administrativos/<numempleado>', methods=['DELETE'])
def eliminar_administrativo(numempleado):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM administrativos WHERE numempleado = %s"
        cursor.execute(sql, (numempleado,))
        
        mysql.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({
                'mensaje': 'Administrativo eliminado correctamente',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se encontró ningún administrativo con ese número de empleado',
                'exito': False
            }), 404

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f"Error al eliminar el administrativo: {ex}",
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
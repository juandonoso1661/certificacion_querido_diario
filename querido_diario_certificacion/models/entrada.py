from config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Entrada:
    def __init__(self, data):
        self.id_entrada = data['id_entradas']
        self.fecha = data['fecha']
        self.notas = data['notas']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO entradas (fecha, notas, usuario_id)
            VALUES (%(fecha)s, %(notas)s, %(usuario_id)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def get_all_by_user(cls, usuario_id):

        query = """
            SELECT * FROM entradas 
            WHERE usuario_id = %(usuario_id)s 
            ORDER BY fecha DESC, created_at DESC;
        """
        data = {'usuario_id': usuario_id}
        results = connectToMySQL().query_db(query, data)
        
        entradas = []
        if results:
            for row in results:
                entradas.append(cls(row))
        return entradas

    @classmethod
    def get_by_id(cls, entrada_id):
        query = "SELECT * FROM entradas WHERE id_entradas = %(id)s;"
        data = {'id': entrada_id}
        results = connectToMySQL().query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE entradas 
            SET fecha = %(fecha)s, notas = %(notas)s 
            WHERE id_entradas = %(id_entrada)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def delete(cls, entrada_id, usuario_id):

        query = "DELETE FROM entradas WHERE id_entradas = %(id)s AND usuario_id = %(usuario_id)s;"
        data = {'id': entrada_id, 'usuario_id': usuario_id}
        return connectToMySQL().query_db(query, data)

    @classmethod
    def search_by_keyword(cls, usuario_id, keyword):
        query = """
            SELECT * FROM entradas 
            WHERE usuario_id = %(usuario_id)s AND notas LIKE %(keyword)s 
            ORDER BY fecha DESC;
        """
        data = {
            'usuario_id': usuario_id,
            'keyword': f"%{keyword}%"
        }
        results = connectToMySQL().query_db(query, data)
        
        entradas = []
        if results:
            for row in results:
                entradas.append(cls(row))
        return entradas

    @staticmethod
    def validar_entrada(data):
        is_valid = True

        if not data['fecha']:
            flash("La fecha es obligatoria.", "entrada")
            is_valid = False
        else:
            try:
                fecha_ingresada = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
                if fecha_ingresada > datetime.now().date():
                    flash("La fecha no puede ser futura.", "entrada")
                    is_valid = False
            except ValueError:
                flash("Formato de fecha no válido.", "entrada")
                is_valid = False

        if len(data['notas'].strip()) < 1:
            flash("Las notas no pueden estar vacías.", "entrada")
            is_valid = False

        return is_valid
from config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.edad = data['edad']
        self.password = data['password']
        self.created_at = data['created_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, edad, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(edad)s, %(password)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        results = connectToMySQL().query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE id_usuario = %(id)s;"
        data = {'id': usuario_id}
        results = connectToMySQL().query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar_registro(user_data):
        is_valid = True

        if len(user_data['nombre'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        if len(user_data['apellido'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        if not EMAIL_REGEX.match(user_data['email']):
            flash("Formato de correo electrónico no válido.", "registro")
            is_valid = False
        else:
            usuario_existente = Usuario.get_by_email(user_data['email'])
            if usuario_existente:
                flash("Este correo electrónico ya está registrado.", "registro")
                is_valid = False

        if not user_data['edad'] or int(user_data['edad']) < 1:
            flash("Ingresa una edad válida.", "registro")
            is_valid = False

        if len(user_data['password']) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "registro")
            is_valid = False

        if user_data['password'] != user_data['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False

        return is_valid
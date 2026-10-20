from flask import Blueprint, render_template, redirect, request, session, flash
from models.usuario import Usuario

# Definimos el Blueprint para el módulo de usuarios
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    # Importamos bcrypt localmente para verificar el hash sin crear dependencias circulares
    from server import bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "edad": request.form['edad'],
        "password": pw_hash
    }

    usuario_id = Usuario.save(data)
    if not usuario_id:
        flash("No se pudo completar el registro. Inténtalo de nuevo.", "registro")
        return redirect('/')

    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = request.form['nombre']

    return redirect('/dashboard')

@usuarios_bp.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email(request.form['email'])

    if not usuario:
        flash("Correo electrónico no registrado.", "login")
        return redirect('/')

    from server import bcrypt
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Contraseña incorrecta.", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id_usuario
    session['usuario_nombre'] = usuario.nombre

    return redirect('/dashboard')

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
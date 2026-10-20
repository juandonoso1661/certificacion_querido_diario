from flask import render_template, redirect, request, session, flash
from server import app, bcrypt
from models.usuario import Usuario

@app.route('/')
def index():

    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/registrar', methods=['POST'])
def registrar():

    if not Usuario.validar_registro(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "edad": request.form['edad'],
        "password": pw_hash
    }

    usuario_id = Usuario.save(data)

    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = request.form['nombre']

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():

    usuario = Usuario.get_by_email(request.form['email'])

    if not usuario:
        flash("Correo electrónico no registrado.", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Contraseña incorrecta.", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id_usuario
    session['usuario_nombre'] = usuario.nombre

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
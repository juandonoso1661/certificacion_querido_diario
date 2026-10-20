from flask import Blueprint, render_template, redirect, request, session, flash
from models.entrada import Entrada

entradas_bp = Blueprint('entradas', __name__)

def verificar_sesion():
    return 'usuario_id' in session

@entradas_bp.route('/dashboard')
def dashboard():
    if not verificar_sesion():
        return redirect('/')

    entradas = Entrada.get_all_by_user(session['usuario_id'])
    return render_template('dashboard.html', entradas=entradas)

@entradas_bp.route('/entradas/nueva')
def nueva_entrada():
    if not verificar_sesion():
        return redirect('/')
    return render_template('nueva_entrada.html')

@entradas_bp.route('/entradas/crear', methods=['POST'])
def crear_entrada():
    if not verificar_sesion():
        return redirect('/')

    if not Entrada.validar_entrada(request.form):
        return redirect('/entradas/nueva')

    data = {
        'fecha': request.form['fecha'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    Entrada.save(data)
    return redirect('/dashboard')

@entradas_bp.route('/entradas/<int:id>')
def ver_entrada(id):
    if not verificar_sesion():
        return redirect('/')

    entrada = Entrada.get_by_id(id)

    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    return render_template('ver_entrada.html', entrada=entrada)

@entradas_bp.route('/entradas/<int:id>/editar')
def editar_entrada(id):
    if not verificar_sesion():
        return redirect('/')

    entrada = Entrada.get_by_id(id)
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    return render_template('editar_entrada.html', entrada=entrada)

@entradas_bp.route('/entradas/<int:id>/actualizar', methods=['POST'])
def actualizar_entrada(id):
    if not verificar_sesion():
        return redirect('/')

    if not Entrada.validar_entrada(request.form):
        return redirect(f'/entradas/{id}/editar')

    data = {
        'id_entrada': id,
        'fecha': request.form['fecha'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    Entrada.update(data)
    return redirect('/dashboard')

@entradas_bp.route('/entradas/<int:id>/eliminar')
def eliminar_entrada(id):
    if not verificar_sesion():
        return redirect('/')

    Entrada.delete(id, session['usuario_id'])
    return redirect('/dashboard')

@entradas_bp.route('/buscar', methods=['GET'])
def buscar():
    if not verificar_sesion():
        return redirect('/')

    keyword = request.args.get('q', '')
    if keyword.strip():
        entradas = Entrada.search_by_keyword(session['usuario_id'], keyword)
    else:
        entradas = Entrada.get_all_by_user(session['usuario_id'])

    return render_template('dashboard.html', entradas=entradas, busqueda=keyword)
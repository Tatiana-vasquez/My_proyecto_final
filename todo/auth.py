from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from todo import db
from .models import User
from . import models

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))
        error = None
        user_name = User.query.filter_by(username=username).first() #esto me consulta q no hay dos user con el mismo nombre
        if user_name is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado' #esto me mustra el error si el usuario ya esta registrado
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        # validar datos
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'
        # iniciar sesion
        if error is None: # si no hay error, se inicia sesion
            session.clear() # me limpia la sesion si hay una abierta
            session['user_id'] = user.id #esta session me guarda el id del usuario ya creado para q inicie sesion
            db.session.commit()
            return redirect(url_for('todo.home')) #me redireciona al home de la app
        flash(error)
    else:
        pass
    return render_template('auth/login.html')


# resgistrando esta funcion para que se ejecute en cada peticion, decorador, verifica si alguien a iniciado session
@bp.before_app_request  # este decorador me registra esta peticion para q verifique esto primero q todo
def load_logged_in_user():  # mantiene la sesion iniciada
    user_id = session.get('user_id') #user_id tiene el user logeado

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

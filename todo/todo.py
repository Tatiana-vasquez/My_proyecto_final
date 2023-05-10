from typing import Type

from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash
from sqlalchemy.sql.functions import current_user

from todo.auth import login_required
from .models import Partida, User
from todo import db
from flask import session

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/home')
def home():
    return render_template('todo/home.html')


@bp.route('/crear-partida', methods=['GET', 'POST'])
def crear_partida():  # crear partida, q reciba una lista de celebrities
    if request.method == 'POST':
        import json
        data = {
            "retados": request.form.getlist("retado"),
            "modelos": [
                (cel, desc) for cel, desc in zip(request.form.getlist("celebrity"), request.form.getlist("desc")) if cel
            ]
        }
        partida = Partida(retados=json.dumps(data["retados"]), famosos=json.dumps(data["modelos"]),
                          created_by=g.user.id)
        db.session.add(partida)
        db.session.commit()
        flash('Partida Creada exitosamente')
        return render_template('todo/home.html')
    else:
        users_list = db.session.query(User).all()
        user = User.query.all()
        return render_template('todo/crear-partida.html', users_list=users_list, users=user)


@bp.route('/partidas-asignadas<int:partida_id>', methods=['GET', 'POST'])
def partidas_asignadas(partida_id):
    partidas = Partida.query.get_or_404(partida_id)
    return render_template('todo/partidas-asignadas.html', partidas=partidas)


@bp.route('/mis-partidas/<int:user_id>', methods=['GET', 'POST'])
def mis_partidas(user_id):
    partidas = Partida.query.filter(Partida.retados.contains(str(user_id))).all()
    famosos = []
    usuarios = []  # Agregar esta línea
    for partida in partidas:
        famosos.append(partida.famosos)
        user = User.query.filter_by(id=partida.created_by).first()
        usuarios.append(user.username)  # Agregar el nombre de usuario a la lista de usuarios
    return render_template('todo/mis-partidas.html', partidas=partidas, famosos=famosos,
                           usuarios=usuarios)  # Pasar la lista de usuarios a la plantilla


@bp.route('/jugar-partida', methods=['GET', 'POST'])
def jugar_partida():
    # consulta en la bbdd
    todas_las_partidas = db.session.query(Partida).filter_by()
    for i in todas_las_partidas:
        print(i)
    return render_template('todo/jugar-partida.html',
                           lista_de_todas_las_partidas=todas_las_partidas)  # listade tareas es la variable q le he enviado al html


@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    todo = db.session.query(Partida).filter_by(id=id)
    todo.delete()
    db.session.commit()
    partidas = db.session.query(Partida).all()  # me devuelve una lista de partidas
    return render_template('todo/mis-partidas.html', partidas=partidas)

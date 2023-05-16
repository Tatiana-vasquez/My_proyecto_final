import json
from typing import Type

from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash
from sqlalchemy.sql.functions import current_user

from todo.auth import login_required
from .models import Partida, User

from todo import db
from flask import session

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/home')
@login_required
def home():
    return render_template('todo/home.html')


@bp.route('/crear-partida', methods=['GET', 'POST'])
@login_required
def crear_partida():  # crear partida, q reciba una lista de celebrities
    if request.method == 'POST':
        import json
        data = {
            "retados": request.form.get("retado"),
            "modelos": [
                (cel, desc) for cel, desc in zip(request.form.getlist("celebrity"), request.form.getlist("desc")) if cel
            ]
        }
        partida = Partida(retados=data["retados"], famosos=json.dumps(data["modelos"]),
                          created_by=g.user.id, votos='[]')
        db.session.add(partida)
        db.session.commit()
        flash('Partida Creada exitosamente')
        return render_template('todo/home.html')
    else:
        users_list = db.session.query(User).all()
        user = User.query.all()
        return render_template('todo/crear-partida.html', users_list=users_list, users=user)


@bp.route('/partida/<int:id>', methods=['GET', 'POST'])
@login_required
def partida(id):
    partida = db.session.query(Partida).filter_by(id=id).first()
    votos = json.loads(partida.votos)
    famosos = json.loads(partida.famosos)
    if request.method == 'POST':
        votos.append(request.form.get('chosen'))
        partida.votos = json.dumps(votos)
        db.session.commit()
    if len(votos) >0 and len(votos) >= len(famosos)-1:
        index_ganador = int(votos[-1]) #esto me dice quien es la ultima famosa escogida
        ganador = famosos[index_ganador][0] #por ende este es el ganador
        return render_template('todo/partida.html', partida=partida, ganador= ganador)
    if len(votos) == 0: # si la lista de votos es 0 me empieza a soltar los famosos
        index_left = 0
    else:
        index_left = int(votos[-1])
    index_right = len(votos) + 1
    famoso_left = famosos[index_left][0]# esto me recorre la lista, famoso left es el nombre
    famoso_right = famosos[index_right][0]
    return render_template('todo/partida.html', partida=partida, index_right = index_right, index_left = index_left, ganador = None, famoso_left=famoso_left,famoso_right=famoso_right )


@bp.route('/mis-partidas/<int:user_id>', methods=['GET', 'POST'])
@login_required
def mis_partidas(user_id):
    partidas_recibidas = Partida.query.filter(Partida.retados.contains(str(user_id))).all()
    partidas_enviadas = Partida.query.filter(Partida.created_by.contains(str(user_id))).all()

    return render_template('todo/mis-partidas.html',  partidas_recibidas= partidas_recibidas,partidas_enviadas=partidas_enviadas, User=User, json=json, len=len)


@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    todo = db.session.query(Partida).filter_by(id=id)
    todo.delete()
    db.session.commit()
    partidas = db.session.query(Partida).all()  # me devuelve una lista de partidas
    return render_template('todo/mis-partidas.html', partidas=partidas)

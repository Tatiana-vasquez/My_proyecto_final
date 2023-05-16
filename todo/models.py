from sqlalchemy import ForeignKey
from todo import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)  # username
    password = db.Column(db.Integer, nullable=False)  # password

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User:{self.username} >'


class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    retados = db.Column(db.Text)
    famosos = db.Column(db.Text)
    votos = db.Column(db.Text)

    def __init__(self, created_by, retados, famosos, votos):
        self.created_by = created_by
        self.retados = retados
        self.famosos = famosos
        self.votos = votos

    def __repr__(self):
        return f'<Partida:{self.famosos} >'



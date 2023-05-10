from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# create the extension
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)  # servidor web, # create the app
    #configuracion del proyecto
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db" #esto me crea la bd no tablas
    # initialize the app with the extension
    db.init_app(app)

    # registrar blueprint
    from . import todo
    app.register_blueprint(todo.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template("index.html")
        # migrar los modelos a la base de datos
    with app.app_context():
        db.create_all()

    return app

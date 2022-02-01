from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv


def build_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB = SQLAlchemy(app)

    class Song(DB.Model):
        id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
        name = DB.Column(DB.String(25), nullable=False)
        artist = DB.Column(DB.String(25), nullable=False)
        # ..........
        # ..........
        # ..........

        def __repr__(self):
            return f"{self.name} by {self.artist}"

    DB.init_app(app)

    @app.route('/')
    def root():
        title = "Welcome to the Spotify Song Suggester app"
        description = "It's a work in progress"
        DB.create_all()
        return render_template(
            'home.html', title=title, description=description)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template(
            'home.html', description='Database has been reset')

    return app

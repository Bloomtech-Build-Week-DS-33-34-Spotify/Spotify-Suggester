from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_assets import Bundle, Environment


def build_app():

    app = Flask(__name__)

    # To use the provided javascript and css template
    js = Bundle('breakpoints.min.js', 'browser.min.js',
                'jquery.min.js', 'jquery.scrolly.min.js', 'main.js',
                'util.js', output='gen/all.js')

    css = Bundle('fontawesome-all.min.css',
                 'main.css', output='gen/all.css')

    assets = Environment(app)

    assets.register('all_js', js)
    assets.register('all_css', css)

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
        return render_template('index.html')

    @app.route('/rec', methods=['POST'])
    def recommend():
        user_input = request.values['text_input']
        # do data science here
        return render_template('rec.html')

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return 'Database has been reset'

    return app

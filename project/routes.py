from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_assets import Bundle, Environment
from .api import get_track_features
from .models import get_rec_track


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

    #app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #DB = SQLAlchemy(app)

    # DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/rec', methods=['POST'])
    def recommend():
        user_text = request.values['text_input']
        if "by" not in user_text:
            message = "make sure to include the artist!"
            return render_template('index.html', message=message)
        else:
            (user_track_name, user_track_artist, user_track_id,
             user_track_features) = get_track_features(user_text)

            (rec_track_name, rec_track_artist, rec_track_id) = get_rec_track(
                user_track_id, user_track_features)
            return render_template('rec.html', user_track=user_track_name, user_artist=user_track_artist,
                                   rec_track=rec_track_name, rec_artist=rec_track_artist)

    return app

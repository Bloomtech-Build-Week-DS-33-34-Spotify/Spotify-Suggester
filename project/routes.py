from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_assets import Bundle, Environment
from .api import get_track_features
from .models import get_rec_tracks


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

            rec_tracks = get_rec_tracks(user_track_id, user_track_features)

            rt1_id = rec_tracks.loc[0]['id']
            rt1_name = rec_tracks.loc[0]['name']
            rt1_artist = rec_tracks.loc[0]['artists']

            rt2_id = rec_tracks.loc[1]['id']
            rt2_name = rec_tracks.loc[1]['name']
            rt2_artist = rec_tracks.loc[1]['artists']

            rt3_id = rec_tracks.loc[2]['id']
            rt3_name = rec_tracks.loc[2]['name']
            rt3_artist = rec_tracks.loc[2]['artists']

            rt4_id = rec_tracks.loc[3]['id']
            rt4_name = rec_tracks.loc[3]['name']
            rt4_artist = rec_tracks.loc[3]['artists']

            rt5_id = rec_tracks.loc[4]['id']
            rt5_name = rec_tracks.loc[4]['name']
            rt5_artist = rec_tracks.loc[4]['artists']

            return render_template('rec.html', user_track=user_track_name, user_artist=user_track_artist,
                                   rt1=rt1_name, ra1=rt1_artist,
                                   rt2=rt2_name, ra2=rt2_artist,
                                   rt3=rt3_name, ra3=rt3_artist,
                                   rt4=rt4_name, ra4=rt4_artist,
                                   rt5=rt5_name, ra5=rt5_artist)

    return app

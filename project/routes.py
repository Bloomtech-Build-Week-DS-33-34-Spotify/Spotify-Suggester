from flask import Flask, render_template, request
from os import getenv
from flask_assets import Bundle, Environment
from .api import get_track_features
from .models import get_rec_tracks, format_user_track_features


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

    # app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # DB = SQLAlchemy(app)

    # DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/rec', methods=['POST'])
    def recommend():
        user_text = request.values['text_input']
        user_year = int(request.values['year_input'])
        if " by " not in user_text:
            message = "Make sure to include the artist!"
            return render_template('index.html', message=message)
        else:
            try:
                (user_track_name, user_track_artist, user_track_id,
                    user_track_features) = get_track_features(user_text)
            except:
                message = "That didn't work. Try again!"
                return render_template('index.html', message=message)

            try:
                rec_tracks = get_rec_tracks(
                    user_track_id, user_track_features, user_year)
            except:
                message = "There is something wrong. Come try again at a later time."
                return render_template('index.html', message=message)

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

            # Graphs
            df_user_track = format_user_track_features(user_track_features)

            data1 = []
            data1.append(
                (user_track_name, df_user_track['danceability'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['danceability'])
                data1.append(tup)
            legend1 = "danceability"
            labels1 = [row[0] for row in data1]
            values1 = [float(row[1]) for row in data1]

            data2 = []
            data2.append(
                (user_track_name, df_user_track['energy'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['energy'])
                data2.append(tup)
            legend2 = "energy"
            labels2 = [row[0] for row in data2]
            values2 = [float(row[1]) for row in data2]

            data3 = []
            data3.append(
                (user_track_name, df_user_track['key'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['key'])
                data3.append(tup)
            legend3 = "key"
            labels3 = [row[0] for row in data3]
            values3 = [float(row[1]) for row in data3]

            data4 = []
            data4.append(
                (user_track_name, df_user_track['loudness'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['loudness'])
                data4.append(tup)
            legend4 = "loudness"
            labels4 = [row[0] for row in data4]
            values4 = [float(row[1]) for row in data4]

            data5 = []
            data5.append(
                (user_track_name, df_user_track['mode'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['mode'])
                data5.append(tup)
            legend5 = "mode"
            labels5 = [row[0] for row in data5]
            values5 = [float(row[1]) for row in data5]

            data6 = []
            data6.append(
                (user_track_name, df_user_track['speechiness'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['speechiness'])
                data6.append(tup)
            legend6 = "speechiness"
            labels6 = [row[0] for row in data6]
            values6 = [float(row[1]) for row in data6]

            data7 = []
            data7.append(
                (user_track_name, df_user_track['acousticness'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['acousticness'])
                data7.append(tup)
            legend7 = "acousticness"
            labels7 = [row[0] for row in data7]
            values7 = [float(row[1]) for row in data7]

            data8 = []
            data8.append(
                (user_track_name, df_user_track['instrumentalness'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['instrumentalness'])
                data8.append(tup)
            legend8 = "instrumentalness"
            labels8 = [row[0] for row in data8]
            values8 = [float(row[1]) for row in data8]

            data9 = []
            data9.append(
                (user_track_name, df_user_track['liveness'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['liveness'])
                data9.append(tup)
            legend9 = "liveness"
            labels9 = [row[0] for row in data9]
            values9 = [float(row[1]) for row in data9]

            data10 = []
            data10.append(
                (user_track_name, df_user_track['valence'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['valence'])
                data10.append(tup)
            legend10 = "valence"
            labels10 = [row[0] for row in data10]
            values10 = [float(row[1]) for row in data10]

            data11 = []
            data11.append(
                (user_track_name, df_user_track['tempo'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['tempo'])
                data11.append(tup)
            legend11 = "tempo"
            labels11 = [row[0] for row in data11]
            values11 = [float(row[1]) for row in data11]

            data12 = []
            data12.append(
                (user_track_name, df_user_track['time_signature'][0]))
            for i in range(len(rec_tracks)):
                tup = (rec_tracks.loc[i]['name'],
                       rec_tracks.loc[i]['time_signature'])
                data12.append(tup)
            legend12 = "time_signature"
            labels12 = [row[0] for row in data12]
            values12 = [float(row[1]) for row in data12]

            return render_template('rec.html', user_track=user_track_name, user_artist=user_track_artist, user_year=str(user_year),
                                   rt1=rt1_name, ra1=rt1_artist, rid1=rt1_id,
                                   rt2=rt2_name, ra2=rt2_artist, rid2=rt2_id,
                                   rt3=rt3_name, ra3=rt3_artist, rid3=rt3_id,
                                   rt4=rt4_name, ra4=rt4_artist, rid4=rt4_id,
                                   rt5=rt5_name, ra5=rt5_artist, rid5=rt5_id,
                                   labels1=labels1, values1=values1, legend1=legend1,
                                   labels2=labels2, values2=values2, legend2=legend2,
                                   labels3=labels3, values3=values3, legend3=legend3,
                                   labels4=labels4, values4=values4, legend4=legend4,
                                   labels5=labels5, values5=values5, legend5=legend5,
                                   labels6=labels6, values6=values6, legend6=legend6,
                                   labels7=labels7, values7=values7, legend7=legend7,
                                   labels8=labels8, values8=values8, legend8=legend8,
                                   labels9=labels9, values9=values9, legend9=legend9,
                                   labels10=labels10, values10=values10, legend10=legend10,
                                   labels11=labels11, values11=values11, legend11=legend11,
                                   labels12=labels12, values12=values12, legend12=legend12
                                   )

    return app

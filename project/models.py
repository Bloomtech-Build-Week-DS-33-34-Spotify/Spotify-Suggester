import numpy as np
import pandas as pd


def get_rec_track(user_track_id, user_track_features):
    '''
    Takes a list of track features and returns the recommended song in tuple
    '''
    user_vector = np.array(user_track_features)

    df = pd.read_csv("project/static/tracks_features.csv")

    feature_columns = ['danceability', 'energy', 'key', 'loudness',	'mode',
                       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                       'valence', 'tempo', 'time_signature']
    df_X = df[feature_columns]

    X_matrix = df_X.to_numpy()
    #X_norm = preprocessing.normalize(X_matrix, norm='l2')
    cos_sims = []
    #user_vector_norm = preprocessing.normalize(user_vector.reshape(1,-1), norm='l2')[0]
    for i in range(len(X_matrix)):
        #cos_sim = cosine(user_song_norm, X_matrix[i])
        cos_sim = np.dot(
            user_vector, X_matrix[i])/(np.linalg.norm(user_vector)*np.linalg.norm(X_matrix[i]))
        cos_sims.append((cos_sim))

    df['similarity'] = cos_sims

    df_final = df[['id', 'name', 'album', 'artists', 'artist_ids',
                   'similarity']].sort_values(by='similarity', ascending=False).reset_index()

    if user_track_id in df_final.id.values:
        rec_track_id = df_final.loc[1]['id']
        rec_track_name = df_final.loc[1]['name']
        rec_track_artist = df_final.loc[1]['artists']
    else:
        rec_track_id = df_final.loc[0]['id']
        rec_track_name = df_final.loc[0]['name']
        rec_track_artist = df_final.loc[0]['artists']

    char_to_remove = ["'", '"', "[", "]"]

    for char in char_to_remove:
        rec_track_artist = rec_track_artist.replace(char, "")

    return (rec_track_name, rec_track_artist, rec_track_id)

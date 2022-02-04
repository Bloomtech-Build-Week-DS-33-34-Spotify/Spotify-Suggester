import numpy as np
import pandas as pd
from .mongodb import tracks_features


def get_rec_tracks(user_track_id, user_track_features, user_year):
    '''
    Takes a list of track features and returns n=5 recommended tracks
    '''
    user_vector = np.array(user_track_features)

    df = pd.DataFrame(list(tracks_features.find({'year': str(user_year)})))

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

    df_final = df[['id', 'name', 'artists',
                   'similarity']].sort_values(by='similarity', ascending=False).reset_index(drop=True)

    df_final.drop(columns='similarity', inplace=True)

    if user_track_id in df_final.id.values:
        rec_tracks = df_final.loc[1:5].reset_index(drop=True)
    else:
        rec_tracks = df_final.loc[:4]

    def format_artist(artist_str):
        char_to_remove = ["'", '"', "[", "]"]
        for char in char_to_remove:
            artist_str = artist_str.replace(char, "")
        return artist_str

    rec_tracks['artists'] = rec_tracks['artists'].apply(format_artist)

    return rec_tracks

# import base64

import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')


def set_bg_hack_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://image.shutterstock.com/image-vector/film-strips-cinema-rell-isolated-260nw-1415904974.jpg");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


set_bg_hack_url()


# [theme]
# backgroundColor = "#4e615e"
# textColor = "#c8dbdb"
# font = "sans serif"


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    rec_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    recommendations_posters = []

    for i in rec_movies:
        movie_id = movies.iloc[i[0]].id
        movie_title = movies.iloc[i[0]].title

        recommendations.append(movie_title)
        recommendations_posters.append(fetch_poster(movie_id))

    return recommendations, recommendations_posters


selected_movie = st.selectbox(
    'Enter the movie name',
    movies_list)

if st.button('Recommend'):
    # recommendations = recommend(selected_movie)
    recommendations, recommendations_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(recommendations_posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(recommendations_posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(recommendations_posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(recommendations_posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(recommendations_posters[4])

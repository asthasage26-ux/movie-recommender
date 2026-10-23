import pandas as pd
import streamlit as st
import pickle
import requests




@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    api_key = "30e93b9f8ffa915f07d0b92e31851427"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            params={"api_key": api_key},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except requests.exceptions.RequestException as e:
        print(f"TMDB error for movie {movie_id}: {e}")

    return None







def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        # Add only the movie name to this list
        recommended_movies.append(movies.iloc[i[0]].title)

        # Add only the poster URL to this list
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
    )




if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.write(name)

            if poster:
                st.image(poster, width=150)
            else:
                st.caption("Poster unavailable")


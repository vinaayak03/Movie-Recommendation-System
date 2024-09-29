import streamlit as st
import pickle
import requests

# Load models
movie_recom_model = pickle.load(open("movies_list.pkl", 'rb'))
movie_similarity_model = pickle.load(open("similarity.pkl", 'rb'))

# API Key for TMDb (replace 'your_api_key' with your actual key)
api_key = '5728e92ef95125340d0317186271dfb1'

# Get movie list
movies_list = movie_recom_model['title'].values

# Streamlit app
st.header("Movie Recommendation System")
select_value = st.selectbox('Select Movie from below', movies_list)

def fetch_poster(movie_title):
    """
    Fetch movie poster URL from TMDb API using the movie title.
    """
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    
    # Check if the movie was found and return the poster path
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_poster_url
    else:
        return None

def recommend(movie):
    """
    Recommends Movies Based on the input of the user
    """
    try:
        # Match movie title case-insensitively and remove extra spaces
        index = movie_recom_model[movie_recom_model['title'].str.strip().str.lower() == movie.strip().lower()].index[0]
        recom_sys = sorted(list(enumerate(movie_similarity_model[index])), reverse=True, key=lambda vector: vector[1])
        
        # Get top 5 recommended movies
        recommended_movie = []
        recommended_movie_posters = []
        
        for i in recom_sys[1:6]:  # Start from 1 to skip recommending the same movie
            movie_title = movie_recom_model.iloc[i[0]].title
            recommended_movie.append(movie_title)
            poster_url = fetch_poster(movie_title)
            recommended_movie_posters.append(poster_url)
        
        return recommended_movie, recommended_movie_posters
    except IndexError:
        st.error(f"Movie '{movie}' not found.")
        return [], []

if st.button('Show Recommend'):
    recom_movie, recom_posters = recommend(select_value)
    
    if recom_movie:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(recom_movie[0])
            if recom_posters[0]:
                st.image(recom_posters[0])
        
        with col2:
            st.text(recom_movie[1])
            if recom_posters[1]:
                st.image(recom_posters[1])
        
        with col3:
            st.text(recom_movie[2])
            if recom_posters[2]:
                st.image(recom_posters[2])
        
        with col4:
            st.text(recom_movie[3])
            if recom_posters[3]:
                st.image(recom_posters[3])
        
        with col5:
            st.text(recom_movie[4])
            if recom_posters[4]:
                st.image(recom_posters[4])

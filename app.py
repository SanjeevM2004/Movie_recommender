import streamlit as st
import pickle
import requests
from fuzzywuzzy import process
import os

repo_owner = 'SanjeevM2004'
repo_name = 'Movie_recommender'
release_tag = 'Similaritymodel'
movie_list_url = f'https://github.com/{repo_owner}/{repo_name}/releases/download/{release_tag}/movie_list.pkl'
similarity_url = f'https://github.com/{repo_owner}/{repo_name}/releases/download/{release_tag}/similarity.pkl'

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Download files from GitHub release
if not os.path.exists('movie_list.pkl'):
    download_file(movie_list_url, 'movie_list.pkl')
if not os.path.exists('similarity.pkl'):
    download_file(similarity_url, 'similarity.pkl')

# Load the models
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# OMDb API settings
api_key = '31b1fb0d'
base_url = 'http://www.omdbapi.com/'

def get_movie_poster(title):
    url = f"{base_url}?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    return None

def recommend(movie):
    # Use fuzzy matching to find the closest match
    closest_match = process.extractOne(movie, movie_list['title'])[0]
    index = movie_list[movie_list['title'] == closest_match].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_title = movie_list.iloc[i[0]].title
        movie_poster = get_movie_poster(movie_title)
        recommended_movies.append((movie_title, movie_poster))
    return recommended_movies

# Custom CSS for background and image styling
st.markdown(
    """
    <style>
    .whites {
        color: white;
    }
    """,
    unsafe_allow_html=True
)
import streamlit as st

# Include custom CSS to style the button
st.markdown(
    """
    <style>
    .red-button {
        background-color: white;
        color: red;
        border: red;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
  .stApp{
    background-image: url("https://cdn.hashnode.com/res/hashnode/image/upload/v1618683315311/KuMns646J.png?w=1600&h=840&fit=crop&crop=entropy&auto=compress,format&format=webp");
    background-size: cover; /* Stretch image to fill the entire viewport */
    color: white;
  }
  
  .row {
    display: flex;
    flex-wrap: wrap; /* Ensure items wrap to next line */
    justify-content: space-around;
    margin: 0px 10px;
  }

  .movie {
    display: flex;
    background-color: #fff;
    text-align: center;
    position: relative;
    width: 200px; /* Adjust width as needed */
    margin: 10px;
  }

  .movie img {
    border: 5px solid white; /* Add a thick white border */
    width: 100%;
    height: auto;
  }

  .movie-title {
    font-size: 40px;
    font-weight: bold;
    margin: 30px 0;
    padding: 20px 50px;
    text-align: center;
  }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="whites">Movie Recommender System</h1>', unsafe_allow_html=True)

selected_movie = st.text_input('Type the name of a movie:', '')

if st.markdown('<button class="red-button">Recommend</button>', unsafe_allow_html=True):
  if selected_movie:
    recommendations = recommend(selected_movie)
    if recommendations:
      st.markdown("<div class='row'>", unsafe_allow_html=True)
      for movie_title, movie_poster in recommendations:
        st.markdown(f"""
        <div class='movie'>
          <img src='{movie_poster}' alt='Poster'>
          <div class='movie-title'>{movie_title}</div>
        </div>
        """, unsafe_allow_html=True)
      # Close the row div after all recommendations are displayed
      st.markdown("</div>", unsafe_allow_html=True)
    else:
      st.write("No recommendations found.")
  else:
    st.write("Please enter a movie name.")

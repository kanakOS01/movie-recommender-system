import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommendation System", page_icon="🎬", layout="wide"
)

st.title("Movie Recommendation System")

df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def get_poster(id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{id}?api_key=f886f2c752b0a89a87b5dac5f65dc386"
    )
    data = response.json()
    poster = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return poster


def recommend(movie):
    res = []
    posters = []

    idx = df[df["title"] == movie].index[0]
    distances = similarity[idx]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]
    print(res)
    for i in movies_list:
        id = df.iloc[i[0]].id
        res.append(df.iloc[i[0]].title)
        posters.append(get_poster(id))

    return res, posters

option = st.selectbox(
    "Select the movie you would like to get recommendations for",
    df["title"].values,
    index=None,
    placeholder="Select movie",
)

if st.button("Recommend", type="primary"):
    recommendations = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommendations[1][0])
        st.subheader(recommendations[0][0])

    with col2:
        st.image(recommendations[1][1])
        st.subheader(recommendations[0][1])

    with col3:
        st.image(recommendations[1][2])
        st.subheader(recommendations[0][2])

    with col4:
        st.image(recommendations[1][3])
        st.subheader(recommendations[0][3])

    with col5:
        st.image(recommendations[1][4])
        st.subheader(recommendations[0][4])

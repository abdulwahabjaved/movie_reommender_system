import streamlit as st
import pickle
import pandas as pd
import requests
import os
# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="CineVault",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# LOAD DATA
# ----------------------------

BASE_DIR = os.path.dirname(__file__)

movies = pickle.load(open(os.path.join(BASE_DIR, 'movies.pkl'), 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----------------------------
# TMDB API FUNCTION
# ----------------------------
API_KEY = "65ce2fc6a88dbc6c07ff44452c56dd64"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750/1a1a2e/E50914?text=No+Image"

# ----------------------------
# RECOMMEND FUNCTION
# ----------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# ----------------------------
# GLOBAL CSS
# ----------------------------
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* ── Reset & base ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e8e8 !important;
  }

  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(ellipse 80% 40% at 50% -10%, rgba(229,9,20,0.18) 0%, transparent 70%),
      radial-gradient(ellipse 60% 30% at 80% 110%, rgba(229,9,20,0.08) 0%, transparent 60%),
      #0a0a0f !important;
  }

  [data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stSidebar"] { background: #0d0d14 !important; }
  .block-container { padding: 0 2rem 4rem !important; max-width: 100% !important; }

  * { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: #111; }
  ::-webkit-scrollbar-thumb { background: #E50914; border-radius: 4px; }

  /* ── NAVBAR ── */
  .navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.4rem 2rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(10,10,15,0.92);
    backdrop-filter: blur(12px);
  }

  .navbar-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, #E50914 0%, #ff6b35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    user-select: none;
  }

  .navbar-tagline {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 500;
    margin-top: 0.15rem;
  }

  .navbar-right {
    display: flex;
    gap: 1.6rem;
    align-items: center;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.55);
    font-weight: 500;
    letter-spacing: 0.02em;
  }

  .navbar-right span {
    cursor: pointer;
    transition: color 0.2s;
  }
  .navbar-right span:hover { color: #fff; }
  .navbar-right .active { color: #E50914; }

  /* ── HERO SEARCH ── */
  .hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
  }
  .hero-eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #E50914;
    font-weight: 600;
    margin-bottom: 0.8rem;
  }
  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    letter-spacing: 0.05em;
    color: #fff;
    line-height: 0.95;
    margin-bottom: 0.5rem;
  }
  .hero-title span {
    background: linear-gradient(135deg, #E50914 0%, #ff6b35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.4);
    margin-bottom: 2.5rem;
    font-weight: 300;
    letter-spacing: 0.02em;
  }

  /* ── SEARCH INPUT ── */
  [data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 50px !important;
    color: #fff !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s, background 0.2s !important;
    caret-color: #E50914;
  }
  [data-testid="stTextInput"] input::placeholder { color: rgba(255,255,255,0.3) !important; }
  [data-testid="stTextInput"] input:focus {
    border-color: #E50914 !important;
    background: rgba(229,9,20,0.07) !important;
    box-shadow: 0 0 0 3px rgba(229,9,20,0.15) !important;
    outline: none !important;
  }
  [data-testid="stTextInput"] label { display: none !important; }
  [data-testid="stTextInput"] > div { border: none !important; background: transparent !important; }

  /* ── SELECTBOX ── */
  [data-testid="stSelectbox"] > label { 
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
  }
  [data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #fff !important;
  }
  [data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #E50914 !important;
    box-shadow: 0 0 0 3px rgba(229,9,20,0.15) !important;
  }

  /* ── BUTTON ── */
  [data-testid="stButton"] button {
    background: linear-gradient(135deg, #E50914 0%, #c40812 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 2rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 20px rgba(229,9,20,0.35) !important;
  }
  [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(229,9,20,0.5) !important;
  }
  [data-testid="stButton"] button:active { transform: translateY(0px) !important; }

  /* ── SECTION HEADERS ── */
  .section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.5rem 0 1.2rem;
    padding-left: 0.25rem;
  }
  .section-header .accent-bar {
    width: 4px;
    height: 1.5rem;
    background: linear-gradient(180deg, #E50914, #ff6b35);
    border-radius: 2px;
    flex-shrink: 0;
  }
  .section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.06em;
    color: #fff;
  }
  .section-count {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.3);
    font-weight: 500;
    letter-spacing: 0.05em;
    margin-left: auto;
    text-transform: uppercase;
  }

  /* ── MOVIE CARD ── */
  .movie-card {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #13131a;
    transition: transform 0.25s cubic-bezier(.4,0,.2,1), box-shadow 0.25s;
    cursor: pointer;
    group: card;
  }
  .movie-card:hover {
    transform: scale(1.05) translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.7), 0 0 0 1.5px rgba(229,9,20,0.4);
    z-index: 10;
  }
  .movie-card img {
    width: 100%;
    display: block;
    border-radius: 10px 10px 0 0;
    aspect-ratio: 2/3;
    object-fit: cover;
  }
  .movie-card-info {
    padding: 0.65rem 0.75rem 0.75rem;
    background: linear-gradient(180deg, #13131a 0%, #0d0d14 100%);
    border-radius: 0 0 10px 10px;
  }
  .movie-card-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #e8e8e8;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    letter-spacing: 0.01em;
    line-height: 1.3;
  }
  .movie-card-badge {
    display: inline-block;
    margin-top: 0.3rem;
    font-size: 0.65rem;
    color: #E50914;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── RECOMMENDED CARD ── */
  .rec-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: #13131a;
    transition: transform 0.25s cubic-bezier(.4,0,.2,1), box-shadow 0.25s;
    cursor: pointer;
    border: 1.5px solid rgba(229,9,20,0.2);
  }
  .rec-card:hover {
    transform: scale(1.06) translateY(-5px);
    box-shadow: 0 20px 50px rgba(229,9,20,0.25), 0 0 0 2px rgba(229,9,20,0.5);
  }
  .rec-card img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
  }
  .rec-number {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    background: #E50914;
    color: #fff;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 0.02em;
    box-shadow: 0 2px 10px rgba(229,9,20,0.6);
    z-index: 2;
  }
  .rec-card-info {
    padding: 0.7rem 0.8rem 0.8rem;
    background: linear-gradient(180deg, #16161f 0%, #0d0d14 100%);
  }
  .rec-card-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    letter-spacing: 0.01em;
  }
  .rec-card-label {
    font-size: 0.65rem;
    color: rgba(229,9,20,0.8);
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem;
  }

  /* ── DIVIDER ── */
  .cinema-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(229,9,20,0.3), rgba(255,255,255,0.08), transparent);
    margin: 2rem 0;
  }

  /* ── EMPTY STATE ── */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: rgba(255,255,255,0.2);
    font-size: 0.9rem;
    letter-spacing: 0.05em;
  }
  .empty-state .icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.4; }

  /* ── FOOTER ── */
  .footer {
    text-align: center;
    padding: 2.5rem 1rem;
    margin-top: 4rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-size: 0.75rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.05em;
  }
  .footer span { color: #E50914; }

  /* ── SPINNER ── */
  [data-testid="stSpinner"] { color: #E50914 !important; }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
  [data-testid="stDecoration"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# NAVBAR
# ----------------------------
st.markdown("""
<div class="navbar">
  <div>
    <div class="navbar-logo">CineVault</div>
    <div class="navbar-tagline">Discover · Explore · Recommend</div>
  </div>
  <div class="navbar-right">
    <span class="active">Home</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# HERO + SEARCH
# ----------------------------
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Powered by AI Recommendations</div>
  <div class="hero-title">Your Next Favorite<br><span>Film Awaits</span></div>
  <div class="hero-sub">Search any movie — we'll find what to watch next</div>
</div>
""", unsafe_allow_html=True)

_, center_col, _ = st.columns([1, 2.5, 1])
with center_col:
    search_query = st.text_input("search", placeholder="🔍  Search movies, genres, directors...", label_visibility="collapsed")

st.markdown("<div class='cinema-divider'></div>", unsafe_allow_html=True)

# ----------------------------
# FILTERED MOVIE LIST
# ----------------------------
all_titles = movies['title'].values
if search_query:
    filtered_titles = [t for t in all_titles if search_query.lower() in t.lower()]
else:
    filtered_titles = list(all_titles)

# ----------------------------
# MOVIE SELECTION + RECOMMEND
# ----------------------------
_, center_col2, _ = st.columns([1, 2.5, 1])
with center_col2:
    selected_movie = st.selectbox(
        "Choose a movie to get recommendations",
        filtered_titles if filtered_titles else all_titles
    )
    recommend_clicked = st.button("✦ Recommend", use_container_width=True)

# ----------------------------
# RECOMMENDATIONS SECTION
# ----------------------------
if recommend_clicked and selected_movie:
    with st.spinner("Finding your next obsession..."):
        names, posters = recommend(selected_movie)

    st.markdown(f"""
    <div class="section-header">
      <div class="accent-bar"></div>
      <div class="section-title">Because You Liked &nbsp;<span style="color:#E50914">{selected_movie}</span></div>
      <div class="section-count">5 Picks</div>
    </div>
    """, unsafe_allow_html=True)

    rec_cols = st.columns(5, gap="medium")
    for i, col in enumerate(rec_cols):
        with col:
            st.markdown(f"""
            <div class="rec-card">
              <div class="rec-number">{i+1}</div>
              <img src="{posters[i]}" alt="{names[i]}" loading="lazy"/>
              <div class="rec-card-info">
                <div class="rec-card-title">{names[i]}</div>
                <div class="rec-card-label">Recommended</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='cinema-divider'></div>", unsafe_allow_html=True)

# ----------------------------
# TRENDING / BROWSE ROW
# ----------------------------
browse_label = f"Search Results — &quot;{search_query}&quot;" if search_query else "All Movies"
count_label = f"{len(filtered_titles)} Titles" if filtered_titles else ""

st.markdown(f"""
<div class="section-header">
  <div class="accent-bar"></div>
  <div class="section-title">{browse_label}</div>
  <div class="section-count">{count_label}</div>
</div>
""", unsafe_allow_html=True)

display_titles = filtered_titles[:18] if filtered_titles else []

if display_titles:
    rows = [display_titles[i:i+6] for i in range(0, min(len(display_titles), 18), 6)]
    for row_titles in rows:
        cols = st.columns(len(row_titles), gap="medium")
        for col, title in zip(cols, row_titles):
            with col:
                row_movie = movies[movies['title'] == title].iloc[0]
                poster_url = fetch_poster(row_movie['movie_id'])
                st.markdown(f"""
                <div class="movie-card">
                  <img src="{poster_url}" alt="{title}" loading="lazy"/>
                  <div class="movie-card-info">
                    <div class="movie-card-title">{title}</div>
                    <div class="movie-card-badge">▶ Watch</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
      <div class="icon">🎬</div>
      No movies found for your search.
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("""
<div class='cinema-divider'></div>
<div class='footer'>
  © 2025 <span>CineVault</span> &nbsp;·&nbsp; Powered by TMDB &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
🎬 Movie Recommender System

A content-based movie recommendation system built using Python, Machine Learning, and Streamlit. It suggests similar movies based on genres, keywords, cast, crew, and overview, and displays results in a Netflix-style UI with posters fetched from TMDB API.

🚀 Live Demo

(Add your deployed Streamlit link here)

https://your-app-name.streamlit.app
📌 Features
🎥 Movie recommendation based on similarity
🔍 Search functionality (type & filter movies)
🧠 Content-based filtering using NLP
📊 Cosine similarity for recommendations
🖼️ Movie posters using TMDB API
🎨 Netflix-style Streamlit UI
⚡ Fast and lightweight
🛠️ Tech Stack
Python 🐍
Pandas & NumPy
Scikit-learn (CountVectorizer, Cosine Similarity)
Streamlit (Frontend UI)
TMDB API (Movie posters)
Pickle (Model storage)
📂 Project Structure
movie-recommender/
│
├── app.py                  # Streamlit UI
├── main.py / model.py      # Data preprocessing & model training
├── movies.pkl             # Processed dataset
├── similarity.pkl         # Similarity matrix
├── tmdb_5000_movies.csv   # Dataset
├── tmdb_5000_credits.csv  # Dataset
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
⚙️ How It Works
Combine movie features:
Genres
Keywords
Cast
Crew
Overview
Convert text into vectors using CountVectorizer
Compute similarity using Cosine Similarity
Recommend top 5 most similar movies
Fetch posters using TMDB API
▶️ Installation & Setup
1. Clone repository
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
2. Install dependencies
pip install -r requirements.txt
3. Run Streamlit app
streamlit run app.py
🔑 TMDB API Setup
Get API key from: https://www.themoviedb.org/
Replace in app.py:
API_KEY = "YOUR_API_KEY"
🎯 Example

Input:

Avatar

Output:

1. Guardians of the Galaxy
2. John Carter
3. Avengers
4. Thor
5. Star Trek
## 🖼️ Home Page Preview

![Home Page](cine1.png)

Home Page
Search Feature
Recommendations with Posters
📈 Future Improvements
⭐ Add movie ratings
🎥 Add trailer previews (YouTube API)
🌐 Deploy on cloud (Streamlit / Render)
🤖 Improve model using TF-IDF or BERT
❤️ Add favorites system
👨‍💻 Author
Abdul Wahab
AI / ML & Web Developer
📜 License

This project is for educational purposes only.

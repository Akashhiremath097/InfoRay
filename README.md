Inforay – Intelligent AI-Powered News Aggregator

An end-to-end intelligent news aggregation platform that fetches global news, cleans data, classifies categories using ML, enriches it with AI-generated summaries, resolves images, performs sentiment detection, caches thumbnails, and finally serves a beautiful futuristic UI.


🌍 Project Overview
Inforay automates the entire news processing pipeline:

1️⃣ Fetching Layer (Data Fetcher)
Pulls live RSS feeds from multiple global sources
Stores raw articles in MongoDB
Handles failed fetches, invalid XML, or duplicated content

2️⃣ Cleaning & Transformation
Located in data_fetcher/clean_data.py
Removes junk text
Normalizes titles and summaries
Removes duplicates
Performs AI-assisted cleaning for missing or broken data

3️⃣ AI Processing Pipeline
Located in ai_processing/

Each module handles one major enrichment step:
Module	                            Function
category_classifier.py	            ML-based topic prediction
sentiment_analyzer.py	              Positive/Neutral/Negative classification
summarizer.py	                      Generates 2–3 line summaries
image_resolver.py	                  Resolves thumbnails, generates fallbacks, caches locally

After processing, the enriched articles are stored back in MongoDB.
4️⃣ Automated Schedulers
Located in automation/
scheduler.py         → Runs the pipeline every X minutes
db_maintenance.py    → Purges old data
log_cleanup.py       → Maintains clean logs

5️⃣ Web App (Frontend + API)
Located in web_app/
Beautiful futuristic UI
Dark/light mode
AI-powered search
Infinite scroll
Trending topics
Category filtering
Article viewer modal
API built with Flask, static frontend with HTML/CSS/JS.

📁 Directory Structure
.
├── ai_processing/
│   ├── ai_processing_pipeline.py
│   ├── category_classifier.py
│   ├── image_resolver.py
│   ├── sentiment_analyzer.py
│   ├── summarizer.py
│   └── models/

│
├── automation/
│   ├── scheduler.py
│   ├── db_maintenance.py
│   ├── log_cleanup.py
│   └── __init__.py
│
├── data_fetcher/
│   ├── fetch_rss.py
│   ├── fetch_news.py
│   ├── clean_data.py
│   ├── config.py
│   ├── db_manager.py
│   └── tests/
│
├── database/
│   ├── mongo_connection.py
│
├── web_app/
│   ├── static/
│   │   ├── script.js
│   │   ├── style.css
│   │   ├── fallbacks/
│   │   └── thumb_cache/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── category.html
│   ├── app.py          ← Flask application
│   ├── routes.py       ← API endpoints
│   └── README.md
│
├── run_pipeline.py      ← Main runner
├── requirements.txt
└── .env

⚙️ Installation & Setup
1️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate    # Mac/Linux
.venv\Scripts\activate       # Windows

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Set Up Environment Variables (.env)
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=inforay
OPENAI_API_KEY=your_key_here

📰 Running the Full System
Option A — Run Everything Manually
STEP 1: Fetch + Clean + AI Process
python run_pipeline.py

STEP 2: Start the Web App
cd web_app
python app.py

Visit:
👉 http://localhost:5000

Option B — Automatic Scheduler
Runs fetching + cleaning + AI processing periodically:
python automation/scheduler.py


🧠 AI Capabilities

✔ Category Classification

ML model predicts:
Technology, Politics, Business, Sports, Health, etc.

✔ Sentiment Analysis
Labels each article as:
Positive, Neutral, Negative
✔ Summarization
2–3 sentence clean summary using a transformer model.
✔ Image Resolution
Fixes broken images
Extracts OpenGraph thumbnails
Generates fallback images
Caches locally to reduce load

🔌 API Endpoints
Fetch All Articles
GET /api/articles

Search
GET /api/search?q=keyword

Categories
GET /api/category/<name>

Single Article
GET /api/article/<id>


🎨 Frontend Features
✔ Futuristic, responsive UI
✔ Infinite scroll
✔ Trending topics
✔ Category chips
✔ Search bar with instant results
✔ Dark & light theme
✔ Image modal view
✔ AI-powered summaries and metadata

🚀 Deployment Guide
Docker Deployment
(If needed later)
docker build -t inforay .
docker run -p 5000:5000 inforay

Cloud Deployment Options
Render
Railway
DigitalOcean
AWS Lightsail
Azure App Service

MongoDB can be hosted on:
MongoDB Atlas
DigitalOcean Managed DB
Local VM

📌 Future Enhancements
User accounts + saved articles
AI topic clustering
Personalized news feed
Real-time event detection
Push notifications

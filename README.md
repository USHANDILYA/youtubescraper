# 📺 YouTube Video Scraper using Streamlit and Youtube API

This Streamlit application allows users to interactively scrape YouTube video data based on search keywords and extract comments from any public YouTube video. It leverages the official **YouTube Data API v3** and offers powerful tools to download and visualize the results.

---

## 🚀 Features

### 🔍 Search-Based Video Scraping
- Search videos by **keywords**, **publish date**, and **custom sort order** (date, views, rating, etc.)
- Fetches **up to 50 videos** per keyword.
- Displays key video details:
  - Title
  - Description
  - Channel Name
  - Publish Date
  - View Count
  - Like Count
  - Comment Count
  - Thumbnail and Direct URL
- Identifies the **most viewed video** in the search result.
- Generates a **Word Cloud** from all video titles.
- Provides downloadable **CSV** format of results.

### 💬 Comment Scraping
- Scrapes **top-level comments** for any YouTube video (by video ID).
- Extracts:
  - Author name
  - Comment text
  - Like count
  - Publish timestamp
- Download all comments in **CSV** format.

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/USHANDILYA/youtubescraper.git
cd youtube-video-scraper
### 2. Install Python Packages
Make sure Python 3.7+ is installed. Then run:

```bash
pip install -r requirements.txt
Or install manually:

```bash
pip install streamlit pandas matplotlib wordcloud google-api-python-client

### 3. Get a YouTube API Key
- Visit Google Cloud Console
- Create a new project
- Enable YouTube Data API v3
- Go to APIs & Services > Credentials
- Click Create API Key

### 4. Save API Key Securely
- Create a file at: .streamlit/secrets.toml
- API_KEY = "your_actual_youtube_api_key"
- ⚠️ DO NOT push this file to GitHub.

### 5. Run the Streamlit App
```bash
streamlit run app.py

## 🖥️ Usage Flow (Step-by-Step)

### Step 1: Search Videos
- Enter search keyword(s)
- Choose optional start/end date (YYYY-MM-DD)
- Choose sorting (e.g., by view count)
- Click Submit

### Step 2: View Results
- App displays table with all matching videos
- Scroll through:
- Titles
- Views
- Likes
- Links
- Published dates, etc.

### Step 3: View Most Viewed Video
- App automatically shows the most viewed video and its stats

### Step 4: View Word Cloud
- A word cloud is shown based on all video titles

### Step 5: Download Video CSV
- Click Download CSV to save video data locally

### Step 6: Scrape Comments
- Scroll to "Comment Scraper" section
- Enter Video ID (e.g., dQw4w9WgXcQ)
- Click Submit

### Step 7: View Comments
- Comments will appear in a structured table:
- Author
- Text
- Likes
- Publish Date

### Step 8: Download Comment CSV
- Click Download CSV to export all comments

## 🧩 Dependencies
- streamlit
- pandas
- matplotlib
- wordcloud
- google-api-python-client

## ✅ Pros
- Clean UI with Streamlit
- Uses official YouTube API
- Quick CSV export
- Can run locally or deploy online
- Visual word cloud and summary features

## ❌ Limitations
- Only 50 videos per search due to API limits
- Only top-level comments (no replies)
- YouTube API has a daily quota (default: 10,000 units)
- Requires manual input of Video ID for comment scraping

## ⚠️ Notes to Remember
- Video ID = part after v= in a YouTube link
- Example:
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
ID: dQw4w9WgXcQ

- API key must be kept secret in .streamlit/secrets.toml

- If comment scraping fails, ensure:
  - Video is public
  - Comments are enabled
  - Correct Video ID is entered

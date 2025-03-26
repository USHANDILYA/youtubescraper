import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyBW1IeX2PoLEvgWvz1JLVM9LlFoZQFHvjw"

def search_videos(query, api_key=API_KEY, max_results=50, published_after=None, published_before=None):
    youtube = build("youtube", "v3", developerKey=api_key)
    search_request = youtube.search().list(
        part="id,snippet",
        q=query,
        type="video",
        maxResults=max_results,
        publishedAfter=published_after,
        publishedBefore=published_before
    )
    search_response = search_request.execute()
    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
    return video_ids

def get_video_details(video_ids, api_key=API_KEY):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()
    
    video_details = []
    for video in response.get("items", []):
        snippet = video["snippet"]
        stats = video.get("statistics", {})
        details = {
            "Title": snippet["title"],
            "Channel": snippet["channelTitle"],
            "Published Date": snippet["publishedAt"],
            "Views": stats.get("viewCount", "N/A"),
            "Likes": stats.get("likeCount", "N/A"),
            "Comments": stats.get("commentCount", "N/A"),
            "Video URL": f"https://www.youtube.com/watch?v={video['id']}"
        }
        video_details.append(details)
    return video_details

def main():
    st.title("YouTube Video Scraper")
    query = st.text_input("Enter search keyword")
    published_after = st.text_input("Published After (YYYY-MM-DD)")
    published_before = st.text_input("Published Before (YYYY-MM-DD)")
    
    if st.button("Search") and query:
        published_after += "T00:00:00Z" if published_after else None
        published_before += "T23:59:59Z" if published_before else None
        
        video_ids = search_videos(query, API_KEY, 50, published_after, published_before)
        details = get_video_details(video_ids, API_KEY)
        
        if details:
            df = pd.DataFrame(details)
            st.dataframe(df)
            
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "youtube_videos.csv", "text/csv")
        else:
            st.write("No videos found.")

if __name__ == "__main__":
    main()
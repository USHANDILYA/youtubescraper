# import streamlit as st
# import pandas as pd
# from googleapiclient.discovery import build

# API_KEY = st.secrets["API_KEY"]

# def search_videos(query, api_key=API_KEY, max_results=50, published_after=None, published_before=None):
#     youtube = build("youtube", "v3", developerKey=api_key)
#     search_request = youtube.search().list(
#         part="id,snippet",
#         q=query,
#         type="video",
#         maxResults=max_results,
#         publishedAfter=published_after,
#         publishedBefore=published_before
#     )
#     search_response = search_request.execute()
#     video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
#     return video_ids

# def get_video_details(video_ids, api_key=API_KEY):
#     youtube = build("youtube", "v3", developerKey=api_key)
#     request = youtube.videos().list(
#         part="snippet,statistics",
#         id=",".join(video_ids)
#     )
#     response = request.execute()
    
#     video_details = []
#     for video in response.get("items", []):
#         snippet = video["snippet"]
#         stats = video.get("statistics", {})
#         details = {
#             "Title": snippet["title"],
#             "Channel": snippet["channelTitle"],
#             "Published Date": snippet["publishedAt"],
#             "Views": stats.get("viewCount", "N/A"),
#             "Likes": stats.get("likeCount", "N/A"),
#             "Comments": stats.get("commentCount", "N/A"),
#             "Video URL": f"https://www.youtube.com/watch?v={video['id']}"
#         }
#         video_details.append(details)
#     return video_details

# def main():
#     st.title("YouTube Video Scraper")
#     query = st.text_input("Enter search keyword")
#     published_after = st.text_input("Published After (YYYY-MM-DD)")
#     published_before = st.text_input("Published Before (YYYY-MM-DD)")
    
#     if st.button("Search") and query:
#         published_after += "T00:00:00Z" if published_after else None
#         published_before += "T23:59:59Z" if published_before else None
        
#         video_ids = search_videos(query, API_KEY, 50, published_after, published_before)
#         details = get_video_details(video_ids, API_KEY)
        
#         if details:
#             df = pd.DataFrame(details)
#             st.dataframe(df)
            
#             csv = df.to_csv(index=False).encode("utf-8")
#             st.download_button("Download CSV", csv, "youtube_videos.csv", "text/csv")
#         else:
#             st.write("No videos found.")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# from googleapiclient.discovery import build
# #from io import BytesIO

# API_KEY = st.secrets["API_KEY"]

# def search_videos(query, api_key=API_KEY, max_results=50, published_after=None, published_before=None, order="relevance"):
#     youtube = build("youtube", "v3", developerKey=api_key)
#     search_request = youtube.search().list(
#         part="id,snippet",
#         q=query,
#         type="video",
#         maxResults=max_results,
#         publishedAfter=published_after,
#         publishedBefore=published_before,
#         order=order
#     )
#     search_response = search_request.execute()
#     video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
#     return video_ids

# def get_video_details(video_ids, api_key=API_KEY):
#     youtube = build("youtube", "v3", developerKey=api_key)
#     request = youtube.videos().list(
#         part="snippet,statistics",
#         id=",".join(video_ids)
#     )
#     response = request.execute()
    
#     video_details = []
#     for video in response.get("items", []):
#         snippet = video["snippet"]
#         stats = video.get("statistics", {})
#         details = {
#             "Title": snippet["title"],
#             "Description": snippet["description"],
#             "Channel": snippet["channelTitle"],
#             "Published Date": snippet["publishedAt"],
#             "Views": stats.get("viewCount", "N/A"),
#             "Likes": stats.get("likeCount", "N/A"),
#             "Comments": stats.get("commentCount", "N/A"),
#             "Video URL": f"https://www.youtube.com/watch?v={video['id']}",
#             "Thumbnail": snippet["thumbnails"]["medium"]["url"]
#         }
#         video_details.append(details)
#     return video_details

# def generate_wordcloud(video_titles):
#     text = " ".join(video_titles)
#     wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     st.pyplot(plt)

# def main():
#     st.title("YouTube Video Scraper Dashboard")
    
#     with st.sidebar:
#         query = st.text_input("Enter search keywords (comma-separated)")
#         published_after = st.text_input("Published After (YYYY-MM-DD)")
#         published_before = st.text_input("Published Before (YYYY-MM-DD)")
#         order = st.selectbox("Sort by", ["relevance", "date", "rating", "viewCount", "title"], index=0)
    
#     if st.button("Search") and query:
#         published_after = published_after + "T00:00:00Z" if published_after else None
#         published_before = published_before + "T23:59:59Z" if published_before else None
        
#         all_details = []
#         for keyword in query.split(","):
#             keyword = keyword.strip()
#             if keyword:
#                 video_ids = search_videos(keyword, API_KEY, 50, published_after, published_before, order)
#                 details = get_video_details(video_ids, API_KEY)
#                 all_details.extend(details)
        
#         if all_details:
#             df = pd.DataFrame(all_details)
#             st.dataframe(df.drop(columns=["Thumbnail"]))
            
#             # Horizontal thumbnail scroller
#             st.subheader("Video Thumbnails")
#             thumbnails_html = """<div style='display: flex; overflow-x: auto; white-space: nowrap;'>"""
#             for _, row in df.iterrows():
#                 thumbnails_html += f"""<div style='margin: 5px;'>
#                 <a href='{row['Video URL']}' target='_blank'>
#                 <img src='{row['Thumbnail']}' width='120' height='80'><br>{row['Title']}
#                 </a></div>"""
#             thumbnails_html += "</div>"
#             st.markdown(thumbnails_html, unsafe_allow_html=True)
            
#             # Summary metrics
#             st.subheader("Summary")
#             st.write(f"Total Videos Found: {len(df)}")
#             if "Views" in df.columns and df["Views"].dtype == "object":
#                 df["Views"] = pd.to_numeric(df["Views"], errors='coerce')
#             most_viewed = df.loc[df["Views"].idxmax()] if "Views" in df.columns else None
#             st.write(f"Most Viewed Video: [{most_viewed['Title']}]({most_viewed['Video URL']}) with {most_viewed['Views']} views")
            
#             # Word Cloud
#             st.subheader("Word Cloud of Video Titles")
#             generate_wordcloud(df["Title"].tolist())
            
#             # Download options
#             csv = df.to_csv(index=False).encode("utf-8")
#             # excel_buffer = BytesIO()
#             # df.to_excel(excel_buffer, index=False, engine="openpyxl")
#             # excel_buffer.seek(0)
            
#             st.download_button("Download CSV", csv, "youtube_videos.csv", "text/csv")
#             #st.download_button("Download Excel", excel_buffer, "youtube_videos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#         else:
#             st.write("No videos found.")

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from googleapiclient.discovery import build
#from io import BytesIO

API_KEY = "AIzaSyBW1IeX2PoLEvgWvz1JLVM9LlFoZQFHvjw"

def search_videos(query, api_key=API_KEY, max_results=50, published_after=None, published_before=None, order="relevance"):
    youtube = build("youtube", "v3", developerKey=api_key)
    search_request = youtube.search().list(
        part="id,snippet",
        q=query,
        type="video",
        maxResults=max_results,
        publishedAfter=published_after,
        publishedBefore=published_before,
        order=order
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
            "Description": snippet["description"],
            "Channel": snippet["channelTitle"],
            "Published Date": snippet["publishedAt"],
            "Views": stats.get("viewCount", "N/A"),
            "Likes": stats.get("likeCount", "N/A"),
            "Comments": stats.get("commentCount", "N/A"),
            "Video URL": f"https://www.youtube.com/watch?v={video['id']}",
            "Thumbnail": snippet["thumbnails"]["default"]["url"]
        }
        video_details.append(details)
    return video_details

def generate_wordcloud(video_titles):
    text = " ".join(video_titles)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

def get_comments(video_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "Author": comment["authorDisplayName"],
                "Comment": comment["textDisplay"],
                "Likes": comment["likeCount"],
                "Published At": comment["publishedAt"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments

def main():
    st.title("YouTube Video Scraper")
    mode = st.radio("Select Mode", ["Search-Based Video Scraping", "Comment Scraping"])

    if mode == "Search-Based Video Scraping":
        with st.sidebar:
            query = st.text_input("Enter search keywords (comma-separated)")
            published_after = st.text_input("Published After (YYYY-MM-DD)")
            published_before = st.text_input("Published Before (YYYY-MM-DD)")
            order = st.selectbox("Sort by", ["relevance", "date", "rating", "viewCount", "title"], index=0)

        if st.button("Search") and query:
            published_after += "T00:00:00Z" if published_after else None
            published_before += "T23:59:59Z" if published_before else None

            all_details = []
            for keyword in query.split(","):
                keyword = keyword.strip()
                if keyword:
                    video_ids = search_videos(keyword, API_KEY, 50, published_after, published_before, order)
                    details = get_video_details(video_ids, API_KEY)
                    all_details.extend(details)

            if all_details:
                df = pd.DataFrame(all_details)
                st.dataframe(df.drop(columns=["Thumbnail"]))

                st.subheader("Video Thumbnails")
                thumbnails = "".join([
                    f'<a href="{row["Video URL"]}" target="_blank"><img src="{row["Thumbnail"]}" style="margin: 5px; height: 100px;"></a>'
                    for _, row in df.iterrows()
                ])
                st.markdown(f"<div style='white-space: nowrap; overflow-x: auto'>{thumbnails}</div>", unsafe_allow_html=True)

                st.subheader("Summary")
                st.write(f"Total Videos Found: {len(df)}")
                df["Views"] = pd.to_numeric(df["Views"], errors='coerce')
                most_viewed = df.loc[df["Views"].idxmax()]
                st.write(f"Most Viewed Video: [{most_viewed['Title']}]({most_viewed['Video URL']}) with {most_viewed['Views']} views")

                st.subheader("Word Cloud of Video Titles")
                generate_wordcloud(df["Title"].tolist())

                csv = df.to_csv(index=False).encode("utf-8")
                # excel_buffer = BytesIO()
                # df.to_excel(excel_buffer, index=False, engine="openpyxl")
                # excel_buffer.seek(0)

                st.download_button("Download CSV", csv, "youtube_videos.csv", "text/csv")
                #st.download_button("Download Excel", excel_buffer, "youtube_videos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.write("No videos found.")

    elif mode == "Comment Scraping":
        video_id = st.text_input("Enter YouTube Video ID for Comment Scraping")
        if st.button("Fetch Comments") and video_id:
            comments = get_comments(video_id, API_KEY)
            if comments:
                df_comments = pd.DataFrame(comments)
                st.dataframe(df_comments)

                csv = df_comments.to_csv(index=False).encode("utf-8")
                # excel_buffer = BytesIO()
                # df_comments.to_excel(excel_buffer, index=False, engine="openpyxl")
                # excel_buffer.seek(0)

                st.download_button("Download Comments CSV", csv, "youtube_comments.csv", "text/csv")
                #st.download_button("Download Comments Excel", excel_buffer, "youtube_comments.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.write("No comments found.")

if __name__ == "__main__":
    main()

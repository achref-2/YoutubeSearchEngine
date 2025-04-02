from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Replace with your actual YouTube API key
YOUTUBE_API_KEY = "*****"

# YouTube API Endpoints
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_STATS_URL = "https://www.googleapis.com/youtube/v3/videos"

def get_youtube_video_stats(video_id: str):
    """Fetch views & likes for a video."""
    params = {"part": "statistics", "id": video_id, "key": YOUTUBE_API_KEY}
    response = requests.get(YOUTUBE_STATS_URL, params=params)
    
    if response.status_code != 200:
        return {"views": 0, "likes": 0}

    stats = response.json().get("items", [{}])[0].get("statistics", {})
    return {
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0))
    }

def search_youtube(query: str):
    """Search for music videos on YouTube."""
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 10
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)

    if response.status_code != 200:
        return []

    items = response.json().get("items", [])
    results = []

    for item in items:
        video_id = item["id"]["videoId"]
        stats = get_youtube_video_stats(video_id)

        results.append(
            {
                "title": item["snippet"]["title"],
                "artist": item["snippet"]["channelTitle"],
                "views": stats["views"],
                "likes": stats["likes"],
                "video_id": video_id,
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "source": "YouTube"
            }
        )

    return results

def rank_results(results):
    """Rank videos based on views and likes."""
    return sorted(results, key=lambda x: (x["views"], x["likes"]), reverse=True)

@app.get("/", response_class=HTMLResponse)
def root():
    # Read the HTML content from the file
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Music Search</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        input { padding: 10px; width: 80%; margin-bottom: 10px; }
        button { padding: 10px; }
        .video { margin-top: 20px; }
    </style>
</head>
<body>

    <h1>YouTube Music Search</h1>
    <input type="text" id="searchQuery" placeholder="Search for music...">
    <button onclick="searchMusic()">Search</button>

    <div id="results"></div>

    <script>
        async function searchMusic() {
            let query = document.getElementById("searchQuery").value;
            if (!query) return alert("Please enter a search term!");

            // Update to use relative URL instead of localhost
            let response = await fetch(`/search?query=${encodeURIComponent(query)}`);
            let data = await response.json();

            let resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";

            data.ranked_results.forEach(video => {
                let videoElement = `
                    <div class="video">
                        <h3>${video.title} - ${video.artist}</h3>
                        <p>Views: ${video.views} | Likes: ${video.likes}</p>
                        <iframe width="300" height="200" src="https://www.youtube.com/embed/${video.video_id}" allowfullscreen></iframe>
                    </div>
                `;
                resultsDiv.innerHTML += videoElement;
            });
        }
    </script>

</body>
</html>
    """
    return html_content

@app.get("/search")
def search_music(query: str = Query(..., title="Music Search Query")):
    youtube_results = search_youtube(query)
    ranked_results = rank_results(youtube_results)
    
    return {"ranked_results": ranked_results}
# YouTube Music Search

A small web app that searches YouTube for music videos, ranks the results by views and likes, and plays them right on the page.

[Live demo](https://searchengine-0w94.onrender.com/) (hosted on Render's free tier, so the first load can take a minute)

## How it works

`script.py` is a FastAPI app with two routes:

| Route | What it does |
| --- | --- |
| `GET /` | Serves the search page (HTML and JavaScript, no framework) |
| `GET /search?query=...` | Searches YouTube for up to 10 videos, fetches views and likes for each one with a second API call, and returns them sorted by views, then likes |

Each result has the title, channel, view and like counts, and a link. The page embeds the selected video in a player.

## Run it locally

You need Python 3.10 or newer and a YouTube Data API v3 key from the Google Cloud console.

```bash
pip install -r requirements.txt
# put your key into YOUTUBE_API_KEY in script.py
uvicorn script:app --reload
# open http://localhost:8000
```

## Files

| File | What it is |
| --- | --- |
| `script.py` | FastAPI backend and the search page |
| `Front.html` | Standalone version of the frontend |
| `requirements.txt` | fastapi, uvicorn, requests |

## Ideas for later

- Read the API key from an environment variable instead of the source file
- Fetch the statistics for all videos in one `videos` request instead of one per video
- Cache popular searches to stay within the API quota

---

Built by Achraf Aroua · [Portfolio](https://achref-2.github.io)

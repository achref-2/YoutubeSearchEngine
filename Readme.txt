# YouTube Music Search

YouTube Music Search is a web application that allows users to search for music videos on YouTube, view their details (title, artist, views, likes), and watch them directly on the page.

---

## Features
- **Search for music videos** using keywords.
- View video details such as:
  - Title
  - Artist
  - Views
  - Likes
- **Watch videos** embedded directly on the page.
- **Ranked results** based on views and likes.

---

## Demo
You can find a live demo of the application here:  
[https://searchengine-0w94.onrender.com/](https://searchengine-0w94.onrender.com/)

---

## How to Run Locally

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)

### Installation
1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Replace the `YOUTUBE_API_KEY` in `script.py` with your YouTube Data API key.

---

### Running the Application
1. Start the FastAPI server:
   ```bash
   uvicorn script:app --reload
   ```
2. Open your browser and navigate to [http://localhost:8000](http://localhost:8000).

---

## File Structure
- `Front.html`: The frontend HTML file for the application.
- `script.py`: The backend FastAPI server handling API requests.
- `requirements.txt`: List of dependencies required for the project.

---

## License
This project is licensed under the MIT License.
# GIF Grid Splitter

A web application that processes animated GIFs by splitting them into a grid of smaller animated GIFs and displays them in a synchronized manner on an HTML page.

## Features

- Upload an animated GIF and split it into a specified grid of smaller GIFs.
- Display the original GIF preview and the split GIFs on the same page.
- Store and retrieve split GIFs using Deta Base HTTP API.

## Technologies Used

- FastAPI
- PIL (Pillow)
- HTMX
- Bootstrap
- Deta Base

## Setup and Installation

1. **Clone the repository**:
   ```sh
   git clone git@github.com:psyk01337/gifsplitter.git
   cd gifsplitter

2. **Create a virtual environment**:
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

3. **Install dependencies**:
pip install -r requirements.txt

4. **Set up environment variables**:
Create a .env file in the root directory and add your Deta project key:
DETA_PROJECT_KEY=your_project_key_here

5. **Run the application**:
uvicorn main:app --reload
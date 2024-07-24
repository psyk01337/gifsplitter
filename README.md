# GIF Grid Splitter

The GIF Grid Splitter web application provides a simple and intuitive interface for splitting GIFs into smaller segments. Users can upload a GIF, specify the number of rows and columns for splitting, and view the resulting segments. The application also offers a toggle to control the gap between the segments.

## Features

- Upload GIF files for processing.
- Split GIFs into specified rows and columns.
- Preview the uploaded GIF before splitting.
- Toggle gaps between the resulting GIF segments.
- Download the source code from the provided link

## Technologies Used

- FastAPI
- HTMX
- Bootstrap
- Deta

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone git@github.com:psyk01337/gifsplitter.git
    cd gifsplitter
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```
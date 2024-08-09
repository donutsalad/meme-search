# Meme Search Project

This project allows you to search through a collection of memes using a backend server and a React frontend. The server generates embeddings for the images and provides a search functionality through a Flask API.

## Requirements

- Python 3.7+
- Node.js and npm

## Setup Instructions

### Windows

1. **Clone the repository**:
    
shell

    git clone <your_repo_url>
    cd your_repo
    
2. **Run the setup script**:
    Double-click `setup.bat` to install all dependencies required for both the Python backend and the React frontend.

3. **Embed your images**:
    Run the `embed.py` script in the terminal after changing `search_string = "/home/isabelle/memes"` to your meme folder.
    
shell

    python embed.py

4. **Start the server and React app**:
    Run the `backend.py` script in the terminal:
    
shell

    python backend.py
    
### Linux

1. **Clone the repository**:
    
shell

    git clone <your_repo_url>
    cd your_repo
    
2. **Run the setup script**:
    Make `setup.sh` executable by running:
    
shell
    
    chmod +x setup.sh
    
Then execute it:
    
shell

    ./setup.sh
    
3. **Embed your images**:
    Run the `embed.py` script in the terminal after changing `search_string = "/home/isabelle/memes"` to your meme folder.
    
shell

    python embed.py

4. **Start the server and React app**:
    Run the `backend.py` script in the terminal:
    
shell

    python backend.py
    
## Usage

### Backend

- The backend server provides a `/search` endpoint to search for memes based on text input.
- Example search request:
    
json

    {
        "query": "boykisser",
        "top_n": 10
    }
    
### React App

- The React app will be started alongside the Flask server and can be accessed in your default web browser at the specified port (default is `http://localhost:3000`).

## License

This project is licensed under the MIT License.

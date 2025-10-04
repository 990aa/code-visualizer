# Code Visualizer

This project is a web-based tool to visualize code and understand its structure and execution flow.

## Project Structure

- `app.py`: The main Flask application that serves the frontend and provides the analysis API.
- `frontend/`: The Vue.js frontend application.
- `utils/`: Contains the Python code for parsing different programming languages and generating visualizations.

## Running the Application

### 1. Backend (Flask)

The backend is a Flask server that handles code analysis.

**Prerequisites:**

- Python 3.x
- `pip`

**Setup:**

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**

    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask server:**

    ```bash
    python app.py
    ```

    The backend will be running at `http://localhost:5000`.

### 2. Frontend (Vue.js)

The frontend is a Vue.js application built with Vite.

**Prerequisites:**

- Node.js and `npm`

**Setup:**

1.  **Navigate to the `frontend` directory:**

    ```bash
    cd frontend
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Build the frontend for production:**

    ```bash
    npm run build
    ```

    This will create a `dist` directory with the compiled frontend assets. The Flask server is configured to serve these files.

4.  **Development:**

    To run the frontend in development mode with hot-reloading:

    ```bash
    npm run dev
    ```

    The development server will be available at `http://localhost:5173`. Note that for the frontend to communicate with the backend, the Flask server must be running.

## How to Use

1.  Make sure both the backend and frontend are set up and running.
2.  Open your browser and navigate to `http://localhost:5000`.
3.  Select a programming language.
4.  Enter your code in the editor or load an example.
5.  Click "Visualize Code" to see the analysis.

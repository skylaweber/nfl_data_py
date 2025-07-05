# NFL Data Visualizer Web Interface

This web application provides a user-friendly interface to search, view, and visualize NFL data using the `nfl_data_py` library.

## Features

-   **Comprehensive Data Searching:**
    *   Select the specific `nfl_data_py` function to call (e.g., `import_pbp_data`, `import_seasonal_data`, `import_ngs_data`).
    *   Dynamically displays relevant input fields based on the selected function, including:
        *   Years (comma-separated list).
        *   Columns to retrieve (comma-separated list, optional for many functions).
        *   Function-specific parameters (e.g., `s_type` for seasonal data, `stat_type` for NGS, boolean flags for PBP data like `include_participation`, `cache`, etc.).
-   **Tabular Data Display:** View search results in a scrollable table.
-   **Data Visualization:**
    *   Generate various types of plots (Scatter, Line, Bar, Histogram, Box Plot) from the search results.
    *   Customize plots by selecting X and Y axes, and an optional grouping variable for colors from the currently loaded data.
-   **Dynamic UI:** The interface dynamically updates parameter forms based on the selected `nfl_data_py` function.
-   **Column Helper:** "Fetch Available Columns" button for Play-by-Play and Weekly data types to guide column selection.

## How to Run

1.  **Prerequisites:**
    *   Python 3.x (Ensure your Python version is compatible with `pandas < 2.0` if using `nfl_data_py` version 0.3.3 or similar, or that you have a compatible environment if `nfl_data_py`'s dependencies change).
    *   pip (Python package installer).

2.  **Installation:**
    *   Clone this repository.
    *   It's highly recommended to use a virtual environment:
        ```bash
        python3 -m venv nfl_viz_env
        source nfl_viz_env/bin/activate  # On Windows: nfl_viz_env\Scripts\activate
        ```
    *   Install the required Python packages:
        ```bash
        pip install Flask pandas plotly nfl_data_py
        ```
        **Note on pandas version:** `nfl_data_py` version 0.3.3 (and potentially others around this version) requires `pandas < 2.0`. If `pip` tries to build `pandas` from source and hangs, you may need to ensure your environment has build tools (`sudo apt-get install build-essential python3-dev` on Debian/Ubuntu) or use a Python version for which pre-built `pandas 1.5.x` wheels are available.

3.  **Running the Application:**
    *   Navigate to the root directory of this project (where `run.py` is located).
    *   Execute the following command in your terminal:
        ```bash
        python run.py
        ```
    *   Open your web browser and go to `http://127.0.0.1:5000/`.

## Using the Interface

1.  **Select Function:** Choose the `nfl_data_py` function you want to use from the "Select Function:" dropdown.
2.  **Fill Parameters:**
    *   The form will dynamically update to show parameters relevant to your selected function.
    *   **Years:** If applicable, provide a comma-separated list of years (e.g., `2022,2023`).
    *   **Columns:** If applicable, provide a comma-separated list of columns. For PBP and Weekly data, you can use the "Fetch Available Columns" button as a helper.
    *   **Function-Specific Parameters:** Fill in any other displayed fields (e.g., dropdowns for season type, stat type; checkboxes for boolean options like "Downcast Floats" or "Include Participation").
3.  **Search Data:** Click the "Search Data" button.
    *   Results will be displayed in a table below the search form.
    *   If there's an error (e.g., no data found, invalid input, missing required parameter), an error message will appear.
4.  **Visualize Data:**
    *   Once data is successfully searched and displayed, the "Create Visualization" form will become available.
    *   **Select Visualization Type:** Choose the type of plot.
    *   **Select X-Axis, Y-Axis, Color By (Optional):** Dropdowns will be populated with columns from your current search results. Choose the appropriate columns for your plot.
    *   **Generate Visualization:** Click "Generate Visualization". The plot will appear at the bottom of the page.

## Project Structure

-   `run.py`: Main Flask application script.
-   `app/`: Directory containing the Flask application.
    -   `__init__.py`: Initializes the Flask app.
    -   `routes.py`: Defines application routes and backend logic.
    -   `templates/`:
        -   `index.html`: The main HTML page and frontend JavaScript logic.
-   `nfl_data_py/`: The `nfl_data_py` library itself (if included directly in the repo).
-   `README_WEB.md`: This file.

## Deployment

This application uses the Flask development server, not suitable for production. For deployment, use a production WSGI server (e.g., Gunicorn, uWSGI) behind a reverse proxy (e.g., Nginx).

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```
Ensure `DEBUG = False` in production, manage static files appropriately, and set up logging/monitoring.

# NFL Data Visualizer Web Interface

This web application provides a user-friendly interface to search, view, and visualize NFL data using the `nfl_data_py` library.

## Features

-   **Data Searching:** Select from various NFL datasets (Play-by-Play, Weekly, Seasonal, Rosters, Combine, etc.), specify years, and optionally filter by columns.
-   **Tabular Data Display:** View search results in a sortable and paginated table.
-   **Data Visualization:** Generate various types of plots (Scatter, Line, Bar, Histogram, Box Plot) from the search results. Customize plots by selecting X and Y axes, and an optional grouping variable for colors.
-   **Dynamic UI:** The interface dynamically updates options based on selected data types and provides feedback on available data columns.

## How to Run

1.  **Prerequisites:**
    *   Python 3.x
    *   pip (Python package installer)

2.  **Installation:**
    *   Clone this repository (or ensure you have the `nfl_data_py` library and the `app` directory structure).
    *   Install the required Python packages:
        ```bash
        pip install Flask pandas plotly nfl_data_py
        ```
        (If `nfl_data_py` is part of a larger package or has specific installation steps, refer to its main README.)

3.  **Running the Application:**
    *   Navigate to the root directory of this project (where `run.py` is located).
    *   Execute the following command in your terminal:
        ```bash
        python run.py
        ```
    *   Open your web browser and go to `http://127.0.0.1:5000/`.

## Using the Interface

1.  **Select Data Type:** Choose the type of NFL data you want to explore from the "Data Type" dropdown.
    *   Additional options specific to the data type (e.g., "Season Type" for Seasonal Data, "NGS Stat Type" for Next Gen Stats) will appear below.
2.  **Enter Years:** Provide a comma-separated list of years (e.g., `2022,2023`).
3.  **Specify Columns (Optional):**
    *   You can enter a comma-separated list of columns you are interested in.
    *   Alternatively, click "Fetch Available Columns" to see a list of common columns for the selected data type. This can help guide your selection.
4.  **Search Data:** Click the "Search Data" button.
    *   Results will be displayed in a table below the search form.
    *   If there's an error (e.g., no data found, invalid input), an error message will appear.
5.  **Visualize Data:**
    *   Once data is successfully searched and displayed, the "Create Visualization" form will become available.
    *   **Select Visualization Type:** Choose the type of plot you want (e.g., Scatter Plot, Bar Chart).
    *   **Select X-Axis and Y-Axis:** Choose the columns from your search results to plot on the X and Y axes.
    *   **Select Color By (Optional):** For some plots, you can choose a categorical column to group data by color.
    *   **Generate Visualization:** Click "Generate Visualization". The plot will appear at the bottom of the page.

## Project Structure

-   `run.py`: Main Flask application script to start the development server.
-   `app/`: Directory containing the Flask application.
    -   `__init__.py`: Initializes the Flask app.
    -   `routes.py`: Defines the application's routes (URL handlers) for searching, visualizing, and fetching column information.
    -   `templates/`: Contains HTML templates.
        -   `index.html`: The main page of the application.
    -   `static/`: (Currently unused, but available for CSS, JavaScript files if needed in the future).
-   `nfl_data_py/`: (Assumed to be the existing library for fetching NFL data).
-   `README_WEB.md`: This file.

## Deployment

This application is set up to run with the Flask development server, which is not recommended for production environments. For deployment, consider using a production-ready WSGI server like Gunicorn or uWSGI, and potentially placing it behind a reverse proxy like Nginx.

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```
This command starts Gunicorn with 4 worker processes, listening on port 8000. Adjust parameters as needed. You would then configure Nginx to proxy requests to Gunicorn.

Further steps for production deployment would include:
-   Setting `DEBUG = False` in a Flask configuration.
-   Managing static files more robustly.
-   Setting up logging and error monitoring.
-   Ensuring proper security measures (HTTPS, etc.).

# NFL Data Visualizer Web Interface

This web application provides a user-friendly interface to search, view, and visualize NFL data using the `nfl_data_py` library.

## Features

-   **Comprehensive Data Searching:**
    *   Select the specific `nfl_data_py` function to call (e.g., `import_pbp_data`, `import_seasonal_data`, `import_ngs_data`).
    *   Dynamically displays relevant input fields based on the selected function, including:
        *   Years (comma-separated list).
        *   Columns to retrieve (comma-separated list, optional for many functions). The placeholder suggests consulting `nflverse` documentation for available column names.
        *   Function-specific parameters (e.g., `s_type` for seasonal data, `stat_type` for NGS).
        *   Boolean flags (e.g., `include_participation`, `cache`, `downcast`, `thread_requests`) with tooltips explaining their purpose.
-   **Tabular Data Display:** View search results in a scrollable table, with information on rows/columns retrieved.
-   **Data Visualization:**
    *   Generate various types of plots (Scatter, Line, Bar, Histogram, Box Plot) from the search results.
    *   Customize plots by selecting X and Y axes, and an optional grouping variable for colors from the currently loaded data.
-   **Dynamic UI:** The interface dynamically updates parameter forms based on the selected `nfl_data_py` function.
-   **Column Helper:** "Fetch Columns (PBP/Weekly only)" button for Play-by-Play and Weekly data types to guide column selection.

## Setup and Installation (for GitHub Codespaces)

This guide is optimized for setting up and running the application within a GitHub Codespace.

**1. Open in Codespaces:**

   If you haven't already, open this repository in a GitHub Codespace.

**2. Create and Activate a Python Virtual Environment (Recommended):**

   Open a terminal in your Codespace.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Your terminal prompt should now start with `(.venv)`.

**3. Install Python Dependencies:**

   With your virtual environment active, install the required packages:
   ```bash
   pip install pandas Flask plotly nfl_data_py
   ```

   <br>

   **‼‼‼ BIG WARNING: `pandas` Version & `nfl_data_py` Compatibility ‼‼‼**
   *   The command above attempts to install the **latest available `pandas`**.
   *   However, the version of `nfl_data_py` currently on PyPI (v0.3.3) **officially requires `pandas < 2.0`**.
   *   Using a newer `pandas` (e.g., `pandas 2.x` or `3.x`) with `nfl_data_py 0.3.3` is **NOT OFFICIALLY SUPPORTED** by `nfl_data_py`'s authors.
   *   **POTENTIAL CONSEQUENCES:** This mismatch **MAY LEAD TO RUNTIME ERRORS, CRASHES, OR INCORRECT DATA PROCESSING** within `nfl_data_py`'s functions. You are proceeding with this simplified setup at your own risk regarding the stability and correctness of `nfl_data_py`.
   *   **If you encounter issues that seem related to `nfl_data_py` or `pandas`:**
        *   The most stable solution is to ensure `pandas 1.5.x` is used. In Codespaces, this typically requires installing build tools first, then specifying the `pandas` and `nfl_data_py` versions:
          ```bash
          # (Inside your .venv)
          sudo apt-get update
          sudo apt-get install -y build-essential python3-dev
          pip install Flask "pandas>=1.5.0,<2.0" plotly "nfl_data_py==0.3.3"
          ```
        *   This will likely install `pandas 1.5.3`. The build tools help it compile if a pre-built version isn't available.

   <br>

**4. Running the Application:**

   Once dependencies are installed (and you acknowledge the pandas warning above):
   ```bash
   python run.py
   ```
   GitHub Codespaces should automatically detect the running application (default port 5000) and offer to open it in a browser via the "Ports" tab or a notification.

## Using the Interface

1.  **Select Function:** Choose the `nfl_data_py` function from the "Select Function:" dropdown.
2.  **Fill Parameters:** The form dynamically updates.
    *   **Years:** If applicable, enter comma-separated years.
    *   **Columns:** If applicable, enter comma-separated column names. Use "Fetch Columns (PBP/Weekly only)" for helpers, or consult `nflverse` docs for others.
    *   **Function-Specific Parameters:** Fill any other fields. Hover over labels for options like "Downcast Floats" for tooltips.
3.  **Search Data:** Click "Search Data". Results appear in a table.
4.  **Visualize Data:** If data is found, the visualization form appears. Select plot type, axes, and generate.

## Project Structure

-   `run.py`: Main Flask script.
-   `app/`: Flask application package.
    -   `__init__.py`: App initialization.
    -   `routes.py`: Backend logic and routes.
    -   `templates/index.html`: Frontend HTML and JavaScript.
-   `README_WEB.md`: This file.

## Deployment (General Notes)

For production, use a WSGI server (Gunicorn, uWSGI) and a reverse proxy (Nginx). Set `DEBUG = False`.
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

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

   Install the required packages using pip:
   ```bash
   pip install Flask pandas plotly nfl_data_py
   ```

   **Important Note on `pandas` Version and `nfl_data_py`:**
   *   The standard version of `nfl_data_py` available via pip (e.g., v0.3.3) has a strict requirement for `pandas < 2.0`. If `pip` attempts to install an older `pandas` (like 1.5.3) and needs to build it from source, this can be very slow or fail in some environments if build tools are missing.
   *   **This application setup, by default, does not force an older pandas.** It attempts to install the latest compatible versions of Flask, Plotly, and pandas, alongside `nfl_data_py`.
   *   **POTENTIAL RISK:** Using a `pandas` version `>= 2.0` with `nfl_data_py 0.3.3` (or similar versions) is **not officially supported** by `nfl_data_py` and **may lead to unexpected errors or incorrect data processing within `nfl_data_py` functions.**
   *   **If you encounter issues related to `pandas` version mismatches with `nfl_data_py` functions:**
        1. You might need to create an environment that strictly adheres to `nfl_data_py`'s dependency on `pandas < 2.0`. For Codespaces, this would involve ensuring build tools are present *before* installing, as `pandas 1.5.x` often needs compilation:
           ```bash
           # (Inside your .venv)
           sudo apt-get update
           sudo apt-get install -y build-essential python3-dev
           pip install Flask pandas=="1.5.3" plotly nfl_data_py=="0.3.3" # Example pinning
           ```
        2. Alternatively, await an updated version of `nfl_data_py` that officially supports newer `pandas` versions.

**4. Running the Application:**

   Once dependencies are installed:
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

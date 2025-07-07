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

## Setup and Installation (for GitHub Codespaces)

This guide is optimized for setting up and running the application within a GitHub Codespace.

**1. Open in Codespaces:**

   If you haven't already, open this repository in a GitHub Codespace. This will provide you with a cloud-based development environment.

**2. Create and Activate a Python Virtual Environment (Recommended):**

   Open a terminal in your Codespace (usually available at the bottom of the VS Code interface).
   It's good practice to use a virtual environment to keep dependencies isolated:

   ```bash
   python3 -m venv .venv  # Creates a virtual environment named .venv
   source .venv/bin/activate   # Activates the virtual environment
   ```
   You should see `(.venv)` at the beginning of your terminal prompt.

**3. Install Python Dependencies (with pandas build fix):**

   The `nfl_data_py` library (version 0.3.3) requires an older version of `pandas` (`<2.0`). When `pip` installs this, it might try to build `pandas` from source, which can be slow or fail if build tools are missing.

   To ensure a smooth installation in Codespaces:

   *   **First, ensure build tools are present:**
       ```bash
       sudo apt-get update
       sudo apt-get install -y build-essential python3-dev
       ```
       This command ensures your Codespace environment has the necessary C compilers and Python development headers to build packages like older versions of `pandas` if needed.

   *   **Then, install the required packages:**
       ```bash
       pip install Flask pandas plotly nfl_data_py
       ```
       This command will install Flask, Plotly, and `nfl_data_py`. Because `nfl_data_py` requires `pandas<2.0`, `pip` will fetch a compatible version (likely `pandas 1.5.3`). With the build tools installed, this compilation step (if it occurs) should now succeed. It might still take a few minutes for `pandas` to compile if a pre-built wheel isn't used by pip for your specific Python version in Codespaces.

**4. Running the Application:**

   Once all dependencies are installed successfully (after the `pip install` command completes without errors):

   ```bash
   python run.py
   ```
   GitHub Codespaces should automatically detect that an application is running on a port (default for Flask is 5000) and provide a pop-up or a notification in the "Ports" tab allowing you to open the application in a browser.

   If you don't see an automatic prompt, you can manually check the "Ports" tab in VS Code (usually on the bottom panel, or type "Ports" in the command palette). Find the entry for port 5000, and click the "Open in Browser" (globe) icon. This will open `http://127.0.0.1:5000/` (or a proxied URL) in a new tab.

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

## Deployment (General Notes)

This application uses the Flask development server, not suitable for production. For deployment outside of Codespaces, use a production WSGI server (e.g., Gunicorn, uWSGI) behind a reverse proxy (e.g., Nginx).

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```
Ensure `DEBUG = False` in production, manage static files appropriately, and set up logging/monitoring.

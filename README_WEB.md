# NFL Data Visualizer Web Interface

This web application provides a user-friendly interface to search, view, and visualize NFL data using the `nfl_data_py` library.

## Features

-   **Comprehensive Data Searching:** Select the specific `nfl_data_py` function to call. Dynamically displays relevant input fields for the selected function (Years, Columns, specific options with tooltips).
-   **Tabular Data Display:** View search results in a scrollable table with row/column info.
-   **Data Visualization:** Generate plots (Scatter, Line, Bar, Histogram, Box Plot).
-   **Dynamic UI & Column Helper:** Dynamically updates forms; "Fetch Columns (PBP/Weekly only)" button.

## Setup and Installation (for GitHub Codespaces)

This project uses a version of `nfl_data_py` (included in this repository) that has been configured to work with `pandas 2.0` or newer.

**1. Open in Codespaces:**

   Open this repository in a GitHub Codespace. This is the recommended environment.

**2. Create and Activate a Python Virtual Environment:**

   Open a terminal in your Codespace.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Your terminal prompt should now start with `(.venv)`.

**3. Install Dependencies:**

   With your virtual environment active, install the project and its dependencies. This command installs the `nfl_data_py` package from the local repository files (which now specifies modern `pandas`) and other necessary libraries for the web app.
   ```bash
   pip install -e .
   pip install Flask plotly
   # pandas and numpy will be installed as dependencies of the local nfl_data_py
   # If you want to ensure the absolute latest pandas 2.x or 3.x:
   # pip install "pandas>=2.0"
   ```

**4. Running the Application:**

   Once dependencies are installed:
   ```bash
   python run.py
   ```
   Access the application via the URL provided by Codespaces in the "Ports" tab (usually for port 5000).

## Using the Interface

1.  **Select Function:** Choose the `nfl_data_py` function from the "Select Function:" dropdown.
2.  **Fill Parameters:** The form dynamically updates. Fill in applicable fields (Years, Columns, specific options). Hover over labels for tooltips on some options.
3.  **Search Data:** Click "Search Data". Results appear in a table.
4.  **Visualize Data:** If data is found, the visualization form appears. Select plot type, axes, and generate.

## Project Structure

-   `run.py`: Main Flask script.
-   `app/`: Flask application package.
-   `nfl_data_py/`: The nfl_data_py library (modified for pandas>=2.0).
-   `pyproject.toml`: Defines dependencies for `nfl_data_py`, including the modified pandas requirement.
-   `README_WEB.md`: This file.

## A Note on `nfl_data_py` and `pandas` Versioning

The `nfl_data_py` library as published on PyPI (e.g., v0.3.3) officially requires `pandas < 2.0`. The `pyproject.toml` file in *this* repository has been modified to specify `pandas >= 2.0`. This allows the web application to use a modern version of `pandas`.

**Potential Risk:** While this change enables the use of newer `pandas`, there's a possibility that some internal functions of `nfl_data_py` (v0.3.3 code) might have incompatibilities with `pandas 2.x` or newer, as it wasn't originally designed or tested for them. If you encounter errors specifically from within `nfl_data_py` functions, this version mismatch could be a factor. For maximum stability with the official `nfl_data_py` code, using `pandas 1.5.x` (which often requires compiling from source and thus needs build tools like `build-essential` and `python3-dev` on Linux) would be necessary. This project prioritizes using a newer `pandas` as requested.

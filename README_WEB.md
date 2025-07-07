# NFL Data Visualizer Web Interface

This web application provides a user-friendly interface to search, view, process, and visualize NFL data using the `nfl_data_py` library.

## Features

-   **Comprehensive Initial Data Search:**
    *   Select the specific `nfl_data_py` function to call (e.g., `import_pbp_data`, `import_seasonal_data`).
    *   Dynamically displays relevant input fields for the selected function (Years, Columns, specific options with tooltips).
-   **Advanced Data Processing (Post-Search):**
    *   **Filter Builder:** Apply multiple conditions to the fetched data. Select columns, operators (e.g., `==`, `>`, `contains`), and values to refine your dataset.
    *   **Aggregation:** Group data by specified columns and apply aggregation functions (e.g., `sum`, `mean`, `count`) to selected numeric columns.
    *   **Column Re-selection:** Choose a subset of columns from the processed data for final display and visualization.
-   **Tabular Data Display:** View initial and processed search results in a scrollable table with row/column count information.
-   **Data Visualization:**
    *   Generate various types of plots (Scatter, Line, Bar, Histogram, Box Plot) from the currently displayed (potentially processed) data.
    *   Customize plots by selecting X and Y axes, and an optional grouping variable for colors.
-   **Dynamic UI & Column Helper:** Dynamically updates forms; "Fetch Columns (PBP/Weekly only)" button for initial search.

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

**Phase 1: Initial Data Search**

1.  **Select Function:** Choose the `nfl_data_py` function from the "Select Function:" dropdown (e.g., `import_pbp_data`, `import_weekly_data`).
2.  **Fill Initial Parameters:** The form dynamically updates. Fill in applicable fields:
    *   **Years:** If applicable, provide a comma-separated list of years.
    *   **Columns:** If applicable, provide a comma-separated list of columns. For PBP and Weekly data, you can use the "Fetch Columns (PBP/Weekly only)" button as a helper. For other data types, consult `nflverse` documentation for column names (placeholder text provides this hint).
    *   **Function-Specific Parameters:** Fill in any other displayed fields (e.g., dropdowns for season type, stat type; checkboxes for boolean options like "Downcast Floats"). Hover over labels for tooltips.
3.  **Search Data:** Click the "Search Data" button.
    *   Initial results appear in a table. Row and column counts are displayed.
    *   The "Filter & Process Data" and "Create Visualization" sections become visible.

**Phase 2: Filtering & Processing (Optional)**

After an initial search, you can refine the data:

1.  **Add Filters:**
    *   In the "Filter & Process Data" section, go to "Filters".
    *   Select a column from the "Filter Column" dropdown (populated with columns from your current data).
    *   Choose an operator (e.g., `>`, `==`, `contains`).
    *   Enter a value in the text field.
    *   Click "Add Filter". The filter will appear in the "Active Filters" list.
    *   Repeat to add multiple filters. Filters are applied in AND fashion. You can remove filters from the list.
2.  **Apply Aggregation (Optional):**
    *   Go to the "Aggregation" subsection.
    *   **Group By:** Enter one or more comma-separated column names to group by (e.g., `season,player_name`).
    *   **Aggregation Function:** Select a function like `sum`, `mean`, or `count`.
    *   **Aggregate Columns:** For functions like `sum` or `mean`, enter comma-separated numeric column names to aggregate (e.g., `passing_yards,rushing_tds`). For `count`, this can often be left blank.
3.  **Re-select Display Columns (Optional):**
    *   Go to "Display Columns".
    *   Enter a comma-separated list of column names you want to see in the final table and use for plotting. If left blank, all columns from the processed data are shown.
4.  **Process Data:** Click the "Apply Filters/Processing" button.
    *   The table will update with the data after applying your filters, aggregation (if any), and column selections.
    *   Row/column counts will update.
    *   The visualization axis dropdowns will update based on the columns of this newly processed data.

**Phase 3: Visualization**

1.  **Select Visualization Type:** Choose from Scatter Plot, Line Plot, Bar Chart, etc.
2.  **Select Axes:** Choose X-axis, Y-axis, and optionally "Color By" from the dropdowns. These lists reflect the columns of the data currently displayed in the table.
3.  **Generate Visualization:** Click "Generate Visualization". The plot will appear at the bottom.

## Project Structure

-   `run.py`: Main Flask script.
-   `app/`: Flask application package.
-   `nfl_data_py/`: The nfl_data_py library (its `pyproject.toml` is modified in this repo for pandas>=2.0).
-   `pyproject.toml`: Defines dependencies for `nfl_data_py` at the root of this project.
-   `README_WEB.md`: This file.

## A Note on `nfl_data_py` and `pandas` Versioning

The `nfl_data_py` library as published on PyPI (e.g., v0.3.3) officially requires `pandas < 2.0`. The `pyproject.toml` file in *this* repository has been modified to specify `pandas >= 2.0` for the embedded `nfl_data_py` package. This allows the web application to use a modern version of `pandas`.

**Potential Risk:** While this change enables the use of newer `pandas`, there's a possibility that some internal functions of `nfl_data_py` (v0.3.3 code) might have incompatibilities with `pandas 2.x` or newer, as it wasn't originally designed or tested for them. If you encounter errors specifically from within `nfl_data_py` functions during the initial data fetch, this version mismatch could be a factor. For maximum stability with the official `nfl_data_py` code, using `pandas 1.5.x` (which often requires compiling from source and thus needs build tools like `build-essential` and `python3-dev` on Linux) would be necessary by adjusting the `pyproject.toml` back and ensuring the build environment is set up. This project prioritizes using a newer `pandas` as requested for the web app's direct dependencies.

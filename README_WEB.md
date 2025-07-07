# NFL Data Visualizer Web Interface

This web application provides a user-friendly interface to search, view, and visualize NFL data using the `nfl_data_py` library.

## Features

-   **Comprehensive Data Searching:**
    *   Select the specific `nfl_data_py` function to call.
    *   Dynamically displays relevant input fields for selected function (Years, Columns, specific options with tooltips).
-   **Tabular Data Display:** View search results in a scrollable table with row/column info.
-   **Data Visualization:** Generate plots (Scatter, Line, Bar, Histogram, Box Plot).
-   **Dynamic UI & Column Helper:** Dynamically updates forms; "Fetch Columns (PBP/Weekly only)" button.

## Setup and Installation (for GitHub Codespaces)

This guide is optimized for setting up and running the application within a GitHub Codespace.

**1. Open in Codespaces:**

   Open this repository in a GitHub Codespace.

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
   This command attempts to install the latest versions of these packages.

   *(For troubleshooting potential `nfl_data_py` dependency issues, please see `WARNINGS.md`)*

**4. Running the Application:**

   Once dependencies are installed:
   ```bash
   python run.py
   ```
   GitHub Codespaces should automatically detect the running application (default port 5000) and offer to open it in a browser via the "Ports" tab or a notification.

## Using the Interface

1.  **Select Function:** Choose the `nfl_data_py` function from the "Select Function:" dropdown.
2.  **Fill Parameters:** The form dynamically updates. Fill in applicable fields (Years, Columns, specific options). Hover over labels for tooltips on some options.
3.  **Search Data:** Click "Search Data". Results appear in a table.
4.  **Visualize Data:** If data is found, the visualization form appears. Select plot type, axes, and generate.

## Project Structure

-   `run.py`: Main Flask script.
-   `app/`: Flask application package.
-   `README_WEB.md`: This file.
-   `WARNINGS.md`: Important notes on dependencies and troubleshooting.

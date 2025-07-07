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

## Setup and Installation (for GitHub Codespaces - Using Current Pandas)

This guide outlines how to set up the application to use a **current version of `pandas` (>= 2.0)**. This approach **deviates from the official dependencies of `nfl_data_py` version 0.3.3 (which requires `pandas < 2.0`) and carries risks of incompatibility.**

**USER ACKNOWLEDGES THE RISKS: By following this setup, you are attempting to run `nfl_data_py` (v0.3.3 or similar) with a `pandas` version it was not designed or tested for. This may lead to runtime errors, incorrect data processing, or crashes within `nfl_data_py`'s functions. This setup is provided at user request for a potentially simpler initial install if `pandas 1.5.x` compilation is problematic, but stability of `nfl_data_py` is NOT guaranteed.**

**1. Open in Codespaces:**

   If you haven't already, open this repository in a GitHub Codespace.

**2. Create and Activate a Python Virtual Environment (Recommended):**

   Open a terminal in your Codespace.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Your terminal prompt should now start with `(.venv)`.

**3. Modify `nfl_data_py` to Allow Newer Pandas (Required for this approach):**

   To use a newer `pandas` version, you must modify the `nfl_data_py` library's source code to change its `pandas` dependency requirements *before* it is installed.

   a.  **Clone the `nfl_data_py` repository into a separate directory (or alongside this project):**
      ```bash
      # Example: cloning into a 'libs' subdirectory
      mkdir -p libs
      cd libs
      git clone https://github.com/cooperdff/nfl_data_py.git
      cd nfl_data_py
      # You are now in the nfl_data_py source directory
      ```

   b.  **Edit `pyproject.toml` in the cloned `nfl_data_py` directory:**
      Find the line that specifies the pandas dependency, which looks like:
      `pandas = ">=1.0,<2.0"`
      Change it to allow newer versions, for example:
      `pandas = ">=1.5"` or `pandas = ">=2.0"`
      (Using `>=1.5` is slightly less risky but still outside the original `<2.0` bound). For this guide, we'll assume you change it to allow `pandas >=2.0` as per the user request for "current pandas".

   c.  **Install your modified local version of `nfl_data_py`:**
      From within your modified `nfl_data_py` source directory (where `pyproject.toml` is), run:
      ```bash
      # (Ensure your virtual environment .venv is active)
      pip install -e .
      ```
      The `-e .` installs it in "editable" mode, meaning your environment will use this local, modified version. Pip will now try to install its dependencies, including the newer `pandas` version you specified.

**4. Install Web Application Dependencies:**

   Navigate back to the root directory of *this* web application project.
   With the virtual environment still active (and your modified `nfl_data_py` installed), install Flask and Plotly:
   ```bash
   # (Ensure you are in the root of the web visualizer project)
   pip install Flask plotly pandas
   ```
   (Adding `pandas` here ensures it gets the latest version if not already pulled by your modified `nfl_data_py`'s install, or aligns it if `nfl_data_py` just had `>=1.5`).

**5. Running the Application:**

   Once all dependencies are installed:
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
3.  **Search Data:** Click "Search Data". Results appear in a table. **Be vigilant for errors here, as this is where `nfl_data_py` interacts with the potentially incompatible `pandas` version.**
4.  **Visualize Data:** If data is found, the visualization form appears. Select plot type, axes, and generate.

## Project Structure

-   `run.py`: Main Flask script.
-   `app/`: Flask application package.
-   `README_WEB.md`: This file.
-   (Locally cloned and modified `nfl_data_py` directory, as per setup).

## Alternative: Stable Setup (Using `pandas < 2.0` as required by `nfl_data_py 0.3.3`)

If you encounter issues with the above setup due to `pandas` incompatibility, the most stable method is to adhere to `nfl_data_py`'s original dependencies:

1.  Activate your virtual environment (`source .venv/bin/activate`).
2.  Ensure build tools are present for `pandas 1.5.x` compilation:
    ```bash
    sudo apt-get update
    sudo apt-get install -y build-essential python3-dev
    ```
3.  Install packages, letting `nfl_data_py` specify its `pandas` version:
    ```bash
    pip install Flask plotly "nfl_data_py==0.3.3" "pandas<2.0,>=1.5.0"
    ```
    This will likely install `pandas 1.5.3`. The build tools should help it compile successfully.
---
This README now prioritizes the user's request for a "current pandas" setup by guiding them through modifying `nfl_data_py` locally, while heavily emphasizing the risks. It also retains the "stable setup" as a clearly marked alternative.

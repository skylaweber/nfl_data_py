# WARNINGS & Dependency Troubleshooting

This file contains important information regarding potential dependency issues when setting up the NFL Data Visualizer, particularly concerning the `nfl_data_py` library and its interaction with different versions of the `pandas` library.

## ‼‼‼ `pandas` Version & `nfl_data_py` Compatibility ‼‼‼

The main `README_WEB.md` provides a simplified installation command:
```bash
pip install pandas Flask plotly nfl_data_py
```
This command attempts to install the **latest available `pandas`** version from PyPI.

**HOWEVER, PLEASE BE AWARE:**

*   The version of `nfl_data_py` currently on PyPI (v0.3.3 as of late 2023/early 2024) **officially requires `pandas < 2.0`** in its package metadata.
*   Using a newer `pandas` (e.g., `pandas 2.x` or `3.x`) with `nfl_data_py 0.3.3` is **NOT OFFICIALLY SUPPORTED** by `nfl_data_py`'s authors.
*   **POTENTIAL CONSEQUENCES:** This mismatch **MAY LEAD TO RUNTIME ERRORS, CRASHES, OR INCORRECT DATA PROCESSING** within `nfl_data_py`'s functions. The web application might appear to run, but calls to `nfl_data_py` functions (like fetching data or even getting column lists) could fail unexpectedly.

**You are proceeding with the simplified setup (latest `pandas`) at your own risk regarding the stability and correctness of data retrieved via `nfl_data_py`.**

## Troubleshooting: If `nfl_data_py` Functions Fail

If you use the simple `pip install` command from the main README and encounter errors when the web application tries to fetch data (e.g., "Error fetching columns: error", or errors during data search that mention `pandas` or `nfl_data_py` internals), it is highly likely due to the `pandas` version incompatibility.

**Recommended Stable Setup (Adhering to `nfl_data_py 0.3.3` Dependencies):**

To ensure `nfl_data_py` uses a `pandas` version it was designed for (`pandas 1.5.x`), follow these steps, especially in a GitHub Codespace or similar Linux environment:

1.  **Ensure your virtual environment is active:**
    ```bash
    # Example: source .venv/bin/activate
    ```

2.  **Install build tools (if not already present):**
    Older versions of `pandas` like 1.5.3 often need to be compiled from source if a pre-built "wheel" isn't available for your specific Python/OS combination. Build tools are necessary for this compilation.
    ```bash
    sudo apt-get update
    sudo apt-get install -y build-essential python3-dev
    ```
    *(For macOS, ensure Xcode Command Line Tools are installed. For Windows, Microsoft C++ Build Tools might be needed, which is more complex; consider WSL or using the `conda` environment manager if on Windows and facing build issues).*

3.  **Install specific package versions:**
    This command tells `pip` to install `nfl_data_py` version 0.3.3 and a version of `pandas` that is `>=1.5.0` but `<2.0`.
    ```bash
    pip install Flask plotly "nfl_data_py==0.3.3" "pandas>=1.5.0,<2.0"
    ```
    This will likely result in `pandas 1.5.3` being installed. The presence of build tools (from step 2) should allow it to compile successfully if needed. This setup is much more likely to be stable for `nfl_data_py 0.3.3`.

By following this "Stable Setup," you align the environment with `nfl_data_py`'s documented dependencies, significantly reducing the risk of runtime issues within that library.

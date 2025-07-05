from flask import render_template, request, jsonify
from app import app
import nfl_data_py as nfl
import plotly.express as px
import pandas as pd
import json
import plotly

# Utility function to convert plot to JSON
def fig_to_json(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_data():
    try:
        payload = request.form
        function_name = payload.get('function_name')

        if not function_name:
            return jsonify({'error': 'Missing function_name.'}), 400

        # Prepare arguments for nfl_data_py functions
        kwargs = {}
        years_str = payload.get('years')
        if years_str:
            try:
                kwargs['years'] = [int(year.strip()) for year in years_str.split(',')]
            except ValueError:
                return jsonify({'error': 'Invalid format for years. Please provide comma-separated integers.'}), 400

        columns_str = payload.get('columns_str') # Renamed from 'columns' to avoid conflict with kwarg
        if columns_str:
            kwargs['columns'] = [col.strip() for col in columns_str.split(',')]

        # Dynamically call the selected nfl_data_py function
        df = None
        if function_name == 'import_pbp_data':
            kwargs['include_participation'] = payload.get('pbp_include_participation') == 'true'
            kwargs['downcast'] = payload.get('pbp_downcast') == 'true'
            kwargs['cache'] = payload.get('pbp_cache') == 'true'
            kwargs['alt_path'] = payload.get('pbp_alt_path') if payload.get('pbp_alt_path') else None
            kwargs['thread_requests'] = payload.get('pbp_thread_requests') == 'true'
            # Filter out years if not applicable (though frontend should hide it)
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for PBP data.'}), 400
            df = nfl.import_pbp_data(**{k: v for k, v in kwargs.items() if k in nfl.import_pbp_data.__code__.co_varnames})

        elif function_name == 'import_weekly_data':
            kwargs['downcast'] = payload.get('weekly_downcast') == 'true'
            kwargs['thread_requests'] = payload.get('weekly_thread_requests') == 'true'
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Weekly data.'}), 400
            df = nfl.import_weekly_data(**{k: v for k, v in kwargs.items() if k in nfl.import_weekly_data.__code__.co_varnames})

        elif function_name == 'import_seasonal_data':
            kwargs['s_type'] = payload.get('seasonal_s_type', 'REG')
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Seasonal data.'}), 400
            df = nfl.import_seasonal_data(**{k: v for k, v in kwargs.items() if k in nfl.import_seasonal_data.__code__.co_varnames})

        elif function_name == 'import_seasonal_rosters':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Seasonal Rosters.'}), 400
            df = nfl.import_seasonal_rosters(**{k: v for k, v in kwargs.items() if k in nfl.import_seasonal_rosters.__code__.co_varnames})

        elif function_name == 'import_weekly_rosters':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Weekly Rosters.'}), 400
            df = nfl.import_weekly_rosters(**{k: v for k, v in kwargs.items() if k in nfl.import_weekly_rosters.__code__.co_varnames})

        elif function_name == 'import_ngs_data':
            kwargs['stat_type'] = payload.get('ngs_stat_type')
            if not kwargs.get('stat_type'): return jsonify({'error': 'NGS Stat Type is required.'}), 400
            # Years is optional for ngs_data in lib, but UI makes it common. Filter if not needed by function.
            df = nfl.import_ngs_data(**{k: v for k, v in kwargs.items() if k in nfl.import_ngs_data.__code__.co_varnames})

        elif function_name == 'import_combine_data':
            positions_str = payload.get('combine_positions')
            if positions_str:
                kwargs['positions'] = [pos.strip() for pos in positions_str.split(',')]
            df = nfl.import_combine_data(**{k: v for k, v in kwargs.items() if k in nfl.import_combine_data.__code__.co_varnames})

        elif function_name == 'import_draft_picks':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Draft Picks.'}), 400
            df = nfl.import_draft_picks(**{k: v for k, v in kwargs.items() if k in nfl.import_draft_picks.__code__.co_varnames})

        elif function_name == 'import_qbr':
            kwargs['level'] = payload.get('qbr_level', 'nfl')
            kwargs['frequency'] = payload.get('qbr_frequency', 'season')
            df = nfl.import_qbr(**{k: v for k, v in kwargs.items() if k in nfl.import_qbr.__code__.co_varnames})

        elif function_name == 'import_seasonal_pfr':
            kwargs['s_type'] = payload.get('pfr_seasonal_s_type')
            if not kwargs.get('s_type'): return jsonify({'error': 'PFR Stat Type is required.'}), 400
            df = nfl.import_seasonal_pfr(**{k: v for k, v in kwargs.items() if k in nfl.import_seasonal_pfr.__code__.co_varnames})

        elif function_name == 'import_weekly_pfr':
            kwargs['s_type'] = payload.get('pfr_weekly_s_type')
            if not kwargs.get('s_type'): return jsonify({'error': 'PFR Stat Type is required.'}), 400
            df = nfl.import_weekly_pfr(**{k: v for k, v in kwargs.items() if k in nfl.import_weekly_pfr.__code__.co_varnames})

        elif function_name == 'import_snap_counts':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Snap Counts.'}), 400
            df = nfl.import_snap_counts(**{k: v for k, v in kwargs.items() if k in nfl.import_snap_counts.__code__.co_varnames})

        elif function_name == 'import_ftn_data':
            kwargs['downcast'] = payload.get('ftn_downcast') == 'true'
            kwargs['thread_requests'] = payload.get('ftn_thread_requests') == 'true'
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for FTN Data.'}), 400
            df = nfl.import_ftn_data(**{k: v for k, v in kwargs.items() if k in nfl.import_ftn_data.__code__.co_varnames})

        elif function_name == 'import_depth_charts':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Depth Charts.'}), 400
            df = nfl.import_depth_charts(years=kwargs['years'])

        elif function_name == 'import_injuries':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Injury Reports.'}), 400
            df = nfl.import_injuries(years=kwargs['years'])

        elif function_name == 'import_schedules':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Schedules.'}), 400
            df = nfl.import_schedules(years=kwargs['years'])

        elif function_name == 'import_officials': # years optional
            df = nfl.import_officials(**{k: v for k, v in kwargs.items() if k in nfl.import_officials.__code__.co_varnames and k=='years'})

        elif function_name == 'import_win_totals': # years optional
             df = nfl.import_win_totals(**{k: v for k, v in kwargs.items() if k in nfl.import_win_totals.__code__.co_varnames and k=='years'})

        elif function_name == 'import_sc_lines': # years optional
             df = nfl.import_sc_lines(**{k: v for k, v in kwargs.items() if k in nfl.import_sc_lines.__code__.co_varnames and k=='years'})

        elif function_name == 'import_draft_values': # No years/cols from common
            df = nfl.import_draft_values()

        elif function_name == 'import_team_desc': # No years/cols
            df = nfl.import_team_desc()

        elif function_name == 'import_contracts': # No years/cols
            df = nfl.import_contracts()

        elif function_name == 'import_ids': # uses columns, not years
            ids_str = payload.get('ids_ids')
            if ids_str:
                kwargs['ids'] = [i.strip() for i in ids_str.split(',')]
            # Keep only 'columns' and 'ids' for this function
            valid_kwargs_ids = {k: v for k,v in kwargs.items() if k in ['columns', 'ids']}
            df = nfl.import_ids(**valid_kwargs_ids)

        elif function_name == 'import_players': # No years/cols
            df = nfl.import_players()

        else:
            return jsonify({'error': f"Function '{function_name}' is not implemented in the GUI."}), 400

        if df is None:
            return jsonify({'error': 'No data returned from the function call (None result).'}), 404
        if df.empty and not list(df.columns):
             return jsonify({'error': 'No data found for the given parameters (empty result with no columns).'}), 404

        # df.to_json(orient='split') creates a dictionary:
        # {'index': [idx1, idx2, ...], 'columns': [col1, col2, ...], 'data': [[val1, val2,...], ...]}
        # This is what the frontend expects for table display and visualization.
        df_json_data = df.to_json(orient='split')

        return jsonify({'data': df_json_data, 'columns': list(df.columns)})

    except Exception as e:
        # Log the exception e for debugging
        print(f"Error in /search: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/visualize', methods=['POST'])
def visualize_data():
    try:
        data_json_str = request.form.get('data_json_str') # Expecting the JSON string as stored in JS
        viz_type = request.form.get('viz_type')
        x_axis = request.form.get('x_axis')
        y_axis = request.form.get('y_axis')
        color_by = request.form.get('color_by') # Optional

        if not all([data_json_str, viz_type, x_axis, y_axis]):
            return jsonify({'error': 'Missing required fields for visualization (data_json_str, viz_type, x_axis, y_axis).'}), 400

        # data_json_str is already a JSON string in 'split' orientation.
        # We need to parse it into a Python dict first, then load into pandas.
        try:
            data_dict = json.loads(data_json_str)
            df = pd.DataFrame(data_dict['data'], columns=data_dict['columns'], index=data_dict['index'])
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Error decoding or structuring data_json_str: {e}")
            return jsonify({'error': f'Invalid data format received from client: {e}'}), 400


        if df.empty:
            return jsonify({'error': 'Cannot visualize empty dataset.'}), 400

        if x_axis not in df.columns:
            return jsonify({'error': f"X-axis column '{x_axis}' not found in data."}), 400
        if y_axis not in df.columns:
             return jsonify({'error': f"Y-axis column '{y_axis}' not found in data."}), 400
        if color_by and color_by not in df.columns: # color_by is optional
            # Check if color_by is actually provided and not just an empty string from select
            if color_by != "":
                return jsonify({'error': f"Color-by column '{color_by}' not found in data."}), 400
            else:
                color_by = None # Ensure it's None if empty string passed

        fig = None
        title = f'{y_axis} vs. {x_axis}' if x_axis != y_axis else f'{x_axis} Distribution'
        if color_by:
            title += f' by {color_by}'

        # Ensure numeric types for appropriate plots if possible, or let Plotly handle it
        # Forcing conversion can be risky if data is genuinely categorical.
        # Plotly express is generally good at inferring types.

        if viz_type == 'scatter':
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, title=title)
        elif viz_type == 'line':
            # Line plots typically benefit from sorted x-axis if it's numeric/datetime
            # df_sorted = df.sort_values(by=x_axis) if x_axis in df.columns else df
            fig = px.line(df, x=x_axis, y=y_axis, color=color_by, title=title) # Using original df for now
        elif viz_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_by, title=title)
        elif viz_type == 'histogram':
            # Histogram uses x_axis for values, y_axis is typically frequency (auto-calculated)
            # If y_axis is provided and different from x_axis, it can be used for aggregated value
            current_y = y_axis if y_axis != x_axis and y_axis in df.columns else None
            fig = px.histogram(df, x=x_axis, y=current_y, color=color_by, title=f'Distribution of {x_axis}' + (f' (Y:{y_axis})' if current_y else '') + (f' by {color_by}' if color_by else ''))
        elif viz_type == 'box':
            fig = px.box(df, x=x_axis, y=y_axis, color=color_by, title=title)
        else:
            return jsonify({'error': 'Invalid visualization type specified.'}), 400

        if fig:
            graph_json = fig_to_json(fig)
            return jsonify({'graph_json': graph_json})
        else:
            # This case should ideally be caught by invalid viz_type or other errors above
            return jsonify({'error': 'Could not generate visualization for unspecified reasons.'}), 500

    except Exception as e:
        print(f"Error in /visualize: {e}")
        # Consider logging the full traceback here for better debugging
        # import traceback
        # print(traceback.format_exc())
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# Route to get available columns for a selected data type (and potentially years)
@app.route('/get_columns', methods=['GET'])
def get_columns_for_data_type():
    data_type = request.args.get('data_type')
    # For some data types, columns are fixed or can be inferred without loading all data
    # For others, we might need to load a small sample or rely on predefined lists
    # This is a simplified version
    cols = []
    if data_type == 'pbp':
        cols = nfl.see_pbp_cols()
    elif data_type == 'weekly':
        cols = nfl.see_weekly_cols()
    # Add more comprehensive column fetching for other types if nfl_data_py supports it
    # or by loading a small sample, e.g., nfl.import_seasonal_data(years=[2023]).columns.tolist()
    # For now, keep it simple or let user input columns freely / get them from initial search

    # Fallback for types where columns are not easily listed or vary greatly
    if not cols and data_type:
        try:
            # Attempt to load a small sample to get columns - use a recent year as example
            # This might be slow for large datasets like PBP
            sample_year = [2023] # Choose a representative year
            if data_type == 'seasonal':
                df_sample = nfl.import_seasonal_data(years=sample_year)
                cols = df_sample.columns.tolist()
            elif data_type == 'rosters_seasonal':
                df_sample = nfl.import_seasonal_rosters(years=sample_year)
                cols = df_sample.columns.tolist()
            # Add more types here if feasible
        except Exception as e:
            print(f"Could not fetch sample columns for {data_type}: {e}")
            return jsonify({'columns': []}) # Return empty if error or not implemented

    return jsonify({'columns': cols})

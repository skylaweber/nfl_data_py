from flask import render_template, request, jsonify
from app import app
import nfl_data_py as nfl
import plotly.express as px
import pandas as pd
import json
import plotly # For plotly.utils.PlotlyJSONEncoder

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

        kwargs = {} # Arguments for nfl_data_py functions

        # Common 'years' parameter
        years_str = payload.get('years')
        if years_str: # Only process if years_str is not None or empty
            try:
                kwargs['years'] = [int(year.strip()) for year in years_str.split(',') if year.strip()]
                if not kwargs['years']: # If after stripping, the list is empty (e.g. years_str was just ',')
                    kwargs.pop('years', None) # Remove if it became an empty list, let default handling or specific checks pass
            except ValueError:
                return jsonify({'error': 'Invalid format for years. Please provide comma-separated integers.'}), 400

        # Common 'columns' parameter
        columns_input_str = payload.get('columns_str') # Name used in JS payload
        if columns_input_str: # Only process if not None or empty
            kwargs['columns'] = [col.strip() for col in columns_input_str.split(',') if col.strip()]
            if not kwargs['columns']:
                 kwargs.pop('columns', None)


        df = None
        # Dynamically call the selected nfl_data_py function
        # Argument filtering (**{k: v for k,v in kwargs.items() if k in function.__code__.co_varnames})
        # is used to pass only relevant arguments from kwargs to each function.

        if function_name == 'import_pbp_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for PBP data.'}), 400
            kwargs['include_participation'] = payload.get('pbp_include_participation') == 'true'
            kwargs['downcast'] = payload.get('pbp_downcast') == 'true'
            kwargs['cache'] = payload.get('pbp_cache') == 'true'
            kwargs['alt_path'] = payload.get('pbp_alt_path') if payload.get('pbp_alt_path') else None
            kwargs['thread_requests'] = payload.get('pbp_thread_requests') == 'true'
            df = nfl.import_pbp_data(**{k:v for k,v in kwargs.items() if k in nfl.import_pbp_data.__code__.co_varnames})

        elif function_name == 'import_weekly_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Weekly data.'}), 400
            kwargs['downcast'] = payload.get('weekly_downcast') == 'true'
            kwargs['thread_requests'] = payload.get('weekly_thread_requests') == 'true'
            df = nfl.import_weekly_data(**{k:v for k,v in kwargs.items() if k in nfl.import_weekly_data.__code__.co_varnames})

        elif function_name == 'import_seasonal_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Seasonal data.'}), 400
            kwargs['s_type'] = payload.get('seasonal_s_type', 'REG')
            df = nfl.import_seasonal_data(**{k:v for k,v in kwargs.items() if k in nfl.import_seasonal_data.__code__.co_varnames})

        elif function_name == 'import_seasonal_rosters':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Seasonal Rosters.'}), 400
            df = nfl.import_seasonal_rosters(**{k:v for k,v in kwargs.items() if k in nfl.import_seasonal_rosters.__code__.co_varnames})

        elif function_name == 'import_weekly_rosters':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Weekly Rosters.'}), 400
            df = nfl.import_weekly_rosters(**{k:v for k,v in kwargs.items() if k in nfl.import_weekly_rosters.__code__.co_varnames})

        elif function_name == 'import_ngs_data':
            kwargs['stat_type'] = payload.get('ngs_stat_type')
            if not kwargs.get('stat_type'): return jsonify({'error': 'NGS Stat Type is required.'}), 400
            df = nfl.import_ngs_data(**{k:v for k,v in kwargs.items() if k in nfl.import_ngs_data.__code__.co_varnames})

        elif function_name == 'import_combine_data':
            positions_str = payload.get('combine_positions')
            if positions_str: # Only add if provided
                kwargs['positions'] = [pos.strip() for pos in positions_str.split(',') if pos.strip()]
                if not kwargs['positions']: kwargs.pop('positions', None)
            df = nfl.import_combine_data(**{k:v for k,v in kwargs.items() if k in nfl.import_combine_data.__code__.co_varnames})

        elif function_name == 'import_draft_picks':
            # Years is optional in lib, but UI makes it common. Let's make it required for GUI consistency.
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Draft Picks in this GUI.'}), 400
            df = nfl.import_draft_picks(**{k:v for k,v in kwargs.items() if k in nfl.import_draft_picks.__code__.co_varnames})

        elif function_name == 'import_qbr':
            kwargs['level'] = payload.get('qbr_level', 'nfl')
            kwargs['frequency'] = payload.get('qbr_frequency', 'season')
            df = nfl.import_qbr(**{k:v for k,v in kwargs.items() if k in nfl.import_qbr.__code__.co_varnames})

        elif function_name == 'import_seasonal_pfr':
            kwargs['s_type'] = payload.get('pfr_seasonal_s_type')
            if not kwargs.get('s_type'): return jsonify({'error': 'PFR Stat Type is required.'}), 400
            df = nfl.import_seasonal_pfr(**{k:v for k,v in kwargs.items() if k in nfl.import_seasonal_pfr.__code__.co_varnames})

        elif function_name == 'import_weekly_pfr':
            kwargs['s_type'] = payload.get('pfr_weekly_s_type')
            if not kwargs.get('s_type'): return jsonify({'error': 'PFR Stat Type is required.'}), 400
            df = nfl.import_weekly_pfr(**{k:v for k,v in kwargs.items() if k in nfl.import_weekly_pfr.__code__.co_varnames})

        elif function_name == 'import_snap_counts':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Snap Counts.'}), 400
            df = nfl.import_snap_counts(**{k:v for k,v in kwargs.items() if k in nfl.import_snap_counts.__code__.co_varnames})

        elif function_name == 'import_ftn_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for FTN Data.'}), 400
            kwargs['downcast'] = payload.get('ftn_downcast') == 'true'
            kwargs['thread_requests'] = payload.get('ftn_thread_requests') == 'true'
            df = nfl.import_ftn_data(**{k:v for k,v in kwargs.items() if k in nfl.import_ftn_data.__code__.co_varnames})

        elif function_name == 'import_depth_charts':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Depth Charts.'}), 400
            df = nfl.import_depth_charts(years=kwargs['years'])

        elif function_name == 'import_injuries':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Injury Reports.'}), 400
            df = nfl.import_injuries(years=kwargs['years'])

        elif function_name == 'import_schedules':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Schedules.'}), 400
            df = nfl.import_schedules(years=kwargs['years'])

        elif function_name == 'import_officials':
            df = nfl.import_officials(**{k:v for k,v in kwargs.items() if k=='years' and 'years' in nfl.import_officials.__code__.co_varnames})

        elif function_name == 'import_win_totals':
             df = nfl.import_win_totals(**{k:v for k,v in kwargs.items() if k=='years' and 'years' in nfl.import_win_totals.__code__.co_varnames})

        elif function_name == 'import_sc_lines':
             df = nfl.import_sc_lines(**{k:v for k,v in kwargs.items() if k=='years' and 'years' in nfl.import_sc_lines.__code__.co_varnames})

        elif function_name == 'import_draft_values':
            df = nfl.import_draft_values() # This function might take 'picks' argument based on __init__ but not on README. Assuming no args for now.

        elif function_name == 'import_team_desc':
            df = nfl.import_team_desc()

        elif function_name == 'import_contracts':
            df = nfl.import_contracts()

        elif function_name == 'import_ids':
            ids_str = payload.get('ids_ids')
            if ids_str: # Only add if provided
                kwargs['ids'] = [i.strip() for i in ids_str.split(',') if i.strip()]
                if not kwargs['ids']: kwargs.pop('ids', None)
            # Keep only 'columns' and 'ids' for this function
            valid_kwargs_ids = {k: v for k,v in kwargs.items() if k in ['columns', 'ids']}
            df = nfl.import_ids(**valid_kwargs_ids)

        elif function_name == 'import_players':
            df = nfl.import_players()
        else:
            return jsonify({'error': f"Function '{function_name}' is not implemented in the GUI."}), 400

        if df is None:
            return jsonify({'error': 'No data returned from the function call (None result).'}), 404
        # An empty DataFrame (df.empty is True) can still be valid if it has columns.
        # Only consider it an error if it's empty AND has no columns.
        if df.empty and not list(df.columns):
             return jsonify({'error': 'No data found for the given parameters (empty result with no columns).'}), 404

        df_json_data = df.to_json(orient='split')
        return jsonify({'data': df_json_data, 'columns': list(df.columns)})

    except Exception as e:
        import traceback
        print(f"Error in /search for function {payload.get('function_name', 'unknown')}: {e}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/visualize', methods=['POST'])
def visualize_data():
    try:
        data_json_str = request.form.get('data_json_str')
        viz_type = request.form.get('viz_type')
        x_axis = request.form.get('x_axis')
        y_axis = request.form.get('y_axis')
        color_by = request.form.get('color_by')

        if not all([data_json_str, viz_type, x_axis, y_axis]):
            return jsonify({'error': 'Missing required fields for visualization (data_json_str, viz_type, x_axis, y_axis).'}), 400

        try:
            data_dict = json.loads(data_json_str)
            # Reconstruct DataFrame preserving original dtypes as much as possible if they were simple
            # However, to_json(orient='split') may lose some specific dtype info if not careful.
            # Forcing numeric conversion for axes if they are not already can be problematic.
            # Let's assume Plotly Express handles dtype inference reasonably well.
            df = pd.DataFrame(data_dict['data'], columns=data_dict['columns'], index=data_dict['index'])
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Error decoding or structuring data_json_str: {e}")
            return jsonify({'error': f'Invalid data format received from client: {e}'}), 400

        if df.empty: # Check after reconstruction
            return jsonify({'error': 'Cannot visualize empty dataset.'}), 400

        if x_axis not in df.columns:
            return jsonify({'error': f"X-axis column '{x_axis}' not found in data."}), 400
        if y_axis not in df.columns:
             return jsonify({'error': f"Y-axis column '{y_axis}' not found in data."}), 400

        actual_color_by = None
        if color_by and color_by.strip() != "": # Ensure color_by is not empty string
            if color_by not in df.columns:
                return jsonify({'error': f"Color-by column '{color_by}' not found in data."}), 400
            actual_color_by = color_by

        fig = None
        title = f'{y_axis} vs. {x_axis}' if x_axis != y_axis else f'{x_axis} Distribution'
        if actual_color_by:
            title += f' by {actual_color_by}'

        # Attempt to convert selected axis columns to numeric if they aren't already,
        # but only if it makes sense for the plot type. Plotly generally handles this.
        # Forcing can cause errors if data is truly non-numeric.
        # Example: df[x_axis] = pd.to_numeric(df[x_axis], errors='ignore')
        # df[y_axis] = pd.to_numeric(df[y_axis], errors='ignore')

        if viz_type == 'scatter':
            fig = px.scatter(df, x=x_axis, y=y_axis, color=actual_color_by, title=title)
        elif viz_type == 'line':
            fig = px.line(df, x=x_axis, y=y_axis, color=actual_color_by, title=title)
        elif viz_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis, color=actual_color_by, title=title)
        elif viz_type == 'histogram':
            current_y = y_axis if y_axis != x_axis and y_axis in df.columns else None
            fig = px.histogram(df, x=x_axis, y=current_y, color=actual_color_by, title=f'Distribution of {x_axis}' + (f' (Y:{y_axis})' if current_y else '') + (f' by {actual_color_by}' if actual_color_by else ''))
        elif viz_type == 'box':
            fig = px.box(df, x=x_axis, y=y_axis, color=actual_color_by, title=title)
        else:
            return jsonify({'error': 'Invalid visualization type specified.'}), 400

        if fig:
            graph_json = fig_to_json(fig)
            return jsonify({'graph_json': graph_json})
        else:
            return jsonify({'error': 'Could not generate visualization for unspecified reasons.'}), 500

    except Exception as e:
        import traceback
        print(f"Error in /visualize: {e}\n{traceback.format_exc()}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/get_columns', methods=['GET'])
def get_columns_for_data_type():
    # data_type here refers to 'pbp' or 'weekly' for the helper functions
    data_type_param = request.args.get('data_type')
    cols = []
    if data_type_param == 'pbp':
        try:
            cols = nfl.see_pbp_cols()
        except Exception as e:
            print(f"Error calling see_pbp_cols: {e}")
            return jsonify({'error': 'Could not fetch PBP columns.'}), 500
    elif data_type_param == 'weekly':
        try:
            cols = nfl.see_weekly_cols()
        except Exception as e:
            print(f"Error calling see_weekly_cols: {e}")
            return jsonify({'error': 'Could not fetch Weekly columns.'}), 500
    # No generic column fetching for other types via this simple route for now.
    # The UI will guide users to docs for other types.
    return jsonify({'columns': cols})

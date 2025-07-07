from flask import render_template, request, jsonify
from app import app
import nfl_data_py as nfl
import plotly.express as px
import pandas as pd
import json
import plotly # For plotly.utils.PlotlyJSONEncoder
import traceback # For better error logging

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
        if years_str and years_str.strip():
            try:
                kwargs['years'] = [int(year.strip()) for year in years_str.split(',') if year.strip()]
                if not kwargs['years']: # Handle if years_str was just commas or whitespace
                    kwargs.pop('years', None)
            except ValueError:
                return jsonify({'error': 'Invalid format for years. Please provide comma-separated integers.'}), 400

        # Common 'columns' parameter
        columns_input_str = payload.get('columns_str')
        if columns_input_str and columns_input_str.strip():
            kwargs['columns'] = [col.strip() for col in columns_input_str.split(',') if col.strip()]
            if not kwargs['columns']:
                 kwargs.pop('columns', None)

        df = None
        # Helper to filter kwargs for the specific nfl_data_py function
        def get_valid_kwargs(func, current_kwargs):
            valid_arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
            return {k: v for k, v in current_kwargs.items() if k in valid_arg_names}

        if function_name == 'import_pbp_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for PBP data.'}), 400
            kwargs['include_participation'] = payload.get('pbp_include_participation') == 'true'
            kwargs['downcast'] = payload.get('pbp_downcast') == 'true'
            kwargs['cache'] = payload.get('pbp_cache') == 'true'
            kwargs['alt_path'] = payload.get('pbp_alt_path') if payload.get('pbp_alt_path', '').strip() else None
            kwargs['thread_requests'] = payload.get('pbp_thread_requests') == 'true'
            df = nfl.import_pbp_data(**get_valid_kwargs(nfl.import_pbp_data, kwargs))

        elif function_name == 'import_weekly_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Weekly data.'}), 400
            kwargs['downcast'] = payload.get('weekly_downcast') == 'true'
            kwargs['thread_requests'] = payload.get('weekly_thread_requests') == 'true'
            df = nfl.import_weekly_data(**get_valid_kwargs(nfl.import_weekly_data, kwargs))

        elif function_name == 'import_seasonal_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Seasonal data.'}), 400
            kwargs['s_type'] = payload.get('seasonal_s_type', 'REG')
            df = nfl.import_seasonal_data(**get_valid_kwargs(nfl.import_seasonal_data, kwargs))

        elif function_name == 'import_seasonal_rosters':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Seasonal Rosters.'}), 400
            df = nfl.import_seasonal_rosters(**get_valid_kwargs(nfl.import_seasonal_rosters, kwargs))

        elif function_name == 'import_weekly_rosters':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Weekly Rosters.'}), 400
            df = nfl.import_weekly_rosters(**get_valid_kwargs(nfl.import_weekly_rosters, kwargs))

        elif function_name == 'import_ngs_data':
            kwargs['stat_type'] = payload.get('ngs_stat_type')
            if not kwargs.get('stat_type'): return jsonify({'error': 'NGS Stat Type is required.'}), 400
            df = nfl.import_ngs_data(**get_valid_kwargs(nfl.import_ngs_data, kwargs))

        elif function_name == 'import_combine_data':
            positions_str = payload.get('combine_positions')
            if positions_str and positions_str.strip():
                kwargs['positions'] = [pos.strip() for pos in positions_str.split(',') if pos.strip()]
                if not kwargs['positions']: kwargs.pop('positions', None)
            df = nfl.import_combine_data(**get_valid_kwargs(nfl.import_combine_data, kwargs))

        elif function_name == 'import_draft_picks':
            if not kwargs.get('years') and nfl.import_draft_picks.__defaults__ is None or 'years' not in nfl.import_draft_picks.__code__.co_varnames[len(nfl.import_draft_picks.__code__.co_args)-len(nfl.import_draft_picks.__defaults__):]: # check if years is mandatory
                 pass # If years is optional in lib, and not provided, it's fine. UI might make it seem mandatory.
            df = nfl.import_draft_picks(**get_valid_kwargs(nfl.import_draft_picks, kwargs))


        elif function_name == 'import_qbr':
            kwargs['level'] = payload.get('qbr_level', 'nfl')
            kwargs['frequency'] = payload.get('qbr_frequency', 'season')
            df = nfl.import_qbr(**get_valid_kwargs(nfl.import_qbr, kwargs))

        elif function_name == 'import_seasonal_pfr':
            kwargs['s_type'] = payload.get('pfr_seasonal_s_type')
            if not kwargs.get('s_type'): return jsonify({'error': 'PFR Stat Type is required.'}), 400
            df = nfl.import_seasonal_pfr(**get_valid_kwargs(nfl.import_seasonal_pfr, kwargs))

        elif function_name == 'import_weekly_pfr':
            kwargs['s_type'] = payload.get('pfr_weekly_s_type')
            if not kwargs.get('s_type'): return jsonify({'error': 'PFR Stat Type is required.'}), 400
            df = nfl.import_weekly_pfr(**get_valid_kwargs(nfl.import_weekly_pfr, kwargs))

        elif function_name == 'import_snap_counts':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for Snap Counts.'}), 400
            df = nfl.import_snap_counts(**get_valid_kwargs(nfl.import_snap_counts, kwargs))

        elif function_name == 'import_ftn_data':
            if not kwargs.get('years'): return jsonify({'error': 'Years are required for FTN Data.'}), 400
            kwargs['downcast'] = payload.get('ftn_downcast') == 'true'
            kwargs['thread_requests'] = payload.get('ftn_thread_requests') == 'true'
            df = nfl.import_ftn_data(**get_valid_kwargs(nfl.import_ftn_data, kwargs))

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
            df = nfl.import_officials(**get_valid_kwargs(nfl.import_officials, kwargs))

        elif function_name == 'import_win_totals':
             df = nfl.import_win_totals(**get_valid_kwargs(nfl.import_win_totals, kwargs))

        elif function_name == 'import_sc_lines':
             df = nfl.import_sc_lines(**get_valid_kwargs(nfl.import_sc_lines, kwargs))

        elif function_name == 'import_draft_values':
            # This function might take 'picks' argument. Add if UI supports.
            df = nfl.import_draft_values(**get_valid_kwargs(nfl.import_draft_values, kwargs))


        elif function_name == 'import_team_desc':
            df = nfl.import_team_desc()

        elif function_name == 'import_contracts':
            df = nfl.import_contracts()

        elif function_name == 'import_ids':
            ids_str = payload.get('ids_ids')
            if ids_str and ids_str.strip():
                kwargs['ids'] = [i.strip() for i in ids_str.split(',') if i.strip()]
                if not kwargs['ids']: kwargs.pop('ids', None)
            df = nfl.import_ids(**get_valid_kwargs(nfl.import_ids, kwargs))

        elif function_name == 'import_players':
            df = nfl.import_players()
        else:
            return jsonify({'error': f"Function '{function_name}' is not implemented in the GUI."}), 400

        if df is None:
            return jsonify({'error': 'No data returned from the function call (None result).'}), 404
        if df.empty and not list(df.columns):
             return jsonify({'error': 'No data found for the given parameters (empty result with no columns).'}), 404

        df_json_data = df.to_json(orient='split')
        return jsonify({'data': df_json_data, 'columns': list(df.columns)})

    except Exception as e:
        print(f"Error in /search for function {payload.get('function_name', 'unknown')}: {e}\n{traceback.format_exc()}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

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
            df = pd.DataFrame(data_dict['data'], columns=data_dict['columns'], index=data_dict['index'])
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Error decoding or structuring data_json_str: {e}\n{traceback.format_exc()}")
            return jsonify({'error': f'Invalid data format received from client: {e}'}), 400

        if df.empty:
            return jsonify({'error': 'Cannot visualize empty dataset.'}), 400

        if x_axis not in df.columns:
            return jsonify({'error': f"X-axis column '{x_axis}' not found in data."}), 400
        if y_axis not in df.columns:
             return jsonify({'error': f"Y-axis column '{y_axis}' not found in data."}), 400

        actual_color_by = None
        if color_by and color_by.strip() != "":
            if color_by not in df.columns:
                return jsonify({'error': f"Color-by column '{color_by}' not found in data."}), 400
            actual_color_by = color_by

        fig = None
        title = f'{y_axis} vs. {x_axis}' if x_axis != y_axis else f'{x_axis} Distribution'
        if actual_color_by:
            title += f' by {actual_color_by}'

        # Attempt to convert to numeric where appropriate for plotting
        # This is a common source of issues if data isn't clean or has mixed types
        for col_to_convert in [x_axis, y_axis]:
            if col_to_convert in df.columns:
                try:
                    df[col_to_convert] = pd.to_numeric(df[col_to_convert])
                except ValueError:
                    print(f"Could not convert column {col_to_convert} to numeric. Plotly will attempt to handle as is.")


        if viz_type == 'scatter':
            fig = px.scatter(df, x=x_axis, y=y_axis, color=actual_color_by, title=title)
        elif viz_type == 'line':
            # For line plots, sorting by x-axis is often desirable if it's ordered (e.g., time, season)
            # df_sorted = df.sort_values(by=x_axis) if x_axis in df.columns and pd.api.types.is_numeric_dtype(df[x_axis]) else df
            fig = px.line(df, x=x_axis, y=y_axis, color=actual_color_by, title=title) # Using original df for now
        elif viz_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis, color=actual_color_by, title=title)
        elif viz_type == 'histogram':
            current_y_for_hist = y_axis if y_axis != x_axis and y_axis in df.columns else None
            fig = px.histogram(df, x=x_axis, y=current_y_for_hist, color=actual_color_by, title=f'Distribution of {x_axis}' + (f' (Y:{y_axis})' if current_y_for_hist else '') + (f' by {actual_color_by}' if actual_color_by else ''))
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
        print(f"Error in /visualize: {e}\n{traceback.format_exc()}")
        return jsonify({'error': f'An unexpected error occurred during visualization: {str(e)}'}), 500

@app.route('/get_columns', methods=['GET'])
def get_columns_for_data_type():
    data_type_param = request.args.get('data_type')
    cols = []
    error_message = None
    try:
        if data_type_param == 'pbp':
            cols = nfl.see_pbp_cols()
        elif data_type_param == 'weekly':
            cols = nfl.see_weekly_cols()
        else:
            # Not an error, just means no specific helper for this type
            return jsonify({'columns': [], 'message': 'No specific column helper for this data type.'})
    except Exception as e:
        print(f"Error calling column helper for {data_type_param}: {e}\n{traceback.format_exc()}")
        error_message = f'Could not fetch columns for {data_type_param}.'
        return jsonify({'columns': [], 'error': error_message}), 500

    return jsonify({'columns': cols})

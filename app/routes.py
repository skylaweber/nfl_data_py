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
        data_type = request.form.get('data_type')
        years_str = request.form.get('years')
        columns_str = request.form.get('columns')

        if not data_type or not years_str:
            return jsonify({'error': 'Missing required fields: data_type and years are required.'}), 400

        try:
            years = [int(year.strip()) for year in years_str.split(',')]
        except ValueError:
            return jsonify({'error': 'Invalid format for years. Please provide comma-separated integers.'}), 400

        columns = [col.strip() for col in columns_str.split(',')] if columns_str else None

        df = None
        if data_type == 'pbp':
            df = nfl.import_pbp_data(years=years, columns=columns)
        elif data_type == 'weekly':
            df = nfl.import_weekly_data(years=years, columns=columns)
        elif data_type == 'seasonal':
            s_type = request.form.get('s_type', 'REG')
            df = nfl.import_seasonal_data(years=years, s_type=s_type)
        elif data_type == 'rosters_seasonal':
            df = nfl.import_seasonal_rosters(years=years, columns=columns)
        elif data_type == 'rosters_weekly':
            df = nfl.import_weekly_rosters(years=years, columns=columns)
        elif data_type == 'draft_picks':
            df = nfl.import_draft_picks(years=years)
        elif data_type == 'combine':
            positions_str = request.form.get('positions')
            positions = [pos.strip() for pos in positions_str.split(',')] if positions_str else None
            df = nfl.import_combine_data(years=years, positions=positions)
        elif data_type == 'ngs':
            stat_type_ngs = request.form.get('stat_type_ngs')
            if not stat_type_ngs:
                 return jsonify({'error': 'Missing stat_type for NGS data.'}), 400
            df = nfl.import_ngs_data(stat_type=stat_type_ngs, years=years)
        elif data_type == 'depth_charts':
            df = nfl.import_depth_charts(years=years)
        elif data_type == 'injuries':
            df = nfl.import_injuries(years=years)
        elif data_type == 'qbr':
            level = request.form.get('qbr_level', 'nfl')
            frequency = request.form.get('qbr_frequency', 'season')
            df = nfl.import_qbr(years=years, level=level, frequency=frequency)
        elif data_type == 'snap_counts':
            df = nfl.import_snap_counts(years=years)
        elif data_type == 'ftn_data':
            df = nfl.import_ftn_data(years=years, columns=columns)
        # Add other data types as needed based on nfl_data_py library
        else:
            return jsonify({'error': 'Invalid data_type specified.'}), 400

        if df is None or df.empty:
            return jsonify({'error': 'No data found for the given parameters.'}), 404

        # For simplicity, returning JSON representation of the dataframe
        # In a more complex app, you might paginate or process this data further
        return jsonify({'data': df.to_json(orient='split'), 'columns': list(df.columns)})

    except Exception as e:
        # Log the exception e for debugging
        print(f"Error in /search: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/visualize', methods=['POST'])
def visualize_data():
    try:
        data_json = request.form.get('data_json')
        viz_type = request.form.get('viz_type')
        x_axis = request.form.get('x_axis')
        y_axis = request.form.get('y_axis')
        color_by = request.form.get('color_by') # Optional

        if not all([data_json, viz_type, x_axis, y_axis]):
            return jsonify({'error': 'Missing required fields for visualization.'}), 400

        df = pd.read_json(data_json, orient='split')

        if x_axis not in df.columns or y_axis not in df.columns:
            return jsonify({'error': 'X or Y axis not found in data columns.'}), 400
        if color_by and color_by not in df.columns:
            return jsonify({'error': 'Color-by column not found in data columns.'}), 400

        fig = None
        if viz_type == 'scatter':
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by if color_by else None, title=f'{y_axis} vs. {x_axis}')
        elif viz_type == 'line':
            fig = px.line(df, x=x_axis, y=y_axis, color=color_by if color_by else None, title=f'{y_axis} vs. {x_axis}')
        elif viz_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_by if color_by else None, title=f'{y_axis} by {x_axis}')
        elif viz_type == 'histogram':
            # Histogram typically uses one main variable, y_axis can be frequency or another aggregation
            fig = px.histogram(df, x=x_axis, y=y_axis if y_axis in df.columns and y_axis != x_axis else None, color=color_by if color_by else None, title=f'Distribution of {x_axis}')
        elif viz_type == 'box':
            fig = px.box(df, x=x_axis, y=y_axis, color=color_by if color_by else None, title=f'Box plot of {y_axis} by {x_axis}')
        else:
            return jsonify({'error': 'Invalid visualization type.'}), 400

        if fig:
            graph_json = fig_to_json(fig)
            return jsonify({'graph_json': graph_json})
        else:
            return jsonify({'error': 'Could not generate visualization.'}), 500

    except Exception as e:
        print(f"Error in /visualize: {e}")
        return jsonify({'error': str(e)}), 500

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

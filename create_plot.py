import argparse
import csv
import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_secs(time_str):
    """Get Seconds from time."""
    h = time_str.split('h')[0]
    m = time_str.split('h')[1].split('min')[0]
    s = time_str.split('h')[1].split('min')[1].split('s')[0]

    return int(h) * 3600 + int(m) * 60 + int(s)

def get_hours(time_str):
    """Get Seconds from time."""
    h = time_str.split('h')[0]
    m = time_str.split('h')[1].split('min')[0]
    s = time_str.split('h')[1].split('min')[1].split('s')[0]

    return round(int(h) + int(m) / 60 + int(s) / 3600, 2)

def conv_sec_to_timedelta(seconds):
    return str(datetime.timedelta(seconds=seconds))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""A plot script in order to 
        visualize the data in the csv file.""")

    parser.add_argument('-c', '--csv',
                        default='dsl_info.csv',
                        help='The file name of the csv with the data.')
    parser.add_argument('-d', '--csv_headers',
                        default='dsl_info_headers.csv',
                        help='The file name of the csv with the data headers.')

    # Execute parse_args()
    args = parser.parse_args()

    # Assign args
    csv_file = args.csv
    csv_headers_file = args.csv_headers

    # Dictionary for CSV data
    data = {}

    # Read CSV Headers
    with open(csv_headers_file) as csv_header_fd:
        csv_reader = csv.reader(csv_header_fd, delimiter=',')
        for row in csv_reader:
            for header in row:
                data[header] = []

    # Read CSV data
    with open(csv_file) as csv_fd:
        line = csv_fd.readline()
        while line:
            if line != '\n':
                # Tokenize each row
                tokens = line.split(',')
                
                # Append each row field to the correct data key
                i = 0
                for key in data:
                    # Convert current_date to Timestamp object
                    if key == 'current_date':
                        ts = pd.to_datetime(tokens[i].strip(), format='%Y-%m-%d %H:%M:%S', errors='ignore')
                        data[key].append(ts)
                    elif key == 'showtime_start_value':
                        secs = get_secs(tokens[i].strip())
                        hours = get_hours(tokens[i].strip())
                        # data[key].append(secs)
                        data[key].append(hours)
                    else:
                        # Try to convert the int values
                        try:
                            data[key].append(int(tokens[i].strip()))
                        # Else, save as string
                        except ValueError:
                            data[key].append(tokens[i].strip())
                    i += 1

                # print(tokens)
            line = csv_fd.readline()

    # print(data)

    # Create Dataframe from data dictionary
    df_data = pd.DataFrame.from_dict(data)
    # print(df_data)
    df_data = df_data.set_index('current_date')

    # Delete non-error like columns (TEMP)
    # try:
    #     df_data = df_data.drop(['showtime_start_value'], axis=1)
    # except KeyError:
    #     pass
    # print(df_data)


    # Create plot
    # fig = go.Figure([go.Scatter(y=df_data[key], x=df_data.index, name=df_data[key].name) for key in df_data])

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    # Add lines to figure
    for key in df_data:
        if key == 'showtime_start_value':
            # For Showtime values, add second axis
            fig.add_trace(go.Scatter(y=df_data[key], x=df_data.index, name=df_data[key].name), secondary_y=True)
            fig.update_yaxes(title_text='<b>Uptime</b> (Hours)', secondary_y=True)
        else:
            fig.add_trace(go.Scatter(y=df_data[key], x=df_data.index, name=df_data[key].name), secondary_y=False)

    # Add Titles
    fig.update_layout(title='DSL Link Info - Time Series (Logs)')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='<b>Errors</b>', secondary_y=False)

    # Create Range Selector Slider and Buttons
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1d', step='day', stepmode='backward'),
                dict(count=2, label='2d', step='day', stepmode='backward'),
                dict(count=5, label='5d', step='day', stepmode='backward'),
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(step='all')
            ])
        )
    )

    # Show figure on browser (on new port)
    # fig.show()

    # Save figure as interactive HTML
    fig.write_html("plot.html")
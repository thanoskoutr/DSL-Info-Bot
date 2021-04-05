import sys
import csv
import argparse
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # if len(sys.argv) < 3:
    #     print('Usage: '+sys.argv[0]+' <csv> <csv_headers>')
    #     exit(1)
    # csv_file = sys.argv[1]
    # csv_headers_file = sys.argv[2]

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
                    else:
                        # Try to convert the int values
                        try:
                            data[key].append(int(tokens[i].strip()))
                        # Else, save as string
                        except ValueError:
                            data[key].append(tokens[i].strip())
                    i += 1

                print(tokens)
            line = csv_fd.readline()

    print(data)

    # Create Dataframe from data dictionary
    df_data = pd.DataFrame.from_dict(data)
    print(df_data)
    df_data = df_data.set_index('current_date')
    # df_data = df_data.drop(['showtime_start_value'], axis=1) # temp
    print(df_data)

    # Create plot
    sns.set_theme(style='darkgrid')
    sns.color_palette('husl', 8)

    g = sns.lineplot(
        data=df_data,
        # col='current_date'
        # x='current_date',
        # y='errors_fec_down',
    )
    g.set(xlabel='Date', ylabel='Errors')
    plt.xticks(rotation=30)
    plt.savefig('plot.png', bbox_inches='tight')

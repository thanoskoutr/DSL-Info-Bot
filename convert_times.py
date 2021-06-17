import argparse
import csv
from pathlib import Path


def convert_to_rfc3339(timestamp):
    """
    Converts unofficial timestamp format '2021-04-01 05:15:09' to 
    RFC3339 format '2021-04-01T05:15:09Z'.
    """
    time_rfc3339 = timestamp.replace(' ', 'T')
    # Check if already in rfc3339 format
    if time_rfc3339[-1] != 'Z':
        time_rfc3339 += 'Z'
    return time_rfc3339


def convert_to_duration(time_str):
    """
    Converts time string format '27h34min51s' to a duration in
    seconds '97345'.
    """
    # Check if already in duration format
    if time_str.find('h') < 0:
        return time_str

    h = time_str.split('h')[0]
    m = time_str.split('h')[1].split('min')[0]
    s = time_str.split('h')[1].split('min')[1].split('s')[0]
    
    uptime = int(h)*3600 + int(m)*60 + int(s)
    uptime = str(uptime) + 's'

    return uptime


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""A script to convert the 
        timestamp of the csv data file to RFC3339 format and the uptime string
        in a seconds format. The script is idempotent, meaning if fields 
        already in correct format no changes are applied.""")

    parser.add_argument('-c', '--csv',
                        # default='dsl_info_w_headers.csv',
                        help='The file name of the csv with the data to be converted.')

    # Execute parse_args()
    args = parser.parse_args()

    # Check if csv option given
    if args.csv is None:
        dir_path = Path(__file__).parent.absolute()
        csv_file = dir_path.joinpath('dsl_info_w_headers.csv')
    else:
        csv_file = args.csv

    # List for CSV rows
    data_list = []

    # Read CSV data
    with open(csv_file) as csv_fd:
        csv_reader = csv.reader(csv_fd, delimiter=',')
        for row in csv_reader:
            # Convert timestamp
            time = row[-1]
            time_rfc3339 = convert_to_rfc3339(time)
            # Convert uptime (duration or long)
            uptime = row[-2]
            uptime_sec = convert_to_duration(uptime)

            new_row = row[:-2] + [uptime_sec] + [time_rfc3339]
            data_list.append(new_row)

    # Write Converted CSV data
    with open(csv_file, mode='w') as csv_fd:
            csv_writer = csv.writer(csv_fd)
            for row in data_list:
                csv_writer.writerow(row)

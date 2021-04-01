import time
import os
import sys
import argparse
from pathlib import Path

from dotenv import load_dotenv

from selenium.common.exceptions import TimeoutException
from DslLinkInfo import DslLinkInfo

def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""DSL-Info-Bot -  A python bot, 
    that uses Selenium, in order to automatically access the Router/Modem's 
    web-based setup page and get DSL Link info.""")

    parser.add_argument('-d', '--driver',
                        default='firefox',
                        choices=['firefox', 'chrome'],
                        help='The browser driver to use.')
    parser.add_argument('--headless',
                        default='True',
                        choices=['True', 'False'],
                        help='Run without a GUI.')
    parser.add_argument('-t', '--timeout', 
                        type=float,
                        default=10,
                        help='The maximum time to wait for page loading.')
    parser.add_argument('-f', '--file',
                        default='dsl_info.csv',
                        help='The file name of the csv where the data will be saved.')

    # Execute parse_args()
    args = parser.parse_args()

    # Assign args
    csv_file = args.file
    browser = args.driver
    headless = str2bool(args.headless)
    timeout = args.timeout

    # Take environment variables from .env
    load_dotenv()

    # Get Page, Username, Password
    router_page = os.environ.get('ROUTER_PAGE')
    router_username = os.environ.get('ROUTER_USERNAME')
    router_password = os.environ.get('ROUTER_PASSWORD')

    # Class object
    dsl_link_info = DslLinkInfo(headless=headless, browser=browser)

    # Log-in
    dsl_link_info.login(router_page, router_username, router_password)

    # Go to Internet Page
    try:
        dsl_link_info.internet_page('internet', timeout=timeout)
    except TimeoutException:
        print('Time out waiting for Internet page to load.')
        sys.exit(1)

    # Get DSL Link Info
    try:
        values = dsl_link_info.get_dsl_link_info('DslLinkInforBar', timeout=timeout)
        # print(values)
    except TimeoutException:
        print('Time out waiting for DSL Link Info page to load.')
        sys.exit(1)

    # Save DSL Link Info
    dir_path = Path(__file__).parent.absolute()
    csv_file_path = dir_path.joinpath(csv_file)

    # Save it in current dir
    dsl_link_info.save_dsl_link_info(csv_file_path)

    # Wait before closing
    # time.sleep(2)

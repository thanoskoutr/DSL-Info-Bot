import time
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from selenium.common.exceptions import TimeoutException
from DslLinkInfo import DslLinkInfo

# File to save error data
csv_file = 'dsl_info.csv'

if __name__ == "__main__":

    # Take environment variables from .env
    load_dotenv()

    # Get Page, Username, Password
    router_page = os.environ.get('ROUTER_PAGE')
    router_username = os.environ.get('ROUTER_USERNAME')
    router_password = os.environ.get('ROUTER_PASSWORD')

    # Class object
    dsl_link_info = DslLinkInfo(headless=True, browser='chrome')

    # Log-in
    dsl_link_info.login(router_page, router_username, router_password)

    # Go to Internet Page
    try:
        dsl_link_info.internet_page('internet')
    except TimeoutException:
        print('Time out waiting for Internet page to load.')
        sys.exit(1)

    # Get DSL Link Info
    try:
        values = dsl_link_info.get_dsl_link_info('DslLinkInforBar')
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

    # Close Driver
    # dsl_link_info.close_driver()

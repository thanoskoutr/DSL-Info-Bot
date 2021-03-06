import os
import csv
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class DslLinkInfo():
    def __init__(self, headless=True, browser='firefox'):
        if browser == 'chrome':
            options = webdriver.chrome.options.Options()
        else:
            options = webdriver.firefox.options.Options()

        if headless:
            # Run Chrome driver without GUI
            options.add_argument("--headless")

        # Select Driver
        if browser == 'chrome':
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Firefox(options=options)

    def __del__(self):
        self.driver.close()


    def login(self, router_page, router_username, router_password):
        self.driver.get(router_page)

        # Locate Form Input fields
        form_username = self.driver.find_element_by_id('Frm_Username')
        form_password = self.driver.find_element_by_id('Frm_Password')

        # Clear any pre-populated text in the input field
        form_username.clear()
        form_password.clear()

        # Enter username
        form_username.send_keys(router_username)

        # Enter password
        form_password.send_keys(router_password)
        form_password.send_keys(Keys.RETURN)


    def internet_page(self, internet_page, timeout=10):
        # Test if "Another User is configuring the device" page is shown

        # Wait for page to load (until Apply Button is loaded)
        try:
            btn_apply = WebDriverWait(self.driver, timeout/2).until(
                EC.element_to_be_clickable((By.ID, 'Btn_apply'))
            )
            # Click Internet tab
            btn_apply.click()

        except TimeoutException:
            pass

        # Wait for page to load (until Internet tab is loaded)
        try:
            nav_internet = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.ID, internet_page))
            )
            # Click Internet tab
            nav_internet.click()

        except TimeoutException:
            raise TimeoutException('Timed out waiting for page to load.')


    def get_dsl_link_info(self, dsl_link_info_bar, timeout=10):
        # Wait for page to load (until DSL Link Info bar is loaded)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.ID, dsl_link_info_bar))
            )
            # Get DSL Errors
            errors_crc = self.driver.find_element_by_id('ccrc:0')
            errors_fec = self.driver.find_element_by_id('cfec:0')
            showtime_start = self.driver.find_element_by_id('cststart:0')
            
            # Get DSL Errors Value
            errors_crc_value = errors_crc.get_attribute('title')
            errors_fec_value = errors_fec.get_attribute('title')
            showtime_start_value = showtime_start.get_attribute('title')

            # Get Up and Down Errors
            errors_crc_up = errors_crc_value.split('/')[0]
            errors_crc_down = errors_crc_value.split('/')[1]
            errors_fec_up = errors_fec_value.split('/')[0]
            errors_fec_down = errors_fec_value.split('/')[1]
            showtime_start_value = showtime_start_value.replace(' ', '')

            # Get Current Date
            current_date = time.strftime('%Y-%m-%d %H:%M:%S')

            # Return as a Dict
            self.dsl_link_info_dict = {
                'errors_crc_up': errors_crc_up,
                'errors_crc_down': errors_crc_down,
                'errors_fec_up': errors_fec_up,
                'errors_fec_down': errors_fec_down,
                'showtime_start_value': showtime_start_value,
                'current_date': current_date
            }
            return self.dsl_link_info_dict

        except TimeoutException:
            raise TimeoutException('Timed out waiting for page to load.')


    def save_dsl_link_info(self, csv_file, data=None):
        if data == None:
            data = self.dsl_link_info_dict

        # Get dictionary keys
        csv_columns = list(data.keys())

        # Save results
        with open(csv_file, mode='a') as csv_fd:
            # Create a writer object from csv module
            csv_writer = csv.DictWriter(csv_fd, fieldnames=csv_columns)
            # Add contents as last row in the csv file
            csv_writer.writerow(data)

        # Save results headers
        # Create the headers file from name of CSV file
        csv_headers_file_name = csv_file.stem + '_headers' + csv_file.suffix
        # Get CSV's path without the filename
        csv_dir_path = Path(*csv_file.parts[:-1])
        # Join CSV's path with new filename
        csv_headers_file = csv_dir_path.joinpath(csv_headers_file_name)
        with open(csv_headers_file, mode='w') as csv_fd:
            # Create a writer object from csv module
            csv_writer = csv.writer(csv_fd)
            # Add contents as last row in the csv file
            csv_writer.writerow(csv_columns)

# DSL Info Bot

## About
A python bot, that uses Selenium, in order to automatically access the Router/Modem's web-based setup page and get DSL Link info.
 
Currently gets the following info:
- CRC Errors
- FEC Errors
- Showtime_start

Support for the following Routers/Modems:
- ZTE Nova Routers (H267N, H288A, ...)

## Instalation

### Clone Repository
Clone the repo:
```bash
git clone https://github.com/thanoskoutr/DSL-Info-Bot.git
```

Change directory:
```bash
cd DSL-Info-Bot
```

### Python Virtual Environment

#### Install venv
On Debian/Ubuntu systems, you need to install the `python3-venv` package using the following command:
```bash
sudo apt-get install python3-venv
```

#### Create virtual environment
Create a virtual environment on the top directory of the project:
```bash
python3 -m venv env
```

#### Activate the virtual environment
```bash
source env/bin/activate
```

#### Install required dependencies
```bash
python3 -m pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```
Minimum Python version tested: `Python 3.6.9`
Maximum Python version tested: `Python 3.8.5`

### Download Web-Driver for Selenium
Selenium requires a driver to interface with the chosen browser. For this project the Chrome and Firefox driver is supported, used in *headless* mode in order to not require a GUI.

#### Install Chromium
In order to use the chromium driver, chromium or chrome needs to be installed. If you have already a chrome installation in your system, there is nothing to be done. Else, install a chrome version.

For Ubuntu 20.04, use `wget` to download the latest Google Chrome `.deb` package:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

Install Google Chrome package:
```bash
sudo apt install ./google-chrome-stable_current_amd64.deb
```

#### Download Chrome Driver
Download the chrome browser driver, based on the installed chromium version in your system from this link: 

https://sites.google.com/a/chromium.org/chromedriver/downloads

Check Chrome version:
```bash
google-chrome --version
```

For the Chrome version 89 driver, for Linux 64-bit, download with:
```bash
wget https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
```

Extract the driver, using `unzip`:
```bash
unzip chromedriver_linux64.zip
```

#### Install Mozilla Firefox
In order to use the firefox driver, Firefox needs to be installed. If you have already a Firefox installation in your system, there is nothing to be done. Else, install a Firefox version.

For Ubuntu/Debian Distros, install from th default package repository:
```bash
sudo apt install firefox
```

#### Download Firefox Driver
Download the Firefox browser driver, based on the installed Firefox version in your system from this link: 

https://github.com/mozilla/geckodriver/releases

Check Firefox version:
```bash
firefox --version
```

For the latest Firefox version driver, for Linux 64-bit, download with:
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
```

Extract the driver, using `tar`:
```bash
tar -zxvf geckodriver-v0.29.0-linux64.tar.gz
```

#### Add driver to PATH
In order for selenium to use the binary driver, it has to be in the `PATH` environmental variable. The preferred place for local binaries is to place the driver in the `/usr/local/bin` directory:
```bash
# For Chrome Driver
# Run from the location where your binary is downloaded and extracted
sudo mv chromedriver /usr/local/bin
# For Firefox Driver
# Run from the location where your binary is downloaded and extracted
sudo mv geckodriver /usr/local/bin
```

#### Selenium Guides - Documentation
- [Selenium with Python](https://selenium-python.readthedocs.io/index.html)
- [Selenium Documentation](https://www.selenium.dev/documentation/en/)


### Add Environmental Variables
Create the `.env` file from `.env-test`:
```bash
cp .env-test .env
```

Fill in the environmental variables needed:
- Router's web-based setup page (like `http://192.168.1.1/`)
- Router's Username
- Router's Password

```bash
ROUTER_PAGE=http://192.168.1.1/
ROUTER_USERNAME=username
ROUTER_PASSWORD=password
```

### Run Program
From the project's top directory, run:
```bash
python3 main.py
```

- A file named `dsl-info.csv` should be created in the directory that contains the fetched info.
- Firefox is the default browser, running without GUI.

#### Run Program with arguments
From the project's top directory, run with `help` option to see all available options:
```
$ python3 main.py -h

usage: main.py [-h] [-d {firefox,chrome}] [--headless {True,False}] [-t TIMEOUT] [-f FILE]

DSL-Info-Bot - A python bot, that uses Selenium, in order to automatically access the Router/Modem's web-based setup page and get DSL Link
info.

optional arguments:
  -h, --help            show this help message and exit
  -d {firefox,chrome}, --driver {firefox,chrome}
                        The browser driver to use.
  --headless {True,False}
                        Run without a GUI.
  -t TIMEOUT, --timeout TIMEOUT
                        The maximum time to wait for page loading.
  -f FILE, --file FILE  The file name of the csv where the data will be saved.
```

### Create a Cron Job
In order to run the script after a time interval on a linux machine:

Open crontab:
```bash
crontab -e
```

In order to run the script every 5 minutes, change the path to the repo accordingly:
```bash
*/5 * * * * /usr/bin/env bash -c 'export PATH="/usr/local/bin:$PATH" && source /path/to/DSL-Info-Bot/env/bin/activate && python3 /path/to/DSL-Info-Bot/main.py'

```
We need to use the bash shell in order to execute the `source` command and we need to export the `PATH` variable in order for cron to be able to find the driver.

The `dsl-info.csv` file should be created or updated in the repo directory.


## To-Do

- [ ] ! Fix waiting time (Timeout) for ButtonApply
- [ ] Create Classes for other Routers/Modems
- [ ] Check for corner cases Errors
- [ ] Add more arguments (?)
- [ ] Make Class Methods more abstract
- [ ] Add comments for Documentation
- [ ] Setup File Structure
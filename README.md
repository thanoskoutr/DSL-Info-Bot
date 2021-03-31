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
Selenium requires a driver to interface with the chosen browser. For this project the Chrome driver is used in *headless* mode in order to not require a GUI.

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

#### Add driver to PATH
In order for selenium to use the binary driver, it has to be in the `PATH` environmental variable. The preferred place for local binaries is to place the driver in the `/usr/local/bin` directory:
```bash
# Example for Chrome Driver
# Run from the location where your binary is downloaded and extracted
sudo mv chromedriver /usr/local/bin
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
A file named `dsl-info.csv` should be created in the directory that contains the fetched info.

### Create a Cron Job
In order to run the script after a time interval on a linux machine:

Open crontab:
```bash
crontab -e
```

Run script every 5 minutes:
```bash
*/5 * * * * export PATH="/usr/local/bin:$PATH" && python3 /path/to/DSL-Info-Bot/main.py
```
We export the `PATH` variable in order for cron to be able to find the driver.

The `dsl-info.csv` file should be created or updated in the repo directory.
Elite*gold exchange rate calculator
=====================
[![Python3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/) [![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/Elite-gold-exchange-rate/master/LICENSE)

A small website which tries to calculate the current elite*gold exchange rate via treasures. Using Python, [psycopg2](http://initd.org/psycopg/), [Flask](http://flask.pocoo.org/) and PostgreSQL to achieve this goal.


Configuration
-------------
Currently the only configuration is in `config.py`, copy `config.example.py` and edit the file:

    __version__ = 'v0.2b'
    userAgent = {'User-Agent': f'linux:elite*gold_price_tracker:v{__version__} (by Der-Eddy)'}

    # UNDER THIS change this variables for your enviroment
    databaseCred = {
        'host': '127.0.0.1',
        'dbname': 'epvp_treasures',
        'dbuser': 'python',
        'dbpassword': 'correcthorsebatterystaple'
    }
    __cookieJar__ = {'loginuuid': 'löaskdjfölkdfa65sdf46a5s4df56e1f23s1df32asd1f5ef1325s11bSJ9.ImRXcWNHeWI98sd5f4s65ef6s31h1fgjdfg6h54sdfasdfcvbcvb2465UrYlRORDYyTWREQThtYjBrcFEzd1wvbXZJRiswdlwvaWc5YkZSdDlMQUYzZEJIeE03SitsTFZhSFh5cGgrcHducXdzYjVMMTU5U0lGenNITitsYmdSSWIremlNU01UeVM5XC9ZaVpLSFBmaEkyU3NsZjQ1MVNDeHBvOGdaWWxGRlhmZ28raTlcL0RTYzlQaUJkc2N1alp4VW00dXJHMkd5UUttTnZQekZPa2Y1aE1qUjdHNVRwNkdyakhtNUtWc3VWYmUySVc0bkUyQ0pSWVMi.b6nMo5Q3hBMLauEsePPVNSdTJ8I5CqbZFDLrrln-oag', 'bbuserid': '5660970', 'bbpassword': '1753ec1889f70aa87845cc5bfd3b4409'}

Treasure Scraper
-------------
The second core part of this project is the treasure scraper, run `treasure.py` to start scraping treasures. At the first run the script will run in "Init mode", which will try to scrape all 351909 (as of 16.10.2018) treasures and insert the data into a PostgreSQL database.

Database Dump
-------------
Soon I will release database dumps of all treasures I scraped so far.

Requirements
-------------
On top of Python 3.6, these PyPi packages are needed:

    requests
    psycopg2

LICENSE
-------------
This project is licensed under [GPLv3](https://raw.githubusercontent.com/Der-Eddy/Elite-gold-exchange-rate/master/LICENSE).
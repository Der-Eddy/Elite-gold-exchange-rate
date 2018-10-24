Elite*gold exchange rate calculator ([elitedb.info](https://elitedb.info/))
=====================
[![Python3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/) [![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/Elite-gold-exchange-rate/master/LICENSE)

A small website which tries to calculate the current elite*gold exchange rate via treasures. Using Python, [psycopg2](http://initd.org/psycopg/), [Flask](http://flask.pocoo.org/) and PostgreSQL to achieve this goal.

Screenshots
-------------
![Homepage](https://i.imgur.com/ejAPnzM.png)

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
    jsonSavePath = '/home/eddy/Elite-gold-exchange-rate/flask/api.json'

Treasure Scripts
-------------
The second core part of this project is the treasure scraper, run `treasure.py` to start scraping treasures. At the first run the script will run in "Init mode", which will try to scrape all 351909 (as of 16.10.2018) treasures and insert the data into a PostgreSQL database.
Afterwards you can generate a new `api.json` file via `generatePrice.py`.

Cronjobs / Systemd Timer
-------------
In order to run the scripts automatically via cronjob, create a new systemd services:
`/etc/systemd/system/treasureparse.service`

    [Unit]
    Description=Epvp Treasure Parser
    After=multi-user.target
    [Service]
    WorkingDirectory=/home/eddy/Elite-gold-exchange-rate/scripts
    User=eddy
    Group=eddy
    ExecStart=/usr/bin/python3.6 /home/eddy/Elite-gold-exchange-rate/scripts/treasure.py
    ExecStartPost=/usr/bin/python3.6 /home/eddy/Elite-gold-exchange-rate/scripts/generatePrice.py
    Type=oneshot

and a timer `/etc/systemd/system/treasureparse.timer`

    [Unit]
    Description=Epvp Treasure Parser Timer

    [Timer]
    OnActiveSec=5s
    OnUnitActiveSec=6hours
    Persistent=true

    [Install]
    WantedBy=basic.target

Afterwards enable and start your new timer:

    systemctl enable --now treasureparse.timer

Hosting
-------------
To host the flask application you can use i.e. [Gunicorn](https://gunicorn.org/), a small python http server:

    /usr/local/bin/gunicorn -w 4 --bind 127.0.0.1:3030 main:app

Database Dump
-------------
I will sporadically upload database dumps into this MEGA.nz folder: [https://mega.nz/#F!hUpxAI5Y!XM_Q7ogCaIIM3inWZ8kV3A](https://mega.nz/#F!hUpxAI5Y!XM_Q7ogCaIIM3inWZ8kV3A)

You can import the dumps to your PostgreSQL database via:

    sudo -u postgres pg_restore -d {DATABASE NAME} database.dump 

Requirements
-------------
A PostgreSQL Database is required to store the treasure data, create a new user (i.e. `python` like in the example) and create a new table named `treasures` with this query:

    CREATE TABLE public.treasures (
        id bigint NOT NULL,
        sellerid bigint,
        seller bytea,
        cost bigint,
        "timestamp" timestamp without time zone,
        title bytea,
        last_updated timestamp without time zone NOT NULL,
        buyer bytea,
        buyerid bigint
    );

On top of Python 3.6, these PyPi packages are needed:

    requests
    psycopg2
    flask

LICENSE
-------------
This project is licensed under [GPLv3](https://raw.githubusercontent.com/Der-Eddy/Elite-gold-exchange-rate/master/LICENSE).
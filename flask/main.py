import os
from datetime import datetime
from flask import Flask, render_template, json
app = Flask(__name__)

@app.template_filter('timestamp_to_time')
def timestamp_to_time(s):
    return datetime.fromtimestamp(s).strftime('%d %b. %Y %H:%M')

@app.route('/')
def index():
    jsonFile = os.path.join(app.root_path, 'api.json')
    jsonData = json.load(open(jsonFile))
    return render_template('index.html', data=jsonData)
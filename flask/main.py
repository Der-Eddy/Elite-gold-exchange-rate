import os
from datetime import datetime
import git
#import requests
from flask import Flask, render_template, json, send_from_directory, jsonify
app = Flask(__name__)

jsonFile = os.path.join(app.root_path, 'api.json')
jsonData = json.load(open(jsonFile))

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha[0:7]

@app.template_filter('timestamp_to_time')
def timestamp_to_time(s):
    return datetime.fromtimestamp(s).strftime('%d %b. %Y %H:%M')

@app.route('/')
def index():
    return render_template('index.html', data=jsonData, gitHash=sha)

@app.route('/updates')
def updates():
    commits = repo.iter_commits()
    return render_template('updates.html', data=jsonData, gitHash=sha, commits=commits)

@app.route('/api.json')
@app.route('/api/v1/')
def api():
    data = {
        'idsite': '4',
        'rec': '1',
        'action_name': 'API',
        'url': '/api/v1/'
    }
    #requests.post('https://piwik.eddy-dev.net/piwik.php', data=data)
    return jsonify(jsonData)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', data=jsonData, gitHash=sha), 404
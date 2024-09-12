from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact/')
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# Nouvelle route pour afficher les commits
@app.route('/graph_commits/')
def commits():
    # URL de l'API pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    # Extraire la date des commits minute par minute
    commit_dates = []
    for commit in json_content:
        # Extraire la date dans le champ 'commit', 'author', 'date'
        date_str = commit['commit']['author']['date']
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        commit_dates.append(date_object.strftime("%Y-%m-%d %H:%M"))

    # Compter le nombre de commits par minute
    commit_counts = {}
    for date in commit_dates:
        if date in commit_counts:
            commit_counts[date] += 1
        else:
            commit_counts[date] = 1

    # Retourner les résultats sous forme de JSON pour utilisation dans le graphique
    return jsonify(commit_counts)

@app.route('/commits/')
def graph_commits():
    return render_template('commits.html')


if __name__ == "__main__":
    app.run(debug=True)

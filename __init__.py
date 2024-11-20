from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)   

@app.route("/contact/")
def contact():
    return render_template("contact.html")
  
@app.route('/')
def hello_world():
    return render_template('hello.html') #comment2  
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
  @app.route("/commits/")
def commits():
    # URL de l'API GitHub pour les commits
    github_api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # Effectuer une requête GET vers l'API GitHub
    response = requests.get(github_api_url)

    # Vérifier le statut de la réponse
    if response.status_code != 200:
        return jsonify({"error": "Impossible de récupérer les données depuis l'API GitHub"}), response.status_code

    # Extraire les données JSON
    commits_data = response.json()

    # Compter les commits par minute
    commits_per_minute = {}
    for commit in commits_data:
        commit_date = commit.get("commit", {}).get("author", {}).get("date")
        if commit_date:
            # Convertir la date en objet datetime
            date_object = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
            minute = date_object.minute

            # Compter les occurrences de chaque minute
            if minute in commits_per_minute:
                commits_per_minute[minute] += 1
            else:
                commits_per_minute[minute] = 1

    # Préparer les données pour le graphique
    results = [{"minute": str(minute), "count": count} for minute, count in commits_per_minute.items()]
    return render_template("commits.html", data=results)



if __name__ == "__main__":
  app.run(debug=True)
 
 
 

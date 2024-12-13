from flask import Flask, request
import csv
from datetime import datetime

app = Flask(__name__)

# Ruta pentru salvarea datelor trimise de clienți
@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json  # Preluăm datele în format JSON

    # Valori normale implicite
    valoare_normala_puls = "75 bpm"
    valoare_normala_tensiune = "120/80 mm Hg"
    valoare_normala_oxigen = "98 %"

    # Verificăm și înlocuim valorile lipsă cu cele implicite
    puls = f"{data['puls']} bpm" if 'puls' in data and data['puls'] else valoare_normala_puls
    tensiune = f"{data['tensiune']} mm Hg" if 'tensiune' in data and data['tensiune'] else valoare_normala_tensiune
    oxigen = f"{data['oxigen']} %" if 'oxigen' in data and data['oxigen'] else valoare_normala_oxigen

    # Deschidem fișierul CSV și salvăm datele
    with open('data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Scriem capul de tabel dacă fișierul este gol
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Activitate', 'Puls (bpm)', 'Tensiune Arterială (mm Hg)', 'Nivel Oxigen (SpO2)'])
        # Salvăm datele prelucrate
        writer.writerow([data['timestamp'], data['activitate'], puls, tensiune, oxigen])

    return 'Data saved successfully!', 200

if __name__ == '__main__':
    app.run(debug=True)

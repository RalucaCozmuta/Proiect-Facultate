import threading
import requests
import random
import time
from datetime import datetime

# Funcția pentru generarea datelor de puls și trimiterea lor la server
def send_puls_data():
    while True:
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'activitate': random.choice(["Odihnă", "Alergare", "Plimbare", "Exerciții"]),
            'puls': f"{random.randint(60, 140)} bpm"
        }
        try:
            response = requests.post('http://127.0.0.1:5000/save_data', json=data)
            if response.status_code == 200:
                print(f"Puls sent successfully: {data}")
            else:
                print(f"Error sending puls: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(random.randint(5, 15))  # Interval variabil

# Creăm fire pentru trimiterea datelor
threads = []
for _ in range(2):  # Două fire pentru puls
    thread = threading.Thread(target=send_puls_data)
    threads.append(thread)
    thread.start()

# Așteptăm firele să termine (rulează continuu)
for thread in threads:
    thread.join()


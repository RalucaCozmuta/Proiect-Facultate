import json

# Funcție pentru salvarea utilizatorilor în fișier
def save_users_to_file():
    with open("users_db.json", "w") as f:
        json.dump(users_db, f)

# Funcție pentru încărcarea utilizatorilor din fișier
def load_users_from_file():
    global users_db
    try:
        with open("users_db.json", "r") as f:
            users_db = json.load(f)
    except FileNotFoundError:
        users_db = {}

# Încărcarea utilizatorilor la începutul aplicației
load_users_from_file()

def register_user(username, password):
    if username not in users_db:
        users_db[username] = hash_password(password)
        save_users_to_file()  # Salvăm în fișier după înregistrare
        return True
    return False

# Loop principal
try:
    while True:
        if current_state == "login":
            login_screen()
        elif current_state == "register":
            register_screen()
        elif current_state == "dashboard":
            dashboard_screen()
finally:
    save_users_to_file()  # Salvăm în fișier la închiderea aplicației

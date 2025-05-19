# AJOUT DE LA VUE COACH ET USERS + UPDATE_USER
# Ajout de la vue message popup + Ajout / Update / Delete message

# ? Ajouter des ID pour les messages/sport pour les identifier
# ? Problème sur l'update de sport si deux sport identique sont disponible
# ? Ajouter une vue pour update les sports
# ? Correction des update messages / Sport (id)

import os
import json
import csv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from py122u import nfc
import time
from datetime import datetime,timedelta
import calendar

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

USERS_FILE = 'users.json'
SPORTS_FILE = 'ETA.json'
MESSAGE_FILE = 'message.json'

class NFCReader:
    def __init__(self):
        self.reader = nfc.Reader()
    
    def get_readers(self):
        return str(self.reader.instantiate_reader())
    
    def read_badge(self):
        max_retries = 10
        for attempt in range(max_retries):
            try:
                self.reader.connect()
                uid = self.reader.get_uid()
                return {"status": "success", "uid": str(uid)}
            except Exception as e:
                if attempt == max_retries - 1:
                    return {"status": "error", "message": "Aucun badge détecté, réessayez."}
                time.sleep(0.5)

nfc_reader = NFCReader()

def load_messages_test():
    with open(MESSAGE_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)['messages'] 

def load_messages():
    today = datetime.now()
    today_str = today.strftime("%d/%m/%Y")  # Format de la date : DD/MM/YYYY

    with open(MESSAGE_FILE, 'r', encoding='utf-8') as file:
        messages = json.load(file)['messages']

    valid_messages = []

    for message in messages:
        start_date = datetime.strptime(message['start_date'], "%d/%m/%Y")
        end_date = datetime.strptime(message['end_date'], "%d/%m/%Y")

        # Vérifiez si la date d'aujourd'hui est comprise entre la date de début et la date de fin
        if start_date <= today <= end_date:
            valid_messages.append(message)
    
    #print(valid_messages)

    return valid_messages

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def get_week_number():
    today = datetime.now()
    return today.strftime("%Y-W%W")

def ensure_week_directory():
    week_dir = f"data/{get_week_number()}"
    if not os.path.exists(week_dir):
        os.makedirs(week_dir)
    return week_dir

def log_activity(user_name, sport_name, category, activity_time):
    week_dir = ensure_week_directory()
    csv_file = f"{week_dir}/activities.csv"
    
    # Créer le fichier avec les en-têtes si n'existe pas
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Heure', 'Nom', 'Sport', 'Categorie'])
    
    # Ajouter l'activité
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        current_date = datetime.now().strftime("%Y-%m-%d")
        writer.writerow([current_date, activity_time, user_name, sport_name, category])

def get_sports_schedule():
    with open(SPORTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_todays_sports2():
    # Dictionnaire pour récupérer le jour actuel
    days = {
        0: "Lundi",
        1: "Mardi",
        2: "Mercredi",
        3: "Jeudi",
        4: "Vendredi",
        5: "Samedi",
        6: "Dimanche"
    }

    # Récupération du jour actuel et de l'heure actuelle
    current_day = days[datetime.now().weekday()]
    #print(current_day)

    #current_day = 'Lundi'
    current_time = datetime.now().strftime("%Hh%M")
    #current_time = '12h00'

    # Chargement du planning des sports
    schedule = get_sports_schedule()

    # Vérifier si le jour existe dans le planning
    if current_day not in schedule:
        return {}

    # Filtrage des activités selon la plage horaire (1h avant, 3h après)
    def is_within_time_range(event_time):
        event_dt = datetime.strptime(event_time, "%Hh%M")
        lower_bound = (datetime.strptime(current_time, "%Hh%M") - timedelta(hours=1))
        upper_bound = (datetime.strptime(current_time, "%Hh%M") + timedelta(hours=3))
        return lower_bound <= event_dt <= upper_bound

    filtered_schedule = {
        category: [
            event for event in events if is_within_time_range(event["time"])
        ]
        for category, events in schedule[current_day].items()
    }

    filtered_schedule["Sport en Autonomie"] = [{'id': 97, 'name': 'Course à pied', 'time': '07h00 - 20h00', 'available': True},{'id': 98, 'name': 'Musculation', 'time': '07h00 - 20h00', 'available': True}, {'id': 99, 'name': 'Cardio', 'time': '07h00 - 20h00', 'available': True}]

    print(filtered_schedule)

    # Supprimer les catégories vides
    return {k: v for k, v in filtered_schedule.items() if v}

# Fonction pour tester un jour et une heure spécifiques
def get_sports_on_day_time(day, test_time):
    schedule = get_sports_schedule()

    if day not in schedule:
        return {}

    # Vérification sur la plage horaire (1h avant, 3h après)
    def is_within_time_range(event_time):
        event_dt = datetime.strptime(event_time, "%Hh%M")
        lower_bound = (datetime.strptime(test_time, "%Hh%M") - timedelta(hours=1))
        upper_bound = (datetime.strptime(test_time, "%Hh%M") + timedelta(hours=3))
        return lower_bound <= event_dt <= upper_bound

    filtered_schedule = {
        category: [
            event for event in events if is_within_time_range(event["time"])
        ]
        for category, events in schedule[day].items()
    }

    return {k: v for k, v in filtered_schedule.items() if v}
    
def get_todays_sports():
    days = {
        0: "Lundi",
        1: "Mardi",
        2: "Mercredi",
        3: "Jeudi",
        4: "Vendredi",
        5: "Samedi",
        6: "Dimanche"
    }
    current_day = days[datetime.now().weekday()]
    #current_day = "Lundi"
    schedule = get_sports_schedule()
    daily_schedule = schedule.get(current_day, {})
    #print(daily_schedule)

    # Trier les activités par horaire dans chaque catégorie
    sorted_schedule = {}
    for category, activities in daily_schedule.items():
        sorted_activities = sorted(activities, key=lambda x: datetime.strptime(x['time'], '%Hh%M'))
        sorted_schedule[category] = sorted_activities
    #print(sorted_schedule)

    sorted_schedule["Sport en Autonomie"] = [{'id': 97, 'name': 'Course à pied', 'time': '07h00 - 20h00', 'available': True},{'id': 98, 'name': 'Musculation', 'time': '07h00 - 20h00', 'available': True}, {'id': 99, 'name': 'Cardio', 'time': '07h00 - 20h00', 'available': True}]

    return sorted_schedule

def get_todays_sports_cheat():
    # Simulation du lundi
    #return get_sports_schedule()["Lundi"]
    return get_sports_on_day_time("Lundi", "12h00")

@app.route('/')
def index():
    readers = nfc_reader.get_readers()
    messages = load_messages()
    return render_template('index.html', readers=readers, messages=messages)

@app.route('/read_badge')
def read_badge():
    result = nfc_reader.read_badge()
    if result['status'] == 'success':
        users = load_users()
        uid = result['uid']
        if uid in users:
            session['uid'] = uid  # Stocker l'UID dans la session ici
            session['user'] = users[uid]['name']  # Stocker le nom
            session['role'] = users[uid]['role']  # Stocker le rôle
            session['paid'] = users[uid]['paid']  # Stocker le status d'adhésion
            return jsonify({"status": "recognized", "redirect": url_for('dashboard')})
        else:
            session['pending_uid'] = uid
            return jsonify({"status": "unrecognized", "redirect": url_for('register')})
    return jsonify(result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'pending_uid' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        uid = session.pop('pending_uid')
        
        users = load_users()
        # Ajouter le rôle "user" par défaut
        users[uid] = {'name': name, 'role': 'user'}
        
        save_users(users)
        
        session['user'] = name
        # Ajout du role dans la session 
        session['role'] = 'user'

        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or 'uid' not in session:  # Assurez-vous que l'UID est dans la session
        return redirect(url_for('index'))
    
    # Vérifiez le rôle de l'utilisateur
    users = load_users()
    messages = load_messages()
    current_uid = session['uid']  # Utilisez l'UID de la session
    
    user_data = users.get(current_uid)  # Utilisez get() pour éviter KeyError

    if user_data and user_data['role'] == 'coach':
        todays_sports = get_todays_sports()
        #print(todays_sports)
        messages = load_messages_test()
        return render_template('dashboard_coach.html', name=session['user'], users=users, todays_sports=todays_sports, messages=messages)
    else:
        todays_sports = get_todays_sports2()
        return render_template('dashboard.html', name=session['user'], sports=todays_sports, messages=messages)

@app.route('/users')
def users_list():
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))

    users = load_users()
    todays_sports = get_todays_sports()
    #print(todays_sports)
    message = load_messages_test()
    user_list = {uid: data for uid, data in users.items()}
    return render_template('dashboard_coach.html', name=session['user'], users=user_list, todays_sports=todays_sports, messages=message)

@app.route('/update_user/<uid>', methods=['POST'])
def update_user(uid):
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))
    
    users = load_users()
    if uid in users:
        new_role = request.form.get('role')
        new_name = request.form.get('name')
        users[uid]['role'] = new_role
        users[uid]['name'] = new_name
        save_users(users)
    
    return redirect(url_for('users_list'))

@app.route('/update_message/<int:message_id>', methods=['POST'])
def update_message(message_id):
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))

    messages = load_messages_test()
    
    # Trouver et mettre à jour le message avec l'ID correspondant
    for message in messages:
        if message.get('id') == message_id:
            message['text'] = request.form.get('text')
            message['start_date'] = request.form.get('start_date')
            message['end_date'] = request.form.get('end_date')
            message['color'] = request.form.get('color')
            break
            
    with open(MESSAGE_FILE, 'w', encoding='utf-8') as file:
        json.dump({"messages": messages}, file)

    return redirect(url_for('users_list'))

@app.route('/add_message', methods=['POST'])
def add_message():
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))
    
    # Charger les messages existants
    messages = load_messages_test()
    
    # Trouver le plus grand ID existant
    max_id = 0
    if messages:
        max_id = max(msg.get('id', 0) for msg in messages)
    
    # Ajouter le nouveau message avec un nouvel ID
    messages.append({
        "id": max_id + 1,
        "text": request.form.get('text'),
        "start_date": request.form.get('start_date'),
        "end_date": request.form.get('end_date'),
        "color": request.form.get('color')
    })
    
    # Enregistrer les messages mis à jour
    with open(MESSAGE_FILE, 'w', encoding='utf-8') as file:
        json.dump({"messages": messages}, file)

    return redirect(url_for('users_list'))

@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))

    messages = load_messages_test()
    
    # Filtrer pour supprimer le message avec l'ID correspondant
    messages = [msg for msg in messages if msg.get('id') != message_id]

    with open(MESSAGE_FILE, 'w', encoding='utf-8') as file:
        json.dump({"messages": messages}, file)

    return redirect(url_for('users_list'))

@app.route('/log_activity', methods=['POST'])
def handle_activity_log():
    data = request.json
    user_name = session.get('user')
    selected_activities = data.get('activities', [])  # Liste des activités sélectionnées
    
    # Enregistrer chaque activité sélectionnée
    for activity in selected_activities:
        sport_name = activity.get('sport')
        category = activity.get('category')
        activity_time = activity.get('time')
        log_activity(user_name, sport_name, category, activity_time)
    
    return jsonify({"status": "success", "redirect": url_for('greeting')})

@app.route('/log_activity_coach', methods=['POST'])
def handle_activity_log_coach():
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))
    
    data = request.json
    user_name = data.get('user')
    selected_activities = data.get('activities', [])  # Liste des activités sélectionnées
    
    # Enregistrer chaque activité sélectionnée
    for activity in selected_activities:
        sport_name = activity.get('sport')
        category = activity.get('category')
        activity_time = activity.get('time')
        log_activity(user_name, sport_name, category, activity_time)
    
    return jsonify({"status": "success", "redirect": url_for('users_list')})

@app.route('/toggle_activity/<day>/<category>/<int:activity_id>', methods=['POST'])
def toggle_activity(day, category, activity_id):
    if 'role' not in session or session['role'] != 'coach':
        return redirect(url_for('index'))

    schedule = get_sports_schedule()
    if day in schedule and category in schedule[day]:
        for activity in schedule[day][category]:
            if activity['id'] == activity_id:  # Utilisation de l'ID au lieu du nom
                activity['available'] = not activity.get('available', True)
                break

    with open(SPORTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f)

    return redirect(url_for('users_list'))

@app.route('/greeting')
def greeting():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('greeting.html', name=session['user'], paid=session['paid'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
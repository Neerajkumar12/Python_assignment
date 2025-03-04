from flask import Flask, jsonify, request
import requests
import sqlite3

app = Flask(__name__)

# Fetch Jokes from JokeAPI and Store in Database
def fetch_and_store_jokes():
    url = "https://v2.jokeapi.dev/joke/Any?amount=100"
    response = requests.get(url)
    
    if response.status_code == 200:
        jokes = response.json().get('jokes', [])
        processed_jokes = []
        
        for joke in jokes:
            if joke['type'] == 'single':
                processed_jokes.append({
                    'category': joke['category'],
                    'type': joke['type'],
                    'joke': joke.get('joke'),
                    'setup': None,
                    'delivery': None,
                    'nsfw': joke['flags']['nsfw'],
                    'political': joke['flags']['political'],
                    'sexist': joke['flags']['sexist'],
                    'safe': joke.get('safe'),
                    'lang': joke.get('lang')
                })
            elif joke['type'] == 'twopart':
                processed_jokes.append({
                    'category': joke['category'],
                    'type': joke['type'],
                    'joke': None,
                    'setup': joke.get('setup'),
                    'delivery': joke.get('delivery'),
                    'nsfw': joke['flags']['nsfw'],
                    'political': joke['flags']['political'],
                    'sexist': joke['flags']['sexist'],
                    'safe': joke.get('safe'),
                    'lang': joke.get('lang')
                })
                
        store_jokes(processed_jokes)

def store_jokes(jokes):
    conn = sqlite3.connect('jokes.db')
    
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            type TEXT,
            joke TEXT,
            setup TEXT,
            delivery TEXT,
            nsfw BOOLEAN,
            political BOOLEAN,
            sexist BOOLEAN,
            safe BOOLEAN,
            lang TEXT
        )
    ''')
    
    cursor.executemany('''
        INSERT INTO jokes (category, type, joke, setup, delivery, nsfw, political, sexist, safe, lang)
        VALUES (:category, :type, :joke, :setup, :delivery, :nsfw, :political, :sexist, :safe, :lang)
        ''', jokes)
    
    conn.commit()
    conn.close()

@app.route('/fetch-jokes', methods=['GET'])
def fetch_jokes():
    fetch_and_store_jokes()
    return jsonify({"message": "Jokes fetched and stored successfully!"})

@app.route('/get-jokes', methods=['GET'])
def get_jokes():
    conn = sqlite3.connect('jokes.db')
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jokes")
    
    jokes = cursor.fetchall()
    
    conn.close()
    
    return jsonify(jokes)

if __name__ == '__main__':
    app.run(debug=True)

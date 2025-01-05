from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import datetime
import webbrowser
import socket
import requests
import psutil
import wikipedia
import json
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

class VirtualAssistant:
    def __init__(self):
        self.history_file = "conversation_history.json"
        self.conversation_history = []  # Initialize as an empty list
        self.r = sr.Recognizer()

    def load_history(self):
        try:
            with open(self.history_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Return an empty list if the file doesn't exist
        except json.JSONDecodeError:
            return []  # Return an empty list if the file is not a valid JSON

    def process_command(self, command):
        command = command.lower()
        response = ""
        
        if "hello" in command or "hi" in command or "hey" in command:
            response = self.greet_user()
        elif "time" in command:
            response = self.show_time()
        elif "location" in command:
            response = self.show_location()
        elif "ip" in command:
            response = self.show_ip()
        elif "open" in command:
            if "youtube" in command:
                webbrowser.open("https://www.youtube.com")
                response = "Opening YouTube..."
            elif "google" in command:
                webbrowser.open("https://www.google.com")
                response = "Opening Google..."
            elif "facebook" in command:
                webbrowser.open("https://www.facebook.com")
                response = "Opening Facebook..."
            else:
                response = "I don't know how to open that website."
        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            try:
                response = wikipedia.summary(query, sentences=2)
            except:
                response = "Sorry, I couldn't find that on Wikipedia"
        else:
            response = "I'm not sure how to help with that specific request."
        
        self.save_conversation(command, response)
        return response

    def greet_user(self):
        return "Hello! How can I help you today?"

    def show_time(self):
        return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"

    def show_location(self):
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"Your current location is {data.get('city', 'Unknown')}, {data.get('country_name', 'Unknown')}"
            else:
                return "Sorry, the location service is temporarily unavailable"
        except requests.RequestException:
            return "Sorry, I couldn't determine your location"

    def show_ip(self):
        try:
            # Get external IP
            external_ip = requests.get('https://api.ipify.org').text
            # Get local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return f"Your External IP is {external_ip}\nYour Local IP is {local_ip}"
        except:
            # Fallback to just local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return f"Your Local IP address is {local_ip}"

    def save_conversation(self, command, response):
        conversation = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "command": command,
            "response": response
        }
        self.conversation_history.append(conversation)
        
        try:
            with open(self.history_file, 'w') as file:
                json.dump(self.conversation_history, file, indent=4)
        except Exception as e:
            print(f"Error saving conversation: {e}")

assistant = VirtualAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    command = data.get('command', '')
    response = assistant.process_command(command)
    return jsonify({'response': response})

# Setup logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/virtual_assistant.log', maxBytes=10240,
                                     backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Virtual Assistant startup')

if __name__ == '__main__':
    app.run(debug=True) 
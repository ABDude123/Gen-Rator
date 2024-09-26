from flask import Flask, render_template, jsonify
import random
import string
import requests
import time

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1288888520999436361/J8n5vg-SN8wTz7M8qTv9gs9xgzI31gFkMlKKirfNFZjavnUURvkVfdPKVyexa4I30_0r'  # Replace with your webhook URL
DISCORD_API_URL = 'https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true'

# Function to generate a random 18-character alphanumeric string
def generate_random_string(length=18):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to send the generated string to the Discord API
def check_code(code):
    url = DISCORD_API_URL.format(code=code)
    response = requests.get(url)
    return response.status_code, response

# Function to send a successful code to the Discord webhook
def send_to_discord_webhook(code):
    data = {
        'content': f'Valid code found: {code}'
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code

# Home route that displays the webpage
@app.route('/')
def home():
    return render_template('index.html')

# Route to generate and check code
@app.route('/generate', methods=['GET'])
def generate_code():
    code = generate_random_string()
    status_code, response = check_code(code)
    
    if status_code == 200:
        send_to_discord_webhook(code)
        return jsonify({"code": code, "status": "Valid", "api_status": status_code})
    else:
        return jsonify({"code": code, "status": "Invalid", "api_status": status_code})

if __name__ == '__main__':
    app.run(debug=True)
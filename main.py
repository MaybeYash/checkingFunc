from flask import Flask, request, jsonify, render_template
from pyrogram import Client
from datetime import datetime
import requests

app = Flask(__name__)

API_ID = '29400566'
API_HASH = '8fd30dc496aea7c14cf675f59b74ec6f'
BOT_TOKEN = '7855855349:AAEGGWJ-M4X2wD6cReiTcGNXKzSwtWG1xuM'

app_client = Client("Techno", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_creation_date(telegram_id: int) -> str:
    url = "https://restore-access.indream.app/regdate"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
        "accept-language": "en-US,en;q=0.9"
    }
    data = {"telegramId": telegram_id}
    
    try:
        response = requests.post(url, headers=headers, json=data).json()
        if 'data' in response and 'date' in response['data']:
            return response['data']['date']
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return "N/A"

def get_user_details(identifier: str):
    with app_client:
        try:
            if identifier.isdigit():
                user = app_client.get_users(int(identifier))
            else:
                user = app_client.get_users(identifier)
            
            user_details = {
                "username": user.username,
                "first_name": user.first_name,
                "id": user.id,
                "join_date": get_creation_date(user.id)
            }
            return user_details
        except Exception as e:
            print(f"Error: {e}")
            return None

@app.route('/check', methods=['GET'])
def check_user_details():
    identifier = request.args.get('details', default=None, type=str)
    if identifier is None:
        return jsonify({"error": "Invalid input. Please provide a 'details' parameter with a valid Telegram ID or username."}), 400
    user_details = get_user_details(identifier)
    if user_details:
        return jsonify(user_details)
    else:
        return jsonify({"error": "Could not retrieve user details."}), 400

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

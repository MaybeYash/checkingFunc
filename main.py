# main.py

from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

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

@app.route('/check', methods=['POST'])
def check_join_date():
    data = request.json
    if not data or 'telegramId' not in data:
        return jsonify({"error": "Invalid input. Please provide 'TelegramId'."}), 400
    
    telegram_id = data['telegramId']
    join_date = get_creation_date(telegram_id)
    
    if join_date != "N/A":
        join_year, join_month = map(int, join_date.split('-'))
        join_date_obj = datetime(join_year, join_month, 1)
        
        now = datetime.now()
        diff_years = now.year - join_date_obj.year
        diff_months = now.month - join_date_obj.month

        if diff_months < 0:
            diff_years -= 1
            diff_months += 12

        if diff_years > 0:
            message = f"You Joined Telegram Approximately {diff_years} year{'s' if diff_years > 1 else ''} and {diff_months} month{'s' if diff_months > 1 else ''} ago!"
        else:
            message = f"You Joined Telegram Approximately {diff_months} month{'s' if diff_months > 1 else ''} ago!"
    else:
        message = "Could not retrieve your join date."
    
    return jsonify({"message": message})


@app.route('/')
def home():
    return "Telegram Join Checker..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

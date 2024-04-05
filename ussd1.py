from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import datetime

# Twilio credentials
account_sid = 'AC9200c3e6c03f20b4096087f0e342bc3e'
auth_token = '5c90ff1117c094719b8442ecf5633875'
twilio_number = '+16096421055'

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Store user's phone number and appointment details
user_data = {}

# Route to handle incoming SMS
@app.route('/sms', methods=['POST'])
def sms():
    incoming_number = request.values.get('From')
    incoming_message = request.values.get('Body')

    if incoming_number in user_data:
        # If user has sent a message before, it's considered as booking request
        appointment_time = incoming_message
        user_data[incoming_number]['appointment_time'] = appointment_time

        # Send confirmation message
        response = MessagingResponse()
        response.message(f"Thank you! Your appointment for {appointment_time} has been scheduled.")
        return str(response)

    else:
        # If it's the first message from the user, prompt for appointment
        user_data[incoming_number] = {}
        user_data[incoming_number]['phone_number'] = incoming_number

        # Prompt for appointment date and time
        response = MessagingResponse()
        response.message("Welcome! Please reply with your desired appointment date and time.")
        return str(response)

# Main function to send initial appointment booking prompt
def send_initial_prompt():
    # You may want to schedule this function to run periodically
    # or trigger it based on certain conditions

    # Example: Send initial prompt to all users who haven't booked an appointment yet
    for number in user_data:
        if 'appointment_time' not in user_data[number]:
            client.messages.create(
                body="Welcome! Please reply with your desired appointment date and time.",
                from_=twilio_number,
                to=+919591141007
            )

if __name__ == '__main__':
    # Start Flask app
    app.run(debug=True)

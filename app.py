import os
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import db, MarketPrice, Buyer, FarmerListing, InputDealer, ConversationLog
from handlers import handle_message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///farmconnect.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

# Initialize DB
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Admin Interface
admin = Admin(app, name='FarmConnect Admin', template_mode='bootstrap3')
admin.add_view(ModelView(MarketPrice, db.session))
admin.add_view(ModelView(Buyer, db.session))
admin.add_view(ModelView(FarmerListing, db.session))
admin.add_view(ModelView(InputDealer, db.session))
admin.add_view(ModelView(ConversationLog, db.session))

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    # Process the message and get response text
    response_text = handle_message(sender, incoming_msg)
    
    # Log the conversation
    log_conversation(sender, incoming_msg, response_text)
    
    # Send response back via Twilio
    resp = MessagingResponse()
    resp.message(response_text)
    return Response(str(resp), mimetype='application/xml')

def log_conversation(sender, message, response):
    try:
        # Simple intent extraction for logging (could be improved)
        intent = "unknown"
        msg_lower = message.lower()
        if msg_lower.startswith('price'): intent = 'price'
        elif msg_lower.startswith('sell'): intent = 'sell'
        elif msg_lower.startswith('crop'): intent = 'crop'
        elif msg_lower.startswith('weather'): intent = 'weather'
        elif msg_lower.startswith('inputs'): intent = 'inputs'
        elif any(x in msg_lower for x in ['hi', 'start', 'hello']): intent = 'welcome'
        
        log = ConversationLog(
            phone_number=sender,
            user_message=message,
            bot_response=response,
            intent=intent
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging conversation: {e}")

@app.route('/')
def index():
    return "FarmConnect WhatsApp Bot is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

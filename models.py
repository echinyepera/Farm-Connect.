from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MarketPrice(db.Model):
    __tablename__ = 'market_prices'
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50), nullable=False)
    market = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price_per_tonne = db.Column(db.Integer)
    price_per_kg = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source = db.Column(db.String(100))

    def __repr__(self):
        return f'<MarketPrice {self.crop} at {self.market}>'

class Buyer(db.Model):
    __tablename__ = 'buyers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_interests = db.Column(db.Text)  # Comma-separated list
    location = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Buyer {self.name}>'

class FarmerListing(db.Model):
    __tablename__ = 'farmer_listings'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)  # Hashed or plain for matching
    crop = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, matched, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    matched_buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=True)

    def __repr__(self):
        return f'<FarmerListing {self.crop} by {self.phone_number}>'

class InputDealer(db.Model):
    __tablename__ = 'input_dealers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(50))  # seed, fertilizer, chemical
    location = db.Column(db.String(100))
    address = db.Column(db.Text)
    contact_phone = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<InputDealer {self.name}>'

class ConversationLog(db.Model):
    __tablename__ = 'conversation_logs'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    user_message = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    intent = db.Column(db.String(50))  # price, sell, crop, weather, inputs
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.phone_number} - {self.intent}>'

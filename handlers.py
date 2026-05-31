from models import db, MarketPrice, Buyer, FarmerListing, InputDealer
from services.ai_service import get_crop_advice
from services.weather_service import get_weather_forecast
import re

def handle_message(sender, message):
    msg_lower = message.lower().strip()
    
    if msg_lower.startswith('price'):
        return handle_price(msg_lower)
    elif msg_lower.startswith('sell'):
        return handle_sell(sender, message)
    elif msg_lower.startswith('crop'):
        return handle_crop_advice(message)
    elif msg_lower.startswith('weather'):
        return handle_weather(msg_lower)
    elif msg_lower.startswith('inputs'):
        return handle_inputs(msg_lower)
    elif msg_lower in ['hi', 'start', 'hello', 'menu']:
        return welcome_message()
    elif msg_lower == 'help':
        return help_message()
    else:
        return help_message()

def welcome_message():
    return (
        "🌾 Welcome to FarmConnect, your farming assistant!\n\n"
        "What would you like to do?\n\n"
        "1️⃣ Check market prices\n"
        "2️⃣ Find buyers for your produce\n"
        "3️⃣ Get crop advice\n"
        "4️⃣ Weather forecast\n"
        "5️⃣ Find farm inputs\n\n"
        "Reply with a number or type your question.\n"
        "Example: 'price maize Harare' or 'sell 2 tonnes maize'"
    )

def help_message():
    return (
        "💡 FarmConnect Commands:\n\n"
        "• price [crop] [location] - Get latest prices\n"
        "• sell [quantity] [crop] [location] - Register your produce\n"
        "• crop [problem] - Get AI diagnosis\n"
        "• weather [location] - 3-day forecast\n"
        "• inputs [product] [location] - Find dealers\n\n"
        "Type 'menu' to see all options."
    )

def handle_price(message):
    # price [crop] [location]
    parts = message.split()
    if len(parts) < 3:
        return "Please provide both crop and location. Example: 'price maize Harare'"
    
    crop_query = parts[1]
    location_query = parts[2]
    
    prices = MarketPrice.query.filter(
        MarketPrice.crop.ilike(f"%{crop_query}%"),
        MarketPrice.location.ilike(f"%{location_query}%")
    ).all()
    
    if not prices:
        return f"No price data found for {crop_query} in {location_query}."
    
    response = f"🌽 {crop_query.upper()} PRICES - {location_query.upper()} REGION\n\n"
    for p in prices:
        response += f"{p.market}: ${p.price_per_tonne}/tonne\n"
    
    response += f"\nUpdated: {prices[0].updated_at.strftime('%Y-%m-%d')}\n"
    response += f"\nWant to list your {crop_query} for sale? Reply 'sell [quantity] {crop_query} {location_query}'"
    return response

def handle_sell(sender, message):
    # sell [quantity] [crop] [location]
    # Example: sell 2 tonnes maize Gokwe
    pattern = r"sell\s+(\d+)\s+(tonnes?|kg|bags?)\s+(\w+)\s+(\w+)"
    match = re.search(pattern, message.lower())
    
    if not match:
        return "Format: sell [quantity] [unit] [crop] [location]. Example: 'sell 2 tonnes maize Gokwe'"
    
    qty, unit, crop, location = match.groups()
    
    # Register listing
    new_listing = FarmerListing(
        phone_number=sender,
        crop=crop,
        quantity=float(qty),
        location=location,
        status='active'
    )
    db.session.add(new_listing)
    db.session.commit()
    
    # Find buyers
    buyers = Buyer.query.filter(
        Buyer.crop_interests.ilike(f"%{crop}%"),
        Buyer.location.ilike(f"%{location}%")
    ).limit(3).all()
    
    response = f"🚜 Your listing has been registered!\n\n"
    response += f"Crop: {crop.capitalize()}\n"
    response += f"Quantity: {qty} {unit}\n"
    response += f"Location: {location.capitalize()}\n\n"
    
    if buyers:
        response += f"Found {len(buyers)} buyers interested in {crop} in your region:\n\n"
        for i, b in enumerate(buyers, 1):
            response += f"{i}. {b.name} - {b.contact_phone}\n"
        response += "\nReply with a number to connect, or 'cancel'\n"
    else:
        response += "No immediate buyer matches found. We will notify you when a buyer is interested!"
        
    return response

def handle_crop_advice(message):
    # crop [problem description]
    problem = message[5:].strip()
    if not problem:
        return "Please describe the problem with your crop. Example: 'crop maize leaves turning yellow'"
    
    # Extract crop name if possible, or just send description to AI
    return get_crop_advice(problem)

def handle_weather(message):
    # weather [location]
    parts = message.split()
    if len(parts) < 2:
        return "Please provide a location. Example: 'weather Harare'"
    
    location = parts[1]
    return get_weather_forecast(location)

def handle_inputs(message):
    # inputs [product] [location]
    parts = message.split()
    if len(parts) < 3:
        return "Please provide product and location. Example: 'inputs maize seed Gokwe'"
    
    product = parts[1]
    location = parts[2]
    
    dealers = InputDealer.query.filter(
        InputDealer.product_type.ilike(f"%{product}%"),
        InputDealer.location.ilike(f"%{location}%")
    ).all()
    
    if not dealers:
        return f"No certified {product} dealers found in {location}."
    
    response = f"🌱 CERTIFIED {product.upper()} DEALERS - {location.upper()}\n\n"
    for i, d in enumerate(dealers, 1):
        response += f"{i}. {d.name} - {d.address}\n"
        response += f"   📞 {d.contact_phone}\n"
        if d.is_verified:
            response += "   ✅ Verified Dealer\n\n"
            
    response += "⚠️ Always verify your inputs with AgriTrace before planting."
    return response

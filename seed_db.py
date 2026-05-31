from app import app
from models import db, MarketPrice, Buyer, InputDealer

def seed_data():
    with app.app_context():
        # Clear existing data (optional, but good for seeding)
        # db.drop_all()
        # db.create_all()

        # Sample Market Prices
        prices = [
            MarketPrice(crop='Maize', market='Mbare Musika', location='Harare', price_per_tonne=450, source='MAMID'),
            MarketPrice(crop='Maize', market='Food World', location='Harare', price_per_tonne=440, source='Retail'),
            MarketPrice(crop='Maize', market='National Foods', location='Harare', price_per_tonne=460, source='ZAMACE'),
            MarketPrice(crop='Groundnuts', market='Mbare Musika', location='Harare', price_per_tonne=1200, source='MAMID'),
            MarketPrice(crop='Tomatoes', market='Mutare Produce', location='Mutare', price_per_tonne=800, source='Local'),
            MarketPrice(crop='Potatoes', market='Bulawayo Market', location='Bulawayo', price_per_tonne=750, source='Local'),
        ]

        # Sample Buyers
        buyers = [
            Buyer(name='Gokwe Grain Millers', crop_interests='maize, cotton', location='Gokwe', contact_phone='0772 123 456', is_verified=True),
            Buyer(name='Midlands Farmers Co-op', crop_interests='maize, groundnuts', location='Midlands', contact_phone='0773 789 012', is_verified=True),
            Buyer(name='National Foods Depot', crop_interests='maize, soya beans', location='Harare', contact_phone='0774 345 678', is_verified=True),
        ]

        # Sample Input Dealers
        dealers = [
            InputDealer(name='Gokwe Agriseeds', product_type='maize seed', location='Gokwe', address='CBD, opp Total Garage', contact_phone='0772 111 222', is_verified=True),
            InputDealer(name='Farm Solutions', product_type='fertilizer', location='Gokwe', address='Main Street', contact_phone='0773 333 444', is_verified=True),
        ]

        db.session.add_all(prices)
        db.session.add_all(buyers)
        db.session.add_all(dealers)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()

import sqlite3, random

conn = sqlite3.connect('gotrip.sqlite3')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS city (
                    id INTEGER PRIMARY KEY,
                    cname TEXT NOT NULL,
                    nature BOOLEAN,
                    culture BOOLEAN
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS hotel (
                    id INTEGER PRIMARY KEY,
                    hname TEXT NOT NULL,
                    price REAL,
                    id_city INTEGER NOT NULL,
                    FOREIGN KEY (id_city) REFERENCES city(id)
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS restaurant (
                    id INTEGER PRIMARY KEY,
                    rname TEXT NOT NULL,
                    price REAL,
                    rating REAL,
                    id_city INTEGER NOT NULL,
                    FOREIGN KEY (id_city) REFERENCES city(id)
                 )''')

def generate_city_data():
    cities = [('Casablanca', True, True),
              ('Rabat', True, True),
              ('Marrakech', True, True),
              ('Fes', True, True),
              ('Tangier', True, True)]
    return cities

def generate_hotel_data(num_hotels):
    hotels = []
    for _ in range(num_hotels):
        hname = f'Hotel {random.randint(1, 100)}'
        price = round(random.uniform(50, 500), 2)
        id_city = random.randint(1, 5)  # Assuming 5 cities exist in the database
        hotels.append((hname, price, id_city))
    return hotels

def generate_restaurant_data(num_restaurants):
    restaurants = []
    for _ in range(num_restaurants):
        rname = f'Restaurant {random.randint(1, 100)}'
        price = round(random.uniform(10, 100), 2)
        rating = round(random.uniform(1, 5), 1)
        id_city = random.randint(1, 5)
        restaurants.append((rname, price, rating, id_city))
    return restaurants

city_data = generate_city_data()
hotel_data = generate_hotel_data(50)  
restaurant_data = generate_restaurant_data(50) 

cursor.executemany("INSERT INTO city (cname, nature, culture) VALUES (?, ?, ?)", city_data)
cursor.executemany("INSERT INTO hotel (hname, price, id_city) VALUES (?, ?, ?)", hotel_data)
cursor.executemany("INSERT INTO restaurant (rname, price, rating, id_city) VALUES (?, ?, ?, ?)", restaurant_data)

conn.commit()

conn.close()

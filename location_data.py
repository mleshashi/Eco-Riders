# Creating DB (örneğin: location_data.db)
import sqlite3

# Connection and table creator
conn = sqlite3.connect('location_data.db')
c = conn.cursor()

# Data creating...
c.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        latitude REAL,
        longitude REAL
    )
''')

# Example datas here...
example_data = [
    ("Location 1", 49.493611, 10.988333),
    ("Location 2", 49.500000, 10.990000),
    ("Location 3", 49.480000, 10.970000)
]

c.executemany('INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)', example_data)

conn.commit()
conn.close()

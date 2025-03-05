# import sqlite3

# # Define the database file path
# db_path = "decepticon_database.db"  # Change this path if needed

# # Connect to the SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Create the table with constraints
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS experiments (
#     exp_id TEXT PRIMARY KEY,          -- Unique experiment ID
#     date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Auto-filled timestamp
#     vial_number TEXT,
#     chemicals_used TEXT,
#     rgb_values TEXT,
#     colour_change TEXT CHECK (colour_change IN ('Yes', 'No')),  -- Restrict values
#     image_path TEXT,
#     notes TEXT
# )
# """)

# # Commit and close the connection
# conn.commit()


# print(f"Database setup complete. File saved as {db_path}")


# cursor.execute("SELECT * FROM experiments")
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

# conn.close()


# import sqlite3
# import pandas

# # Define the database file path
# db_path = "decepticon_database.db"  # Change this path if needed

# # Connect to the SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Create the table with constraints (if it doesn't already exist)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS experiments (
#     exp_id TEXT PRIMARY KEY,          -- Unique experiment ID
#     date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Auto-filled timestamp
#     vial_number TEXT,
#     chemicals_used TEXT,
#     rgb_values TEXT,
#     colour_change TEXT CHECK (colour_change IN ('Yes', 'No')),  -- Restrict values
#     image_path TEXT,
#     notes TEXT
# )
# """)

# # Insert sample data (just to check)
# cursor.execute("""
#     INSERT OR IGNORE INTO experiments (exp_id, vial_number, chemicals_used, rgb_values, colour_change, image_path, notes)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("EXP001", "Vial_1", "HCl + NaOH", "(255,0,0)", "Yes", "/path/to/image.jpg", "Turned red"))

# # Commit changes to the database
# conn.commit()

# # Query to fetch all records in the table
# cursor.execute("SELECT * FROM experiments")
# rows = cursor.fetchall()

# # Print out each row in the database
# if rows:
#     for row in rows:
#         print(row)
# else:
#     print("No records found in the database.")

# # Close the connection
# conn.close()

# db_path.info()







import sqlite3
import csv

# Define the database file path
db_path = "decepticon_database.db"

# Define the CSV file path (CSV containing only RGB values)
csv_file_path = "rgb_values.csv"  # Change this to your CSV file path

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Open the CSV file and read data
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    
    # Skip header (if there is one)
    next(reader)
    
    for i, row in enumerate(reader, start=1):
        rgb_values = row[0]  # The RGB value in the first column
        
        # Generate default or placeholder values
        exp_id = f"EXP{1000 + i}"  # Generate a unique exp_id like EXP1001, EXP1002, etc.
        vial_number = f"Vial_{i}"  # Generate vial numbers like Vial_1, Vial_2, etc.
        chemicals_used = "Unknown"  # You can change this as needed or leave it as a placeholder
        colour_change = "Yes" if i % 2 == 0 else "No"  # Just an example, alternate Yes/No
        image_path = f"/path/to/image_{i}.jpg"  # Example file path
        notes = f"RGB Value {rgb_values}"  # Use the RGB value as part of the notes (or custom note)

        # Insert data into the database
        cursor.execute("""
            INSERT OR IGNORE INTO experiments (exp_id, vial_number, chemicals_used, rgb_values, colour_change, image_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            exp_id, 
            vial_number, 
            chemicals_used, 
            rgb_values, 
            colour_change, 
            image_path, 
            notes
        ))

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Data from CSV has been successfully inserted into the database.")

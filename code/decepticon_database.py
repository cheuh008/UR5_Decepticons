import sqlite3
import csv
import random
import time

# Define the database file path
db_path = "decepticon_database.db"

# Define the CSV file path (CSV containing RGB values)
csv_file_path = "RGB_values.csv"

# List of possible indicators
indicators = ["Indicator_A", "Indicator_B", "Indicator_C"]

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the experiments table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        exp_id TEXT PRIMARY KEY,
        vial_number TEXT,
        chemicals_used TEXT,
        rgb_values TEXT,
        colour_change TEXT,
        image_path TEXT,
        notes TEXT,
        successful TEXT,
        time_to_change REAL
    )
""")

# Open the CSV file and read data
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    
    # Read the header
    header = next(reader)
    
    for row in reader:
        sample_id = row[0]  # Use Sample_ID from CSV
        red, green, blue = row[1], row[2], row[3]  # Extract RGB values
        rgb_values = f"{red},{green},{blue}"  # Format as 'R,G,B'
        indicator_used = random.choice(indicators)  # Randomly select an indicator
        
        start_time = time.time()  # Start timing
        
        # Simulate colour change detection logic
        colour_change = "Yes" if int(red) > 50 else "No"  # Example logic
        successful = "Yes" if colour_change == "Yes" else "No"
        
        end_time = time.time()  # End timing
        time_to_change = round(end_time - start_time, 4)  # Calculate time taken
        
        # Insert data into the database
        cursor.execute("""
            INSERT OR IGNORE INTO experiments (exp_id, vial_number, chemicals_used, rgb_values, colour_change, image_path, notes, successful, time_to_change)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"EXP{sample_id}",  # Use Sample_ID as experiment ID
            None,  # Vial number should be pre-existing
            indicator_used, 
            rgb_values, 
            colour_change, 
            None,  # Image path should be pre-existing
            f"RGB Value: {rgb_values}", 
            successful, 
            time_to_change
        ))

# Commit the changes to the database
conn.commit()

# Fetch all data from the experiments table
cursor.execute("SELECT * FROM experiments")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)


# Close the connection
conn.close()

print("Data from CSV has been successfully inserted into the database.")


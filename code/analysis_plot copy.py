import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File path setup
csv_file = "RGB_values.csv"
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data', csv_file)

try:
    # Read CSV data
    data = pd.read_csv(file_path)
    
    # Clean column names by stripping whitespace
    data.columns = data.columns.str.strip()
    
    # Convert Time column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(data['Time']):
        data['Time'] = pd.to_datetime(data['Time'])
    
    # Plotting
    plt.figure(figsize=(12, 8))  # Slightly larger figure
    
    # Plot RGB values with different markers
    plt.plot(data['Time'], data['R'], 'r-', label='Red', marker='o', markersize=6)
    plt.plot(data['Time'], data['G'], 'g-', label='Green', marker='s', markersize=6)
    plt.plot(data['Time'], data['B'], 'b-', label='Blue', marker='^', markersize=6)
    
    # Customize plot
    plt.title('RGB Values Over Time', fontsize=16, pad=20)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Color Value (0-255)', fontsize=14)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Format x-axis
    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S\n%Y-%m-%d'))
    
    # Annotate points (only if Sample_ID is unique to avoid clutter)
    if len(data['Sample_ID'].unique()) == len(data):
        for i, row in data.iterrows():
            plt.annotate(row['Sample_ID'], 
                        (row['Time'], row['R']), 
                        textcoords="offset points",
                        xytext=(5, 5), 
                        ha='left',
                        fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.7))
    
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    print("Please ensure:")
    print(f"1. The file '{csv_file}' exists in the 'data' directory")
    print("2. The 'data' directory is in the same folder as your script")
except KeyError as e:
    print(f"Error: Missing required column - {str(e)}")
    print("Your CSV file needs these columns: 'Sample_ID', 'Time', 'R', 'G', 'B'")
    if 'data' in locals():
        print("\nDetected columns in your CSV:", data.columns.tolist())
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
    if 'data' in locals():
        print("\nFirst few rows of data:")
        print(data.head())
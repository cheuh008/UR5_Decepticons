import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import curve_fit

# File path to your CSV
csv_file = "RGB_values.csv"
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data' ,csv_file)

def plot_rgb_from_csv(csv_file):
        df = pd.read_csv(csv_file)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        for sample_id, group in df.groupby('Sample_ID'):
                plt.figure(figsize=(10,5))
                plt.plot(group['Timestamp'], group['R'], label='Red', marker='o')
                plt.plot(group['Timestamp'], group['G'], label='Red', marker='o')
                plt.plot(group['Timestamp'], group['B'], label='Red', marker='o')


                plt.xlabel("Time")
                plt.ylabel("Color Intensity")
                plt.title("RGB Values of Sample Over Time")
                plt.legend()
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

        
# Exponential decay function
# def exp_decay(t, I0, k):
    # return I0 * np.exp(-k * t)

# Function to update the plot
# def update(frame):
    # plt.cla()  # Clear the previous plot

    # Read the CSV file
    #df = pd.read_csv(file_path)

    # Ensure the CSV has required columns
    #if {"Timestamp", "R", "G", "B"}.issubset(df.columns):
        #df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        #df["Elapsed Time"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()

        # Calculate perceived brightness (luminance)
        # df["Luminance"] = 0.299 * df["R"] + 0.587 * df["G"] + 0.114 * df["B"]

        # Fit exponential decay model if enough points exist
        # if len(df) > 5:  # Need at least 5 points for a good fit
            # try:
                #popt, _ = curve_fit(exp_decay, df["Elapsed Time"], df["Luminance"], p0=(df["Luminance"].iloc[0], 0.01))
                #I0, k = popt  # Extract decay constant
                
                # Plot fitted decay curve
                #t_fit = np.linspace(df["Elapsed Time"].min(), df["Elapsed Time"].max(), 100)
                #I_fit = exp_decay(t_fit, I0, k)
                #plt.plot(df["Timestamp"], df["Luminance"], 'ko', label="Measured Intensity")  # Raw data
                #plt.plot(df["Timestamp"].iloc[0] + pd.to_timedelta(t_fit, unit='s'), I_fit, 'r-', label=f"Fit: k={k:.4f} s⁻¹")

                # Print decay rate in console
                #print(f"Decay constant (k): {k:.4f} s⁻¹")
            #except RuntimeError:
                #print("Fit failed, not enough data points or too much noise.")

        # Plot settings
        #plt.xlabel("Time")
        #plt.ylabel("Color Intensity (Luminance)")
        #plt.title("Reaction Kinetics: Color Fading Over Time")
        #plt.xticks(rotation=45)
        #plt.legend()
        #plt.grid(True)

# Set up the animation
#fig = plt.figure(figsize=(10, 5))
#ani = animation.FuncAnimation(fig, update, interval=1000)  # Update every second

#plt.show()

import pandas as pd

# This script is not working

# Load the Excel file
input_file_path = r"C:\Users\cheta\OneDrive\Chetan\Destiny\archive\nifty_50_1day_1min.xlsx"
df = pd.read_excel(input_file_path)

# Display the original DataFrame (optional, for verification)
print("Original DataFrame:")
print(df.head())

# Rename columns to match required format
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# Convert the 'date' column to datetime using automatic parsing
df['datetime'] = pd.to_datetime(df['date'], errors='coerce')

# Check for any parsing errors (optional)
if df['datetime'].isnull().any():
    print("Some dates could not be parsed. Please check the format.")
    print(df[df['datetime'].isnull()])

# Separate date and time into two columns and explicitly convert types
df['date'] = df['datetime'].dt.date  # Extract date part
df['time'] = df['datetime'].dt.time  # Extract time part

# Explicitly convert 'time' and 'date' columns to the correct dtype
df['time'] = pd.to_datetime(df['time'].astype(str), format='%H:%M:%S').dt.time
df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y-%m-%d').dt.date

# Drop the 'datetime' column as it's no longer needed
df.drop(columns=['datetime'], inplace=True)

# Reorder columns to match required format
df = df[['high', 'volume', 'time', 'date', 'close', 'low', 'open']]

# Save the processed DataFrame back to an Excel file
output_file_path = r"C:\Users\cheta\OneDrive\Chetan\Destiny\archive\processed_nifty_50_data.xlsx"
df.to_excel(output_file_path, index=False)

# Print confirmation
print(f"Processed data saved to {output_file_path}")

# Inspect the DataFrame's structure and column data types again
df.info() # date column is still object



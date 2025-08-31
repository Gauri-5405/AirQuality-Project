import pandas as pd
import os

# -------------------------------
# 1. Read & Combine All CSV Files
# -------------------------------
folder_path = r"C:\Users\Gauri Saraf\Desktop\AirQuality\AirQualityData.csv"  
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

dfs = []
for file in all_files:
    file_path = os.path.join(folder_path, file)
    # Use low_memory=False to avoid dtype warnings
    dfs.append(pd.read_csv(file_path, low_memory=False))

# Combine all files into one DataFrame
df = pd.concat(dfs, ignore_index=True)
print("Original Shape:", df.shape)

# -------------------------------
# 2. Drop Useless Columns
# -------------------------------
drop_cols = ["StationId", "StationName", "Status", "Datetime"]  # drop extra if not useful
df = df.drop(columns=drop_cols, errors="ignore")

# -------------------------------
# 3. Convert Date Column
# -------------------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.sort_values('Date')

# -------------------------------
# 4. Handle Missing Values
# -------------------------------
# Drop rows with too many NaNs (keep rows with at least 5 valid values)
df = df.dropna(thresh=5)

# Forward fill remaining NaNs (useful for time-series)
df = df.fillna(method='ffill')

# -------------------------------
# 5. Remove Duplicates
# -------------------------------
df = df.drop_duplicates()

# -------------------------------
# 6. Clip Outliers (based on valid AQI ranges)
# -------------------------------
if 'PM2.5' in df.columns:
    df['PM2.5'] = df['PM2.5'].clip(lower=0, upper=500)
if 'PM10' in df.columns:
    df['PM10']  = df['PM10'].clip(lower=0, upper=600)
if 'NO2' in df.columns:
    df['NO2']   = df['NO2'].clip(lower=0, upper=400)
if 'SO2' in df.columns:
    df['SO2']   = df['SO2'].clip(lower=0, upper=400)
if 'CO' in df.columns:
    df['CO']    = df['CO'].clip(lower=0, upper=50)

# -------------------------------
# 7. Standardize Text Columns
# -------------------------------
if 'City' in df.columns:
    df['City'] = df['City'].astype(str).str.strip().str.title()
if 'State' in df.columns:
    df['State'] = df['State'].astype(str).str.strip().str.title()
if 'AQI_Bucket' in df.columns:
    df['AQI_Bucket'] = df['AQI_Bucket'].astype(str).str.strip().str.title()

# -------------------------------
# 8. Final Checks
# -------------------------------
print("\nCleaned Dataset Info:")
print(df.info())
print("\nMissing Values Per Column:")
print(df.isnull().sum())
print("\nSummary Statistics:")
print(df.describe())

# -------------------------------
# 9. Save Cleaned Data
# -------------------------------
output_file = os.path.join(folder_path, "Clean_AirQualityData.csv")
df.to_csv(output_file, index=False)
print(f"\n✅ Cleaned dataset saved to: {output_file}")

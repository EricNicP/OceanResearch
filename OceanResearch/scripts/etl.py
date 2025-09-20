import netCDF4 as nc
import pandas as pd
from pathlib import Path

def extract_profile(file_path, profile_idx=0):
    """Extract key variables from a NetCDF file for a specific profile."""
    try:
        with nc.Dataset(file_path, 'r') as ds:
            data = {}
            for var in ['TEMP', 'PSAL', 'PRES', 'LATITUDE', 'LONGITUDE']:
                if var in ds.variables:
                    data[var] = ds.variables[var][profile_idx, :].flatten() if var in ['TEMP', 'PSAL', 'PRES'] else ds.variables[var][profile_idx]
            return data
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def transform_data(data):
    """Transform extracted data into a DataFrame."""
    return pd.DataFrame({
        'Pressure': data.get('PRES', []),
        'Temperature': data.get('TEMP', []),
        'Salinity': data.get('PSAL', [])
    })

def save_to_csv(df, output_path):
    """Save DataFrame to CSV."""
    if df is not None and not df.empty:
        df.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")
    else:
        print(f"No data to save for {output_path}")

def main():
    input_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/data/raw')
    output_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    files = ['D6901930_001.nc', 'D6901758_001.nc']
    for file in files:
        file_path = input_dir / file
        if file_path.exists():
            for profile_idx in range(2):  # Process both profiles
                data = extract_profile(file_path, profile_idx)
                if data:
                    df = transform_data(data)
                    output_path = output_dir / f"{file_path.stem}_profile{profile_idx}_processed.csv"
                    save_to_csv(df, output_path)
                else:
                    print(f"Skipping {file} (profile {profile_idx}): No data extracted")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()


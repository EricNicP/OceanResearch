import netCDF4 as nc
import matplotlib.pyplot as plt
from pathlib import Path

def plot_profile(file_path, profile_idx=0):
    """Plot temperature vs. pressure for a given profile."""
    try:
        with nc.Dataset(file_path, 'r') as ds:
            if 'PRES' in ds.variables and 'TEMP' in ds.variables:
                pres = ds.variables['PRES'][profile_idx, :].flatten()
                temp = ds.variables['TEMP'][profile_idx, :].flatten()
                plt.figure(figsize=(8, 6))
                plt.plot(temp, pres, marker='o', linestyle='-', label=f'Profile {profile_idx}')
                plt.gca().invert_yaxis()  # Depth increases downward
                plt.xlabel('Temperature (°C)')
                plt.ylabel('Pressure (dbar)')
                plt.title(f'Temperature vs. Depth - {file_path.name}')
                plt.grid(True)
                plt.legend()
                output_path = f'C:/Users/Lenovo/Desktop/OceanResearch/data/processed/{file_path.stem}_profile{profile_idx}_plot.png'
                plt.savefig(output_path)
                print(f"Saved plot to {output_path}")
                plt.show()
    except Exception as e:
        print(f"Error plotting {file_path}: {e}")

def main():
    data_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/data/raw')
    output_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    files = ['D6901930_001.nc', 'D6901758_001.nc']
    for file in files:
        file_path = data_dir / file
        if file_path.exists():
            for profile_idx in range(2):  # Plot both profiles
                plot_profile(file_path, profile_idx)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()


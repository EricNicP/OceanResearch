import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_profile(csv_path):
    """Plot temperature vs. pressure from a CSV."""
    try:
        df = pd.read_csv(csv_path)
        plt.figure(figsize=(8, 6))
        plt.plot(df['Temperature'], df['Pressure'], marker='o', linestyle='-', label=csv_path.stem)
        plt.gca().invert_yaxis()  # Depth increases downward
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Pressure (dbar)')
        plt.title(f'Temperature vs. Depth - {csv_path.stem}')
        plt.grid(True)
        plt.legend()
        output_path = csv_path.parent / f"{csv_path.stem}_plot.png"
        plt.savefig(output_path)
        print(f"Saved plot to {output_path}")
        plt.show()
    except Exception as e:
        print(f"Error plotting {csv_path}: {e}")

def main():
    data_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/data/processed')
    csv_files = [
        'D6901930_001_profile0_processed.csv',
        'D6901930_001_profile1_processed.csv',
        'D6901758_001_profile0_processed.csv',
        'D6901758_001_profile1_processed.csv'
    ]
    for csv_file in csv_files:
        csv_path = data_dir / csv_file
        if csv_path.exists():
            plot_profile(csv_path)
        else:
            print(f"File not found: {csv_path}")

if __name__ == "__main__":
    main()

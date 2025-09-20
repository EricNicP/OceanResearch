from flask import Flask
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    # Use the actual location where your PNG files are
    data_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/data/processed')
    static_dir = Path('C:/Users/Lenovo/Desktop/OceanResearch/download.py/FloatChat/static')
    
    # Debug
    print(f"Static directory: {static_dir}")
    print(f"Static directory exists: {static_dir.exists()}")
    
    if static_dir.exists():
        all_files = list(static_dir.iterdir())
        print(f"All files in static: {[f.name for f in all_files]}")
        png_files = [f.name for f in all_files if f.suffix.lower() == '.png']
    else:
        png_files = []
    
    csv_files = [f.name for f in data_dir.glob('*.csv')] if data_dir.exists() else []
    
    print(f"PNG files found: {png_files}")
    print(f"CSV files found: {csv_files}")
    
    # Return HTML directly
    html = "<h1>ARGO Float Data</h1>"
    html += "<h2>CSV Files</h2><ul>"
    for csv in csv_files:
        html += f"<li>{csv}</li>"
    html += "</ul><h2>Plots</h2>"
    
    for png in png_files:
        html += f'<img src="/static/{png}" alt="{png}" width="500"><br>'
    
    return html

# Serve static files from the correct location
@app.route('/static/<path:filename>')
def static_files(filename):
    from flask import send_file
    return send_file(f'C:/Users/Lenovo/Desktop/OceanResearch/download.py/FloatChat/static/{filename}')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

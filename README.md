# OceanResearch
ARGO float data processing pipeline
## Usage Instructions

1. **Download data**: `python download.py`
2. **Inspect files**: `python inspect.py`
3. **Process data**: `python etl.py`
4. **Generate plots**: `python plot.py`
5. **Launch web app**: `python app.py`

## Data Sources
- Primary: ftp.ifremer.fr/ifremer/argo
- Backup: HTTP endpoints for specific ARGO floats

## Dependencies
- netCDF4
- pandas
- matplotlib
- flask
- requests

## Features
- Robust data downloading with failover
- NetCDF to CSV conversion
- Temperature/pressure profile visualization
- Web-based data browser

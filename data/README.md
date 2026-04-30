# Data Folder

Place raw files in `data/raw/` and processed outputs in `data/processed/`.

Default file names used in notebooks:
- bmkg.csv
- bps.csv
- osm.csv
- bnpb.csv
- kelurahan.csv

If your file names or formats differ, update the paths and columns in the notebooks.

Minimal columns expected (adjust as needed):
- kelurahan: string or id
- date: ISO date for time series
- numeric indicators for climate, infrastructure, socioeconomic

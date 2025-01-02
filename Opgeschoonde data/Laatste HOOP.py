import pandas as pd

# Define file paths and types
file_paths = {
    "FossilGasPower": "cleaned_data_fossilgaspower.xlsx",
    "Solar": "cleaned_data_solar.xlsx",
    "Wind": "cleaned_data_wind.xlsx",
    "WindOffshore": "cleaned_data_windoffshore.xlsx"
}

# Define province mapping
province_mapping = {
    0: "Nederland",
    1: "Groningen",
    2: "Friesland",
    3: "Drenthe",
    4: "Overijssel",
    5: "Flevoland",
    6: "Gelderland",
    7: "Utrecht",
    8: "Noord-Holland",
    9: "Zuid-Holland",
    10: "Zeeland",
    11: "Noord-Brabant",
    12: "Limburg",
    14: "Offshore",
    28: "Windpark Luchterduinen",
    29: "Windpark Princes Amalia",
    30: "Windpark Egmond aan Zee",
    31: "Windpark Gemini",
    33: "Windpark Borselle I&II",
    34: "Windpark Borselle III&IV",
    35: "Windpark Hollandse Kust Zuid",
    36: "Windpark Hollandse Kust Noord",
}

# Initialize an empty list to store results
results = []

# Process each file
for type_name, file_path in file_paths.items():
    # Load data
    data = pd.read_excel(file_path)
    
    # Ensure column names are standardized
    data.columns = data.columns.str.strip().str.lower()
    
    # Check if necessary columns exist
    if 'point' in data.columns and 'volume' in data.columns:
        # Map province names
        data['provincie'] = data['point'].map(province_mapping)
        
        # Group by province and calculate total volume
        summary = data.groupby('provincie')['volume'].sum().reset_index()
        summary['type'] = type_name
        
        # Append to results
        results.append(summary)
    else:
        print(f"Skipping {file_path}: Missing 'point' or 'volume' columns.")

# Combine all results
final_summary = pd.concat(results, ignore_index=True)

# Save to Excel
output_path = "total_volume_per_province.xlsx"
final_summary.to_excel(output_path, index=False)

print(f"Aggregated data saved to {output_path}")
import pandas as pd

# Pad naar de 4 opgeschoonde Excel-bestanden
excel_files = [
    'Opgeschoonde data\cleaned_fossilgaspower_data.xlsx',
    'Opgeschoonde data\cleaned_offshore_wind_data.xlsx',
    'Opgeschoonde data\cleaned_solar_data.xlsx',
    'Opgeschoonde data\cleaned_wind_data.xlsx'
]

# Lees de Excel-bestanden in
data_frames = [pd.read_excel(file) for file in excel_files]

# Combineer de dataframes in één groot dataframe (indien van toepassing)
df = pd.concat(data_frames, ignore_index=True)

# Bekijk de eerste paar rijen en kolommen om te zien hoe de data eruit ziet
print(df.head())
print(df.columns)

# We gaan ervan uit dat de kolommen 'volume' (energie) en 'emissionfactor' (emissiefactor) bestaan.
# Voeg de volgende nieuwe kolommen toe:

# 1. Totale energieopwekking (som van de volume voor alle bronnen)
df['totale_energieopwekking'] = df.groupby('type')['volume'].transform('sum')

# 2. Percentage opwekking per bron
df['percentage_opwekking'] = (df['volume'] / df['totale_energieopwekking']) * 100

# 3. Totale CO2-uitstoot (som van de CO2-uitstoot voor alle bronnen)
df['co2_uitstoot'] = df['volume'] * df['emissionfactor']
df['totale_co2'] = df['co2_uitstoot'].sum()

# 4. Percentage CO2-uitstoot per bron
df['percentage_co2'] = (df['co2_uitstoot'] / df['totale_co2']) * 100

# Sla het gewijzigde DataFrame op in een nieuw Excel-bestand
output_excel_file = 'output_file_with_new_variables.xlsx'
df.to_excel(output_excel_file, index=False)

print(f"Nieuwe variabelen toegevoegd en opgeslagen in {output_excel_file}")

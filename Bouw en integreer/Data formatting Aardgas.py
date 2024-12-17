import pandas as pd
import datetime

# Excel bestand namen bepalen
input_excel_file = "Data formatting\cleaned_fossilgaspower_data.xlsx"  
output_excel_file = "formatted_data.xlsx" 

# Datumbereik bepalen
today = datetime.date.today()
last_week = today - datetime.timedelta(days=20)

# Data uit het excel bestand lezen
try:
    df = pd.read_excel(input_excel_file)
    print(f"Data geladen uit {input_excel_file}")
except FileNotFoundError:
    print(f"Het bestand {input_excel_file} bestaat niet. Zorg ervoor dat het bestand in dezelfde map staat.")
    exit()

# Data formatting acties
# 'validfrom' en 'validto' naar datetime-formaat veranderen
if 'validfrom' in df.columns:
    df['validfrom'] = pd.to_datetime(df['validfrom'], errors='coerce')
if 'validto' in df.columns:
    df['validto'] = pd.to_datetime(df['validto'], errors='coerce')


# 'volume' naar numeriek en check op NaN-waarden
if 'volume' in df.columns:
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce') 
    
    # Check op NaN-waarden in de 'volume' kolom
    nan_volume = df['volume'].isna().sum()  
    print(f"Aantal NaN-waarden in de 'volume' kolom: {nan_volume}")
    
    # Vervang NaN-waarden door een standaardwaarde, gemiddelde 
    df['volume'].fillna(df['volume'].mean(), inplace=True) 

    

# Controleer of de 'volume' kolom correct is geconverteerd naar numeriek
if pd.api.types.is_numeric_dtype(df['volume']):
    print("De 'volume' kolom is succesvol geconverteerd naar een numeriek type.")
else:
    print("Er is een probleem met de conversie van de 'volume' kolom naar een numeriek type.")



# Volledigheid, vul missende waarden in
missing_values = df.isnull().sum().sum()  
df.fillna({
    'classification': 2, 
    'granularity': 5,  
    'activity': 1,  
}, inplace=True)

# Vul missende tijdstempels in
if 'validfrom' in df.columns:
    df['validfrom'].fillna(df['validfrom'].min(), inplace=True)
if 'validto' in df.columns:
    df['validto'].fillna(df['validto'].max(), inplace=True)

# Consistentie, controleren of validto groter is dan validfrom
consistency_issues = df[df['validto'] < df['validfrom']].shape[0]
df.loc[df['validto'] < df['validfrom'], 'validto'] = df['validfrom'] + pd.Timedelta(hours=1)

# Validiteit, ongeldige waarden verwijderen
valid_classifications = [1, 2, 3]
valid_granularities = [3, 4, 5, 6, 7, 8]
valid_activities = [1, 2]

invalid_classifications = df[~df['classification'].isin(valid_classifications)].shape[0]
invalid_granularities = df[~df['granularity'].isin(valid_granularities)].shape[0]
invalid_activities = df[~df['activity'].isin(valid_activities)].shape[0]

df = df[df['classification'].isin(valid_classifications)]
df = df[df['granularity'].isin(valid_granularities)]
df = df[df['activity'].isin(valid_activities)]

# omzetten naar numerieke waarden
if 'energy_value' in df.columns:
    df['energy_value'] = pd.to_numeric(df['energy_value'], errors='coerce')

# Uniciteit, duplicaten verwijderen
duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

# Actualiteit, controleren op datumbereiken buiten de gewenste
if 'validfrom' in df.columns:
    df = df[(df['validfrom'] >= str(last_week)) & (df['validfrom'] < str(today))]

# Data opslaan naar een nieuw excel-bestand
df.to_excel(output_excel_file, index=False)
print(f"Geformatteerde data opgeslagen in {output_excel_file}")

# Resultaten weergeven
print("\nData quality check resultaten:")
print(f"- Totaal aantal missende waarden: {missing_values}")
print(f"- Aantal inconsistenties (validto < validfrom): {consistency_issues}")
print(f"- Aantal ongeldige classificaties: {invalid_classifications}")
print(f"- Aantal ongeldige granulariteiten: {invalid_granularities}")
print(f"- Aantal ongeldige activiteiten: {invalid_activities}")
print(f"- Aantal duplicaten verwijderd: {duplicates}")
print(f"- Aantal Not a number waarden in de kolom volume: {nan_volume}")
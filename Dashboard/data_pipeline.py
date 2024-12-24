import pandas as pd
import glob

# Combineer alle Excel-bestanden
files = glob.glob(r"C:\Users\vanpu\OneDrive\Documenten\GitHub\E-Map-Gasunie\Opgeschoonde data.xlsx")
combined_data = pd.concat([pd.read_excel(f) for f in files])

# Controleer op duplicaten en opschonen
combined_data = combined_data.drop_duplicates()

# Opslaan als één bestand
combined_data.to_csv("combined_data.csv", index=False)
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# Te wijzigen parameters voor invoer- en uitvoerbestanden
input_file = 'Opgeschoonde data/cleaned_data_windoffshore.xlsx'
output_file_predictions = 'voorspellingen_2025.xlsx'

# Inlezen van gegevensbestand
data = pd.read_excel(input_file)

# Omzetten van kolommen naar datetime-formaat en verwijderen van ongeldige datums
data['validfrom'] = pd.to_datetime(data['validfrom'], errors='coerce')
data['validto'] = pd.to_datetime(data['validto'], errors='coerce')
data = data.dropna(subset=['validfrom', 'validto'])

# Extractie van tijdgerelateerde kenmerken
data['hour'] = data['validfrom'].dt.hour
data['day'] = data['validfrom'].dt.day
data['month'] = data['validfrom'].dt.month
data['year'] = data['validfrom'].dt.year

# Selectie van invoer- en uitvoerkenmerken voor het model
features = ['point', 'hour', 'day', 'month', 'year']
X = data[features]
y = data['volume']

# Coderingsproces voor categorische gegevens in 'point'
label_encoder_point = LabelEncoder()
X['point'] = label_encoder_point.fit_transform(X['point'])

# Training van een Random Forest-model
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(X, y)

# Genereren van toekomstige gegevens voor voorspellingen
points = data['point'].unique()
date_range = pd.date_range(start='2025-01-01', end='2025-12-31 23:59:59', freq='H')
future_data = pd.DataFrame(
    [(point, dt) for point in points for dt in date_range],
    columns=['point', 'datetime']
)

# Toevoegen van tijdkenmerken aan toekomstige gegevens
future_data['hour'] = future_data['datetime'].dt.hour
future_data['day'] = future_data['datetime'].dt.day
future_data['month'] = future_data['datetime'].dt.month
future_data['year'] = future_data['datetime'].dt.year
future_data = future_data.drop(columns=['datetime'])

# Coderingsproces toepassen op toekomstige gegevens
future_data['point'] = label_encoder_point.transform(future_data['point'])

# Toepassen van het model op toekomstige gegevens
predictions = model.predict(future_data)
future_data['predicted_volume'] = predictions

# Opslaan van de voorspellingen naar een Excel-bestand
future_data.to_excel(output_file_predictions, index=False)
print(f"Voorspellingen zijn opgeslagen in '{output_file_predictions}'.")

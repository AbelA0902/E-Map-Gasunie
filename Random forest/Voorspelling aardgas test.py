import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 1. Laad de data
file_path = 'cleaned_fossilgaspower_data.xlsx'  # Vervang met benodigde bestand
data = pd.read_excel(file_path)

# 2. Selecteer relevante kolommen
selected_columns = ['capacity', 'emissionfactor', 'validfrom', 'timezone', 'activity', 'classification', 'volume', 'point']
prepared_data = data[selected_columns]

# 3. Verwerk tijdsgerelateerde informatie
prepared_data['hour'] = prepared_data['validfrom'].dt.hour
prepared_data['day'] = prepared_data['validfrom'].dt.day
prepared_data['month'] = prepared_data['validfrom'].dt.month
prepared_data = prepared_data.drop(columns=['validfrom'])

# 4. Splits features en doelvariabele
X = prepared_data.drop(columns=['volume', 'point'])
y = prepared_data['volume']

# 5. Splits data in training- en testsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train het Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Maak voorspellingen en evalueer het model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model evaluatie:\nMean Squared Error: {mse}\nR^2 Score: {r2}")

# 8. Genereer data voor november volgend jaar
next_year = pd.Timestamp.now().year + 1
date_range = pd.date_range(start=f'{next_year}-11-01', end=f'{next_year}-11-30 23:00', freq='H')
future_data = pd.DataFrame({
    'validfrom': date_range,
    'capacity': np.random.choice(data['capacity'], size=len(date_range), replace=True),
    'emissionfactor': np.random.choice(data['emissionfactor'], size=len(date_range), replace=True),
    'timezone': np.random.choice(data['timezone'], size=len(date_range), replace=True),
    'activity': np.random.choice(data['activity'], size=len(date_range), replace=True),
    'classification': np.random.choice(data['classification'], size=len(date_range), replace=True),
    'point': np.random.choice(data['point'], size=len(date_range), replace=True)
})

# Verwerk tijdsgerelateerde informatie
future_data['hour'] = future_data['validfrom'].dt.hour
future_data['day'] = future_data['validfrom'].dt.day
future_data['month'] = future_data['validfrom'].dt.month

# Selecteer relevante features
X_toekomstig = future_data[['capacity', 'emissionfactor', 'timezone', 'activity', 'classification', 'hour', 'day', 'month']]

# Maak voorspellingen
voorspellingen = model.predict(X_toekomstig)

# Voeg voorspellingen toe aan de dataset
future_data['voorspelling'] = voorspellingen

# Selecteer de gewenste kolommen en hernoem 'validfrom' naar 'date'
output_data = future_data[['point', 'emissionfactor', 'validfrom', 'voorspelling']].rename(columns={'validfrom': 'date'})

# Voeg een lege volume-kolom toe omdat de echte waarden niet bekend zijn
output_data['volume'] = None  # Geen echte waarden beschikbaar

# Orden de kolommen zoals gewenst
output_data = output_data[['volume', 'point', 'emissionfactor', 'date', 'voorspelling']]

# Sla de resultaten op in een Excel-bestand
output_data.to_excel('voorspellingen_november_volgend_jaar.xlsx', index=False)
print(f"Voorspellingen opgeslagen in 'voorspellingen_november_volgend_jaar.xlsx' voor november {next_year}.")

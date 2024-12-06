import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Laad je dataset
file_path_train = 'Random forest\cleaned_fossilgaspower_data.xlsx'  # Pas het bestandspad aan
prepared_data_train = pd.read_excel(file_path_train)

# Data preprocessing
# Zorg ervoor dat de juiste datatypes worden ingesteld voor datetime kolommen
prepared_data_train['validfrom'] = pd.to_datetime(prepared_data_train['validfrom'])
prepared_data_train['validto'] = pd.to_datetime(prepared_data_train['validto'])

# Voeg kolommen voor uur, dag en maand toe
prepared_data_train['hour'] = prepared_data_train['validfrom'].dt.hour
prepared_data_train['day'] = prepared_data_train['validfrom'].dt.day
prepared_data_train['month'] = prepared_data_train['validfrom'].dt.month

# Selecteer de benodigde kolommen
prepared_data_train = prepared_data_train[['point', 'volume', 'emissionfactor', 'validto', 'hour', 'day', 'month']]

# Stel de features (X) en de target (y) in
X = prepared_data_train[['volume', 'emissionfactor', 'hour', 'day', 'month']]
y = prepared_data_train['point']

# Split de data in trainings- en testset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Maak het model en train het
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Maak voorspellingen
y_pred = model.predict(X_test)

# Model evaluatie
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model evaluatie:")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Voeg de voorspelling toe aan de data
prepared_data_train['prediction'] = model.predict(X)

# Maak een nieuw DataFrame voor de uiteindelijke output
output_data = prepared_data_train[['point', 'volume', 'emissionfactor', 'validto', 'hour', 'day', 'month', 'prediction']]

# Zet de 'validto' kolom om naar een leesbare datum/tijd
output_data['validto'] = pd.to_datetime(output_data['validto'], errors='coerce')

# Zet de 'hour', 'day', 'month' in één kolom genaamd 'date'
output_data['date'] = output_data.apply(lambda row: f"{row['day']}-{row['month']}-{row['hour']}", axis=1)

# Verwijder de 'hour', 'day', 'month' kolommen nu ze gecombineerd zijn
output_data = output_data.drop(columns=['hour', 'day', 'month'])

# Exporteer de uiteindelijke data naar een nieuw Excel-bestand
output_data.to_excel('voorspelling_output.xlsx', index=False)

print("De voorspellingen zijn succesvol geëxporteerd naar 'voorspelling_output.xlsx'")

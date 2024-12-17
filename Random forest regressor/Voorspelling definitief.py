import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Kun je veranderen om verschillende bestanden op te halen en vervolgens op te schonen. keuze uit: fossilgaspower, solar, wind, windoffshore
input_file = 'Opgeschoonde data/cleaned_data_windoffshore.xlsx'
output_file_predictions = 'voorspellingen_2025.xlsx'

# Inlezen van gekozen bestand
data = pd.read_excel(input_file)

# Omzetten van kolommen naar datetime-formaat en verwijderen van ongeldige datums
data['validfrom'] = pd.to_datetime(data['validfrom'], errors='coerce')
data['validto'] = pd.to_datetime(data['validto'], errors='coerce')
data = data.dropna(subset=['validfrom', 'validto'])

data['hour'] = data['validfrom'].dt.hour
data['day'] = data['validfrom'].dt.day
data['month'] = data['validfrom'].dt.month
data['year'] = data['validfrom'].dt.year
 
# Voeg lagged features toe op basis van de kolom 'volume'
data['volume_lag1'] = data['volume'].shift(1)  # Volume van 1 uur geleden
data['volume_lag24'] = data['volume'].shift(24)  # Volume van 24 uur geleden

# Verwijder rijen met ontbrekende waarden (door lagged kolommen)
data = data.dropna(subset=['volume', 'volume_lag1', 'volume_lag24'])

# Kenmerken en doelvariabele instellen
features = ['point', 'hour', 'day', 'month', 'year']
X = data[features]
y = data['volume']

# Coderingsproces voor categorische gegevens in 'point'
label_encoder_point = LabelEncoder()
X['point'] = label_encoder_point.fit_transform(X['point'])

# Split de data in een training- en testset (80% training, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Splitsen van data in een training- (80%) en testset (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=69)

# Model initialiseren en trainen
model = RandomForestRegressor(random_state=150, n_estimators=150)
model.fit(X_train, y_train)

# Testen van het model op de testset
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error op de testset: {mse}")
print(f"R²-score op de testset: {r2}")

# Bestand maken voor voorspellingdata
points = data['point'].unique()
date_range = pd.date_range(start='2025-01-01', end='2025-12-31 23:59:59', freq='H')
future_data = pd.DataFrame(
    [(point, dt) for point in points for dt in date_range],
    columns=['point', 'datetime']
)

# Toevoegen van datum en tijd nieuwe bestand
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

# Opslaan van de voorspellingen in een Excel-bestand
future_data.to_excel(output_file_predictions, index=False)
print(f"Voorspellingen zijn opgeslagen in '{output_file_predictions}'.")

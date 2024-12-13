import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Data inladen vanuit een Excel-bestand
data = pd.read_excel('Opgeschoonde data\cleaned_data_solar.xlsx')

# Converteer 'validfrom' en 'validto' naar datetime
data['validfrom'] = pd.to_datetime(data['validfrom'], errors='coerce')
data['validto'] = pd.to_datetime(data['validto'], errors='coerce')

# Controleer op ontbrekende waarden
if data['validfrom'].isna().any() or data['validto'].isna().any(): 
    print("Waarschuwing: Sommige datetime-waarden zijn ongeldig. Controleer de data.")
    data = data.dropna(subset=['validfrom', 'validto'])  # Verwijder rijen met ongeldige datums indien nodig

# Maak tijdgerelateerde features
data['hour'] = data['validfrom'].dt.hour
data['day'] = data['validfrom'].dt.day
data['month'] = data['validfrom'].dt.month
data['year'] = data['validfrom'].dt.year
 
# Voeg lagged features toe op basis van de kolom 'volume'
data['volume_lag1'] = data['volume'].shift(1)  # Volume van 1 uur geleden
data['volume_lag24'] = data['volume'].shift(24)  # Volume van 24 uur geleden

# Verwijder rijen met ontbrekende waarden (door lagged kolommen)
data = data.dropna(subset=['volume', 'volume_lag1', 'volume_lag24'])

# Selecteer relevante kolommen voor model
features = ['point', 'hour', 'day', 'month', 'year', 'volume_lag1', 'volume_lag24']
X = data[features]  # Input-features
y = data['volume']  # Doelvariabele

# Encodeer categorische kolom 'point'
label_encoder_point = LabelEncoder()
X['point'] = label_encoder_point.fit_transform(X['point'])

# Split de data in een training- en testset (80% training, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train een Random Forest-model
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Maak voorspellingen voor de testset
y_pred = model.predict(X_test)

# Bereken evaluatiescores (R² en MSE)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred) 

print(f'R²: {r2}')
print(f'MSE: {mse}')

# Maak een toekomstig dataset voor voorspellingen (2025)
points = data['point'].unique()  # Unieke punten uit de data
date_range = pd.date_range(start='2025-01-01', end='2025-12-31 23:59:59', freq='h')  # Elk uur van 2025

# Maak een DataFrame voor alle combinaties van punten en tijdstippen
future_data = pd.DataFrame(
    [(point, dt) for point in points for dt in date_range],
    columns=['point', 'datetime']
)

# Voeg tijdsfeatures toe aan toekomstig dataset
future_data['hour'] = future_data['datetime'].dt.hour
future_data['day'] = future_data['datetime'].dt.day
future_data['month'] = future_data['datetime'].dt.month
future_data['year'] = future_data['datetime'].dt.year

# Voeg placeholders toe voor lagged features en voorspellingen
future_data['volume_lag1'] = np.nan
future_data['volume_lag24'] = np.nan
future_data['predicted_volume'] = np.nan

# Initialiseer lagged waarden met de laatste bekende volumes uit de oorspronkelijke dataset
last_known_volumes = data.tail(24)  # Laatste 24 uur
initial_lag1 = last_known_volumes['volume'].iloc[-1]
initial_lag24 = last_known_volumes['volume'].iloc[-24]

for idx in range(len(future_data)):
    if idx == 0:
        # Eerste voorspelling: gebruik laatste bekende waarden
        future_data.loc[idx, 'volume_lag1'] = initial_lag1
        future_data.loc[idx, 'volume_lag24'] = initial_lag24
    else:
        # Gebruik voorspellingen van eerdere iteraties
        future_data.loc[idx, 'volume_lag1'] = future_data.loc[idx - 1, 'predicted_volume']
        if idx >= 24:
            future_data.loc[idx, 'volume_lag24'] = future_data.loc[idx - 24, 'predicted_volume']
        else:
            future_data.loc[idx, 'volume_lag24'] = initial_lag24

    # Bereid features voor de voorspelling
    row_features = future_data.loc[idx, ['point', 'hour', 'day', 'month', 'year', 'volume_lag1', 'volume_lag24']]
    row_features['point'] = label_encoder_point.transform([row_features['point']])[0]  # Encodeer 'point'

    # Maak een DataFrame met dezelfde kolommen als het trainingsmodel
    row_features = pd.DataFrame([row_features], columns=features)

    # Maak voorspelling en sla op
    future_data.loc[idx, 'predicted_volume'] = model.predict(row_features)[0]

# Exporteer resultaten naar Excel
future_data.to_excel('voorspellingen_2025.xlsx', index=False)

print("Voorspellingen zijn opgeslagen in 'voorspellingen_2025.xlsx'.")

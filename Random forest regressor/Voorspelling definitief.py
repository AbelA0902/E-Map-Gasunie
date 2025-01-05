import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Kun je veranderen om verschillende bestanden op te halen en vervolgens op te schonen. keuze uit: fossilgaspower, solar, wind, windoffshore
input_file = 'Powerbi data\WindoffshoreDashboard.xlsx'
output_file_predictions = 'RandomForestWindOffshore2025.xlsx'

# Inlezen van gekozen bestand
data = pd.read_excel(input_file)

# Omzetten van kolommen naar datetime-formaat en verwijderen van ongeldige datums
data['validfrom'] = pd.to_datetime(data['validfrom'], errors='coerce')
data = data.dropna(subset=['validfrom'])  # Verwijder rijen zonder geldige datum

# Voeg datumgebaseerde kenmerken toe
data['day'] = data['validfrom'].dt.day
data['month'] = data['validfrom'].dt.month
data['year'] = data['validfrom'].dt.year
data['weekday'] = data['validfrom'].dt.weekday

# Voeg weekday toe na het groeperen
daily_data = data.groupby(['year', 'month', 'day']).agg({'volume': 'mean'}).reset_index()

# Voeg weekday toe aan daily_data
daily_data['weekday'] = pd.to_datetime(daily_data[['year', 'month', 'day']]).dt.weekday

# Voeg lagged features toe
daily_data['volume_lag1'] = daily_data['volume'].shift(1)
daily_data['volume_lag7'] = daily_data['volume'].shift(7)

# Verwijder ontbrekende waarden door lags
daily_data = daily_data.dropna(subset=['volume_lag1', 'volume_lag7'])

# Voeg normalisatie toe voor alleen lagged features
scaler = StandardScaler()
daily_data[['volume', 'volume_lag1', 'volume_lag7']] = scaler.fit_transform(daily_data[['volume', 'volume_lag1', 'volume_lag7']])

# Selecteer features en target
features = ['day', 'month', 'weekday', 'volume_lag1', 'volume_lag7']
target = 'volume'

# Splits de data in train- en testsets
X = daily_data[features]
y = daily_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train een Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Voorspel op de testset
y_pred = model.predict(X_test)

# Bereken de prestaties van het model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Maak een DataFrame voor de voorspellingen voor heel 2025
dates_2025 = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
predictions_2025 = []

for date in dates_2025:
    day = date.day
    month = date.month
    year = date.year
    weekday = date.weekday()
    volume_lag1 = daily_data.loc[(daily_data['year'] == year) & (daily_data['month'] == month) & (daily_data['day'] == day - 1), 'volume'].values
    volume_lag7 = daily_data.loc[(daily_data['year'] == year) & (daily_data['month'] == month) & (daily_data['day'] == day - 7), 'volume'].values
    
    if len(volume_lag1) == 0:
        volume_lag1 = [0]
    if len(volume_lag7) == 0:
        volume_lag7 = [0]
    
    features_2025 = pd.DataFrame({
        'day': [day],
        'month': [month],
        'weekday': [weekday],
        'volume_lag1': volume_lag1,
        'volume_lag7': volume_lag7
    })
    
    prediction = model.predict(features_2025)
    # Denormaliseer de voorspelling
    prediction_denorm = scaler.inverse_transform([[prediction[0], volume_lag1[0], volume_lag7[0]]])[0][0]
    predictions_2025.append([date, prediction_denorm])

# Zet de voorspellingen om in een DataFrame en voeg een unieke ID toe
predictions_df = pd.DataFrame(predictions_2025, columns=['date', 'predicted_volume'])
predictions_df['id'] = predictions_df.index + 1

# Sla de voorspellingen op als een Excel-bestand
predictions_df.to_excel(output_file_predictions, index=False)

print("Voorspellingen voor 2025 succesvol opgeslagen in", output_file_predictions)

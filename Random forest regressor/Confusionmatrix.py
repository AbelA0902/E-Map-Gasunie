import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Dataset laden
file_path = "Random forest regressor/voorspellingen_2025_windoffshore.xlsx"
data = pd.read_excel(file_path)

# Controleer de eerste paar rijen om te zien hoe de kolommen eruitzien
print("Dataset Preview:")
print(data.head())

# 2. Selecteer de juiste kolommen voor X (features) en y (target)
# We gaan ervan uit dat kolom G, H en I de juiste kolommen zijn
X = data.iloc[:, [6, 7]]  # Kolom G en H (0-gebaseerd indexeren, dus 6 en 7 voor G en H)
y = data.iloc[:, 8]       # Kolom I (de target)

# 3. Controleer de datatypes om te zorgen dat de kolommen geschikt zijn voor het model
print("\nData types of the selected features and target:")
print(X.dtypes)
print(y.dtypes)

# 4. Train-Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 5. Model trainen
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 6. Voorspellingen maken
y_pred = clf.predict(X_test)

# 7. Confusion Matrix berekenen
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# 8. Confusion Matrix visualiseren
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.xlabel('Voorspelde labels')
plt.ylabel('Werkelijke labels')
plt.title('Confusion Matrix')
plt.show()

# 9. Accuraatheid en classificatie-rapport
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy Score:", accuracy)

classification_report_str = classification_report(y_test, y_pred)
print("\nClassification Report:")
print(classification_report_str)

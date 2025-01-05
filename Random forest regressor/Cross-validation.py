import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Dataset laden
file_path = "Opgeschoonde data/cleaned_data_windoffshore.xlsx"
data = pd.read_excel(file_path)

# Controleer de eerste paar rijen
print("Dataset Preview:")
print(data.head())

# 2. Stel features (X) en target (y) in
X = data.iloc[:, :-1]  # Alle kolommen behalve de laatste
y = data.iloc[:, -1]   # Laatste kolom als target

# 3. Train-Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# Cross-validation instellen
clf_cv = RandomForestClassifier(n_estimators=100, random_state=42)

# Gebruik StratifiedKFold voor consistente verdelingen
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(clf_cv, X_train, y_train, cv=cv, scoring='accuracy')

print("\nCross-Validation Scores:")
print(cv_scores)
print("Gemiddelde CV-score:", cv_scores.mean())


import numpy as np
import matplotlib.pyplot as plt

#data gebaseerd op CBS data
categories = {
    "Bad": [4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5],
    "Douche": [50, 50.5, 51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5],
    "Toilet": [35, 35.2, 35.5, 35.7, 36, 36.3, 36.5, 36.8, 37, 37.2],
    "Vaatwasser": [3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.2, 4.3, 4.4],
    "Wasmachine": [10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9],
    "Consumptie": [2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4],
    "Buiten": [4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8],
}

years = np.arange(2022, 2022 + 10)
#data plotten voor visualisatie 
plt.figure(figsize=(12, 8))

for category, usage in categories.items():
    plt.plot(years, usage, marker='o', label=category)

# opmaak
plt.title("Voorspelling Watergebruik per Categorie (liters per dag)", fontsize=16)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Watergebruik (liters per dag)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Categorieën", fontsize=12)
plt.xticks(years, rotation=45)
plt.tight_layout()

plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Dataset: Gemiddeld watergebruik (voorbeeld in liters per dag)
# Data kan worden aangepast aan de categorieën in jouw dataset
data = {
    "Winter": {"mean": 120, "std": 5},
    "Lente": {"mean": 130, "std": 6},
    "Zomer": {"mean": 140, "std": 8},
    "Herfst": {"mean": 125, "std": 5},
}

# Simulatieparameters
n_simulations = 10000  # Aantal simulaties
future_years = 10  # Aantal jaren om te voorspellen
simulated_averages = []

# Monte Carlo-simulatie
for year in range(future_years):
    yearly_average = 0
    for season, stats in data.items():
        mean = stats["mean"]
        std = stats["std"]
        # Simuleer watergebruik voor een seizoen
        simulated_season = np.random.normal(mean, std, n_simulations)
        # Neem het gemiddelde van het gesimuleerde seizoen
        yearly_average += np.mean(simulated_season)
    # Voeg het jaargemiddelde toe
    simulated_averages.append(yearly_average / 4)  # Gemiddelde van 4 seizoenen

# Visualiseer de voorspelling
years = np.arange(2022, 2022 + future_years)

plt.figure(figsize=(12, 6))
plt.plot(years, simulated_averages, marker='o', label="Gemiddeld watergebruik")
plt.fill_between(
    years,
    np.array(simulated_averages) - 5,  # Schatting onzekerheid (voorbeeld)
    np.array(simulated_averages) + 5,
    color='b',
    alpha=0.2,
    label="Onzekerheidsinterval"
)
plt.title("Voorspelling gemiddeld watergebruik per persoon", fontsize=16)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Gemiddeld watergebruik (liters per dag)", fontsize=14)
plt.grid(True)
plt.legend(fontsize=12)
plt.show()

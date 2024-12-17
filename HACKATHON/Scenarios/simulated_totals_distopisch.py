import numpy as np
import matplotlib.pyplot as plt

# Slechter watermanagement: verwachte stijging in waterverbruik
data_distopisch = {
    "Douche": {"mean": 50, "increase_rate": 0.20},  # 20% meer in 10 jaar
    "Toilet": {"mean": 35, "increase_rate": 0.15},  # 15% meer in 10 jaar
    "Overig": {"mean": 24.5, "increase_rate": 0.10},  # 10% meer in 10 jaar
}

# Parameters voor de simulatie
n_simulations = 10000  # Hoe vaak wordt gesimuleerd
future_years = 10  # Voorspelling voor 10 jaar vooruit
simulated_totals_distopisch = []

# Simuleer waterverbruik voor de komende 10 jaar
for year in range(future_years):
    yearly_total = 0
    for stats in data_distopisch.values():
        mean = stats["mean"] * (1 + stats["increase_rate"] * (year / future_years))  # Jaarlijkse stijging
        std = mean * 0.1  # Onzekerheid is 10% van de waarde
        simulated_category = np.random.normal(mean, std, n_simulations)  # Maak simulaties
        yearly_total += np.mean(simulated_category)  # Voeg gemiddelde toe
    simulated_totals_distopisch.append(yearly_total)

# Maak de grafiek van het distopische scenario
years = np.arange(2022, 2022 + future_years)

plt.figure(figsize=(12, 6))
plt.plot(years, simulated_totals_distopisch, marker='o', color='red', label="Distopisch scenario: Totaal watergebruik")
plt.fill_between(
    years,
    np.array(simulated_totals_distopisch) - 5,  # Onzekerheidsmarge
    np.array(simulated_totals_distopisch) + 5,
    color='red',
    alpha=0.2,
    label="Onzekerheidsinterval"
)
plt.title("Distopisch Scenario: Voorspelling Watergebruik (liters per dag)", fontsize=16)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Totaal watergebruik (liters per dag)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

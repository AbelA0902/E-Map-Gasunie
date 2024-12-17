import numpy as np
import matplotlib.pyplot as plt

# Neutraal scenario: lichte toename in watergebruik over 10 jaar
data_neutraal = {
    "Douche": {"mean": 50, "increase_rate": 0.05},  # Doucheverbruik stijgt met 5% in 10 jaar
    "Toilet": {"mean": 35, "increase_rate": 0.03},  # Toiletverbruik stijgt met 3% in 10 jaar
    "Overig": {"mean": 24.5, "increase_rate": 0.02},  # Overig gebruik stijgt met 2% in 10 jaar
}

# Instellingen voor de simulatie
n_simulations = 10000  # Aantal keer dat de simulatie wordt uitgevoerd
future_years = 10  # Voorspelling over 10 jaar
simulated_totals_neutraal = []

# Simuleer waterverbruik voor de komende jaren
for year in range(future_years):
    yearly_total = 0
    for stats in data_neutraal.values():
        # Bereken het gemiddelde waterverbruik met de kleine stijging
        mean = stats["mean"] * (1 + stats["increase_rate"] * (year / future_years))
        std = mean * 0.1  # Onzekerheid is 10% van de waarde
        simulated_category = np.random.normal(mean, std, n_simulations)  # Simulaties uitvoeren
        yearly_total += np.mean(simulated_category)  # Gemiddelde optellen
    simulated_totals_neutraal.append(yearly_total)  # Voeg totaalverbruik toe

# Maak een grafiek van de resultaten
years = np.arange(2022, 2022 + future_years)

plt.figure(figsize=(12, 6))
plt.plot(years, simulated_totals_neutraal, marker='o', color='blue', label="Neutraal scenario: Totaal watergebruik")
plt.fill_between(
    years,
    np.array(simulated_totals_neutraal) - 5,  # Onzekerheidsinterval
    np.array(simulated_totals_neutraal) + 5,
    color='blue',
    alpha=0.2,
    label="Onzekerheidsinterval"
)
plt.title("Neutraal Scenario: Voorspelling Watergebruik (liters per dag)", fontsize=16)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Totaal watergebruik (liters per dag)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

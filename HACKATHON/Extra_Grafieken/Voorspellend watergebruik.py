import numpy as np
import matplotlib.pyplot as plt

# Gemiddeld waterverbruik per maand (CBS-data)
data = {
    "Winter": {"mean": 120, "std": 5},
    "Lente": {"mean": 130, "std": 6},
    "Zomer": {"mean": 140, "std": 8},
    "Herfst": {"mean": 125, "std": 5},
}

n_simulations = 10000  
future_years = 10  
simulated_averages = []

# Simuleer het gemiddelde waterverbruik over 10 jaar
for year in range(future_years):
    yearly_average = 0
    for stats in data.values():
        simulated_season = np.random.normal(stats["mean"], stats["std"], n_simulations)
        yearly_average += np.mean(simulated_season)  
    simulated_averages.append(yearly_average / 4)  


years = np.arange(2022, 2022 + future_years)

plt.figure(figsize=(12, 6))
plt.plot(years, simulated_averages, marker='o', label="Gemiddeld watergebruik")
plt.fill_between(
    years,
    np.array(simulated_averages) - 5,  # Schatting van onzekerheid
    np.array(simulated_averages) + 5,
    color='b',
    alpha=0.2,
    label="Onzekerheidsinterval"
)
plt.title("Voorspelling van gemiddeld watergebruik per persoon (liters per dag)", fontsize=16)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Gemiddeld watergebruik (liters per dag)", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

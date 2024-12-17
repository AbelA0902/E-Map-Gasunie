import numpy as np
import matplotlib.pyplot as plt

# Data uit jouw dataset (voorbeeld met type huishouden)
data = {
    "Eenpersoons": {"mean": 186, "std": 4},
    "Paar zonder kinderen": {"mean": 129, "std": 3},
    "Paar met kinderen": {"mean": 110, "std": 3},
    "Eenouderhuishouden": {"mean": 109, "std": 7},
    "Huishouden > 4 personen": {"mean": 96, "std": 5}
}

# Simulatieparameters
n_simulations = 10000  # Aantal simulaties
simulated_results = {}

# Monte Carlo-simulatie
for group, stats in data.items():
    mean = stats["mean"]
    std = stats["std"]
    # Simuleer waterverbruik met normale verdeling
    simulated_results[group] = np.random.normal(mean, std, n_simulations)

# Visualisatie van de resultaten
plt.figure(figsize=(12, 8))
for group, results in simulated_results.items():
    plt.hist(results, bins=50, alpha=0.6, label=group)

# Grafiekopmaak
plt.title("Monte Carlo-simulatie van waterverbruik per huishoudenstype", fontsize=16)
plt.xlabel("Waterverbruik per persoon (liters)", fontsize=14)
plt.ylabel("Frequentie", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

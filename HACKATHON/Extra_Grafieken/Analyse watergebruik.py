import numpy as np
import matplotlib.pyplot as plt

data = {
    "Eenpersoons": {"mean": 186, "std": 4},
    "Paar zonder kinderen": {"mean": 129, "std": 3},
    "Paar met kinderen": {"mean": 110, "std": 3},
    "Seniorenwoning (1-persoon)": {"mean": 109, "std": 7},
    "Huishouden > 4 personen": {"mean": 96, "std": 5}
}


n_simulations = 10000  #aantal simulaties 
simulated_results = {}


for group, stats in data.items(): #monte carlo modle
    mean = stats["mean"]
    std = stats["std"]
    simulated_results[group] = np.random.normal(mean, std, n_simulations) #verdeling sumleren met normale verdelng
#visualiseren
plt.figure(figsize=(12, 8))
for group, results in simulated_results.items():
    plt.hist(results, bins=50, alpha=0.6, label=group)

#opmaak
plt.title("Monte Carlo-simulatie van waterverbruik per huishoudenstype", fontsize=16)
plt.xlabel("Waterverbruik per persoon (liters)", fontsize=14)
plt.ylabel("Frequentie waarnemingen", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

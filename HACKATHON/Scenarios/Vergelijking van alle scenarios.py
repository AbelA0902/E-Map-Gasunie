import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Simulatieparameters
n_simulations = 10000
future_years = 10
years = np.arange(2022, 2022 + future_years)

# Utopisch scenario
data_utopisch = {
    "Douche": {"mean": 50, "reduction_rate": 0.30},
    "Toilet": {"mean": 35, "reduction_rate": 0.40},
    "Overig": {"mean": 24.5, "reduction_rate": 0.10},
}

simulated_totals_utopisch = []
for year in range(future_years):
    yearly_total = 0
    for stats in data_utopisch.values():
        mean = stats["mean"] * (1 - stats["reduction_rate"] * (year / future_years))
        std = mean * 0.1
        simulated_category = np.random.normal(mean, std, n_simulations)
        yearly_total += np.mean(simulated_category)
    simulated_totals_utopisch.append(yearly_total)

# Neutraal scenario
data_neutraal = {
    "Douche": {"mean": 50, "increase_rate": 0.05},
    "Toilet": {"mean": 35, "increase_rate": 0.03},
    "Overig": {"mean": 24.5, "increase_rate": 0.02},
}

simulated_totals_neutraal = []
for year in range(future_years):
    yearly_total = 0
    for stats in data_neutraal.values():
        mean = stats["mean"] * (1 + stats["increase_rate"] * (year / future_years))
        std = mean * 0.1
        simulated_category = np.random.normal(mean, std, n_simulations)
        yearly_total += np.mean(simulated_category)
    simulated_totals_neutraal.append(yearly_total)

# Distopisch scenario
data_distopisch = {
    "Douche": {"mean": 50, "increase_rate": 0.20},
    "Toilet": {"mean": 35, "increase_rate": 0.15},
    "Overig": {"mean": 24.5, "increase_rate": 0.10},
}

simulated_totals_distopisch = []
for year in range(future_years):
    yearly_total = 0
    for stats in data_distopisch.values():
        mean = stats["mean"] * (1 + stats["increase_rate"] * (year / future_years))
        std = mean * 0.1
        simulated_category = np.random.normal(mean, std, n_simulations)
        yearly_total += np.mean(simulated_category)
    simulated_totals_distopisch.append(yearly_total)

# Vloeiendere lijnen
x_new = np.linspace(years.min(), years.max(), 300)
utopisch_smooth = make_interp_spline(years, simulated_totals_utopisch)(x_new)
neutraal_smooth = make_interp_spline(years, simulated_totals_neutraal)(x_new)
distopisch_smooth = make_interp_spline(years, simulated_totals_distopisch)(x_new)

# Stijlvolle Visualisatie
plt.style.use("seaborn-v0_8-darkgrid")  # Achtergrondstijl
plt.figure(figsize=(12, 7))
plt.plot(x_new, utopisch_smooth, color="#2ca02c", linewidth=3, label="Utopisch scenario (Beter watermanagement)")
plt.plot(x_new, neutraal_smooth, color="#1f77b4", linewidth=3, label="Neutraal scenario (Weinig verandering)")
plt.plot(x_new, distopisch_smooth, color="#d62728", linewidth=3, label="Distopisch scenario (Slechter watermanagement)")

# Onzekerheidsinterval toevoegen (voorbeeld ±5)
plt.fill_between(x_new, utopisch_smooth - 5, utopisch_smooth + 5, color="#2ca02c", alpha=0.2)
plt.fill_between(x_new, neutraal_smooth - 5, neutraal_smooth + 5, color="#1f77b4", alpha=0.2)
plt.fill_between(x_new, distopisch_smooth - 5, distopisch_smooth + 5, color="#d62728", alpha=0.2)

# Grafiek verbeteren
plt.title("Vergelijking van Toekomstige Scenario's voor Watergebruik", fontsize=18, fontweight='bold', pad=20)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Totaal watergebruik (liters per dag)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12, loc="upper left", fancybox=True, shadow=True, frameon=True)
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()

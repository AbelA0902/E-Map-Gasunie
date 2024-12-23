
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Simulatieparameters
n_simulations = 10000
future_years = 10
current_population = 17.8e6  # Startbevolking in Nederland (in 2024, ca. 17,8 miljoen)
annual_growth_rate = 0.007  # Gemiddelde jaarlijkse bevolkingsgroei (0,7%)

# Jaren
years = np.arange(2024, 2024 + future_years)

# Scenario's data
scenarios = {
    "Neutraal": {
        "Douche": {"mean": 50, "increase_rate": 0.05},
        "Toilet": {"mean": 35, "increase_rate": 0.03},
        "Overig": {"mean": 24.5, "increase_rate": 0.02},
    },
    "Utopisch": {
        "Douche": {"mean": 50, "reduction_rate": 0.30},
        "Toilet": {"mean": 35, "reduction_rate": 0.40},
        "Overig": {"mean": 24.5, "reduction_rate": 0.10},
    },
    "Dystopisch": {
        "Douche": {"mean": 50, "increase_rate": 0.20},
        "Toilet": {"mean": 35, "increase_rate": 0.15},
        "Overig": {"mean": 24.5, "increase_rate": 0.10},
    },
}

# Functie om simulaties uit te voeren
def simulate_water_usage(scenario_name):
    scenario = scenarios[scenario_name]
    simulated_totals = []
    category_trends = {"Douche": [], "Toilet": [], "Overig": []}

    for year in range(future_years):
        yearly_total = 0
        population = current_population * ((1 + annual_growth_rate) ** year)  # Bevolking in huidig jaar

        for category, stats in scenario.items():
            if "increase_rate" in stats:
                mean = stats["mean"] * (1 + stats["increase_rate"] * (year / future_years))
            elif "reduction_rate" in stats:
                mean = stats["mean"] * (1 - stats["reduction_rate"] * (year / future_years))

            std = mean * 0.1
            simulated_category = np.random.normal(mean, std, n_simulations)
            category_mean = np.mean(simulated_category)
            yearly_total += category_mean

            category_trends[category].append(category_mean * population / 1e6)  # Per categorie

        yearly_total *= population / 1e6  # Schaal het waterverbruik op basis van bevolking (per miljoen)
        simulated_totals.append(yearly_total)

    return simulated_totals, category_trends

# Simulatie voor alle scenario's
all_scenario_totals = {}
all_category_trends = {}

for scenario_name in scenarios.keys():
    totals, trends = simulate_water_usage(scenario_name)
    all_scenario_totals[scenario_name] = totals
    all_category_trends[scenario_name] = trends

# Vloeiendere lijnen voor alle scenario's
x_new = np.linspace(years.min(), years.max(), 300)
smooth_totals = {
    scenario: make_interp_spline(years, totals)(x_new)
    for scenario, totals in all_scenario_totals.items()
}

# Visualisatie
plt.figure(figsize=(16, 10))
plt.style.use("seaborn-v0_8-darkgrid")
colors = {"Neutraal": "#1f77b4", "Utopisch": "#2ca02c", "Dystopisch": "#d62728"}

# Plotten van alle scenario's
for scenario_name, smooth_values in smooth_totals.items():
    plt.plot(
        x_new, smooth_values, linewidth=3, label=f"{scenario_name} scenario", color=colors[scenario_name]
    )

# Grafiek verbeteren
plt.title("Vergelijking van Toekomstige Watergebruik Scenario's", fontsize=18, fontweight='bold', pad=20)
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Totaal watergebruik (miljard liters per jaar)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12, loc="upper left", fancybox=True, shadow=True, frameon=True)
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()
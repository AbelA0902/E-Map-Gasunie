import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Simulatieparameters
n_simulations = 10000
future_years = 10
current_population = 17.8e6  # Startbevolking in Nederland (2024, ca. 17,8 miljoen)
average_household_size = 2.2  # Gemiddelde grootte van een huishouden
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
def simulate_water_usage_per_household(scenario_name):
    scenario = scenarios[scenario_name]
    simulated_totals = []
    category_trends = {"Douche": [], "Toilet": [], "Overig": []}

    for year in range(future_years):
        yearly_total = 0
        population = current_population * ((1 + annual_growth_rate) ** year)  # Bevolking in huidig jaar
        households = population / average_household_size  # Aantal huishoudens

        for category, stats in scenario.items():
            if "increase_rate" in stats:
                mean = stats["mean"] * (1 + stats["increase_rate"] * (year / future_years))
            elif "reduction_rate" in stats:
                mean = stats["mean"] * (1 - stats["reduction_rate"] * (year / future_years))

            std = mean * 0.1
            simulated_category = np.random.normal(mean, std, n_simulations)
            category_mean = np.mean(simulated_category)
            yearly_total += category_mean

            category_trends[category].append(category_mean)  # Per categorie

        yearly_total_per_household = yearly_total / households  # Per huishouden
        simulated_totals.append(yearly_total_per_household)

    return simulated_totals, category_trends

# Functie om visualisatie te maken
def plot_all_scenarios_per_household():
    plt.style.use("seaborn-v0_8-darkgrid")  # Achtergrondstijl
    plt.figure(figsize=(14, 8))

    # Kleuren voor scenario's
    scenario_colors = {
        "Neutraal": "#1f77b4",
        "Utopisch": "#2ca02c",
        "Dystopisch": "#d62728",
    }

    for scenario_name, color in scenario_colors.items():
        simulated_totals, _ = simulate_water_usage_per_household(scenario_name)

        # Vloeiendere lijnen
        x_new = np.linspace(years.min(), years.max(), 300)
        total_smooth = make_interp_spline(years, simulated_totals)(x_new)

        # Scenario lijn plotten
        plt.plot(
            x_new, total_smooth, color=color, linewidth=2.5, label=f"{scenario_name} scenario"
        )

    # Grafiek verbeteren
    plt.title(
        "Toekomstige Voorspelling Gemiddeld Watergebruik per Huishouden",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Jaar", fontsize=14)
    plt.ylabel("Gemiddeld watergebruik per huishouden (liter per dag)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12, loc="upper left", fancybox=True, shadow=True, frameon=True)
    plt.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.show()

# Plot alle scenario's
plot_all_scenarios_per_household()

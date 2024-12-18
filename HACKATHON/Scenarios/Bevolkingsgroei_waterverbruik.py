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

# Functie om visualisatie te maken
def plot_scenario(scenario_name):
    simulated_totals, category_trends = simulate_water_usage(scenario_name)

    # Vloeiendere lijnen
    x_new = np.linspace(years.min(), years.max(), 300)
    total_smooth = make_interp_spline(years, simulated_totals)(x_new)
    category_smooth = {
        category: make_interp_spline(years, values)(x_new)
        for category, values in category_trends.items()
    }

    # Visualisatie
    plt.style.use("seaborn-v0_8-darkgrid")  # Achtergrondstijl
    plt.figure(figsize=(14, 8))

    # Achtergrondlijnen voor categorieën
    colors = {"Douche": "#ff7f0e", "Toilet": "#2ca02c", "Overig": "#9467bd"}
    for category, smooth_values in category_smooth.items():
        plt.plot(
            x_new, smooth_values, linestyle="--", linewidth=2, color=colors[category], alpha=0.7,
            label=f"{category} (categorie)"
        )

    # Totaallijn
    plt.plot(
        x_new, total_smooth, color="#1f77b4", linewidth=4, label=f"Totaal watergebruik ({scenario_name} scenario)"
    )

    # Onzekerheidsinterval interpoleren
    uncertainty_raw = 0.05 * np.array(simulated_totals)  # Onzekerheid op basis van originele data
    uncertainty_smooth = make_interp_spline(years, uncertainty_raw)(x_new)  # Interpoleren naar dezelfde schaal

    # Onzekerheidsinterval toevoegen
    plt.fill_between(
        x_new, 
        total_smooth - uncertainty_smooth, 
        total_smooth + uncertainty_smooth, 
        color="#1f77b4", 
        alpha=0.2
    )

    # Grafiek verbeteren
    plt.title(f"Toekomstige Voorspelling Watergebruik ({scenario_name} Scenario)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Jaar", fontsize=14)
    plt.ylabel("Totaal watergebruik (miljard liters per jaar)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12, loc="upper left", fancybox=True, shadow=True, frameon=True)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.show()

# Console-interface voor scenario-selectie
while True:
    print("\nKies een scenario:")
    print("1. Neutraal")
    print("2. Utopisch")
    print("3. Dystopisch")
    print("4. Stop")

    keuze = input("Voer het nummer in van je keuze: ")

    if keuze == "1":
        plot_scenario("Neutraal")
    elif keuze == "2":
        plot_scenario("Utopisch")
    elif keuze == "3":
        plot_scenario("Dystopisch")
    elif keuze == "4":
        print("Programma gestopt.")
        break
    else:
        print("Ongeldige invoer. Kies een geldig nummer.")

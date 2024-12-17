import numpy as np
import matplotlib.pyplot as plt

# Utopisch scenario: waterreductie in 10 jaar
data_utopisch = {
    "Douche": {"mean": 50, "reduction_rate": 0.30},
    "Toilet": {"mean": 35, "reduction_rate": 0.40},
    "Overig": {"mean": 24.5, "reduction_rate": 0.10},
}

# Parameters
n_simulations = 10000
future_years = 10
simulated_totals_utopisch = []

# Monte Carlo-simulatie
for year in range(future_years):
    yearly_total = sum(
        np.mean(np.random.normal(
            stats["mean"] * (1 - stats["reduction_rate"] * year / future_years),
            stats["mean"] * 0.1,
            n_simulations
        ))
        for stats in data_utopisch.values()
    )
    simulated_totals_utopisch.append(yearly_total)

# Visualisatie
years = np.arange(2022, 2022 + future_years)
plt.plot(years, simulated_totals_utopisch, marker='o', color='green', label="Utopisch scenario")
plt.fill_between(years, np.array(simulated_totals_utopisch) - 5, np.array(simulated_totals_utopisch) + 5,
                 color='green', alpha=0.2, label="Onzekerheidsinterval")
plt.title("Utopisch Scenario: Voorspelling Watergebruik (liters per dag)")
plt.xlabel("Jaar")
plt.ylabel("Totaal watergebruik (liters per dag)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

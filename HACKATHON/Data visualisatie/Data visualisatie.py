import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dataset samenvatten
data = {
    "Component": ["Bad", "Douche", "Toilet", "Afwas", "Was", "Consumptie", "Buitengebruik", "Overig"],
    "Liters per dag": [5.3, 46.2, 30.2, 3.9, 17.5, 2.6, 0.9, 12.8]
}

# Data in een DataFrame
df = pd.DataFrame(data)

# Histogrammen
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Component", y="Liters per dag", palette="Blues_d")
plt.title("Watergebruik in liters per dag per persoon", fontsize=16)
plt.xlabel("Component", fontsize=14)
plt.ylabel("Liters per dag", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# Staafdiagrammen
household_data = {
    "Huishoudtype": ["Eenpersoons", "Paar zonder kinderen", "Paar met kinderen", "Eenouderhuishouden", "Huishouden > 4 personen"],
    "Liters per dag": [186, 129, 110, 109, 96]
}
df_household = pd.DataFrame(household_data)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_household, x="Huishoudtype", y="Liters per dag", palette="coolwarm")
plt.title("Gemiddeld watergebruik per huishoudenstype", fontsize=16)
plt.xlabel("Huishoudtype", fontsize=14)
plt.ylabel("Liters per dag", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# **3. Lijndiagrammen
trend_data = {
    "Dag": list(range(1, 8)),  # Simuleer een week
    "Douche": [45, 46, 47, 44, 43, 46, 45],
    "Bad": [5, 6, 4, 5, 5, 5, 6],
    "Was": [17, 18, 17, 18, 16, 17, 18]
}
df_trend = pd.DataFrame(trend_data)

plt.figure(figsize=(10, 6))
for column in df_trend.columns[1:]:
    plt.plot(df_trend["Dag"], df_trend[column], marker="o", label=column)

plt.title("Trends in waterverbruik over een week", fontsize=16)
plt.xlabel("Dag", fontsize=14)
plt.ylabel("Liters per dag", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

# **4. Boxplots
components_data = {
    "Component": ["Bad"] * 5 + ["Douche"] * 5 + ["Was"] * 5,
    "Liters per dag": [4, 5, 6, 7, 8, 40, 42, 45, 47, 50, 16, 18, 17, 19, 20]
}
df_box = pd.DataFrame(components_data)

plt.figure(figsize=(10, 6))
sns.boxplot(data=df_box, x="Component", y="Liters per dag", palette="Set2")
plt.title("Boxplots: Variatie in waterverbruik per component", fontsize=16)
plt.xlabel("Component", fontsize=14)
plt.ylabel("Liters per dag", fontsize=14)
plt.grid(True)
plt.show()

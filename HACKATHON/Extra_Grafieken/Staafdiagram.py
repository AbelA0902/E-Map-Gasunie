import matplotlib.pyplot as plt

#waterverbruik per categorie volgens CBS database
categories = {
    "Bad": 4.5,
    "Douche": 50,
    "Toilet": 35,
    "Vaatwasser": 3.5,
    "Wasmachine": 10,
    "Consumptie": 2.5,
    "Buiten": 4,
}

# Categorien definieren.
labels = list(categories.keys())
values = list(categories.values())

# data ploten
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color="skyblue", edgecolor="black")

# opmaak
plt.title("Watergebruik per Categorie (liters per dag)", fontsize=16)
plt.xlabel("Categorie", fontsize=14)
plt.ylabel("Watergebruik (liters per dag)", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()

plt.show()

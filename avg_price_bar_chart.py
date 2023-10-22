import matplotlib.pyplot as plt
import pandas as pd


def plot_avg_price_by_fuel():
    df = pd.read_csv("prix-carburants-par_date.csv")
    avg_price = df.groupby("name")["price"].mean()
    fig, ax = plt.subplots()
    ax.bar(avg_price.index, avg_price.values)
    ax.set_title("Prix moyen par type de carburant")
    ax.set_xlabel("Type de carburant")
    ax.set_ylabel("Prix moyen")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

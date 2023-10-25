import matplotlib.pyplot as plt
import pandas as pd


def plot_avg_price_by_fuel():
    """
    :return: figure plot object from matplotlib
    """

    df = pd.read_csv("prix-carburants-par_date.csv")
    # Group by name (fuel) then aggregate with mean and take price value
    avg_price = df.groupby("name")["price"].mean()

    fig, ax = plt.subplots()
    ax.bar(avg_price.index, avg_price.values)
    ax.set_title("Prix moyen par type de carburant")
    ax.set_xlabel("Type de carburant")
    ax.set_ylabel("Prix moyen")
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

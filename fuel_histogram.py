import pandas as pd
import matplotlib.pyplot as plt

def plot_fuel_histogram():

    df = pd.read_csv("prix-carburants-par_date.csv")

    df["date"] = pd.to_datetime(df["date"])

    df_grouped = df.groupby([pd.Grouper(key="date", freq="M"), "name"])["price"].mean().reset_index()

    fig, ax = plt.subplots()
    for fuel_type in df_grouped["name"].unique():
        subset = df_grouped[df_grouped["name"] == fuel_type]
        ax.bar(subset["date"], subset["price"], label=fuel_type)
    ax.set_title("Prix moyen du carburant en fonction du temps")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix moyen")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


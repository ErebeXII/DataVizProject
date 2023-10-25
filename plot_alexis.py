import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def read_csv(csv):
    df = pd.read_csv(csv, sep=";")
    return df
def st_line(csv):
    df = read_csv(csv)
    df = df.dropna()
    import pandas as pd
    import streamlit as st

    df1 = df[(df["prix_nom"] != "GPLc") & (df["prix_nom"] != "E85")]
    df1 = df1[["prix_maj", "prix_valeur"]]

    df1["prix_maj"] = pd.to_datetime(df1["prix_maj"])  # Utilisez df1 au lieu de df ici
    df1["prix_maj"] = df1["prix_maj"].apply(lambda x: x.date())
    daily_mean_prices = df1.groupby("prix_maj")["prix_valeur"].mean().reset_index()

    st.title("Prix moyen du carburant en fonction du temps (hors GPL et E85)")
    st.line_chart(daily_mean_prices.set_index("prix_maj"))


def st_scatter(csv):
    df = read_csv(csv)
    df = df.dropna()
    df1 = df[df["prix_nom"] == "GPLc"]
    df1 = df1[["prix_maj", "prix_valeur"]]

    df1["prix_maj"] = pd.to_datetime(df1["prix_maj"])
    df1["prix_maj"] = df1["prix_maj"].apply(lambda x: x.date())
    df1 = df1[df1["prix_maj"] > pd.to_datetime("2022-10-01").date()]
    st.title("Prix du GPL en fonction du temps")
    st.scatter_chart(df1, x="prix_maj", y="prix_valeur", size =8)

def categorize_services(row):
    num_services = len(row["services_separés"])
    if num_services >= 11:
        return "Plus de 12 services"
    elif num_services >= 6:
        return "Entre 6 et 11 services"
    elif num_services >= 3:
        return "Entre 3 et 5 services"
    else:
        return "Moins de 3 services"

def categorize_services1(row):
    return len(row["services_separés"])
def matplot_scatter(csv):
    df = read_csv(csv)
    df = df.dropna()
    df = df[(df["prix_nom"] != "GPLc") & (df["prix_nom"] != "E85")]
    df = df[df["reg_name"] == "Nouvelle-Aquitaine"]
    df['services_separés'] = df['services_service'].str.split('//')
    df["prix_maj"] = pd.to_datetime(df["prix_maj"]).apply(lambda x: x.date())
    df = df[df["prix_maj"] > pd.to_datetime("2022-10-01").date()]

    df["categorie"] = df.apply(categorize_services, axis=1)
    df["number"] = df.apply(categorize_services1, axis=1)

    # Create a Streamlit app
    st.title('Corrélation entre le prix du carburant et les services proposés')
    st.write('Prix du carburant (hors GPL et E85) en Nouvelle-Aquitaine en fonction du temps et des services')

    # Create a figure for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        'Moins de 3 services': 'blue',
        'Entre 3 et 5 services': 'green',
        'Entre 6 et 11 services': 'orange',
        'Plus de 12 services': 'red'
    }

    for category, color in colors.items():
        data = df[df['categorie'] == category]
        ax.scatter(data['prix_maj'], data['prix_valeur'], c=color, label=category, alpha=0.5, s=10)

    ax.set_xlabel('Temps')
    ax.set_ylabel('Prix du carburant')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
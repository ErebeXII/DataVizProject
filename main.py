import pandas as pd
import numpy as np
import swifter
import calplot
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def main_plot_calmap(create_csv=False,
                     origin_csv=r"prix-carburants-fichier-instantane-test-ods-copie.csv",
                     destination_csv=r"prix-carburants-par_date.csv"):
    """
    :param create_csv: bool, faut-il refaire le sub csv
    :param origin_csv: chemin vers le csv original
    :param destination_csv: chemin vers le sub csv
    :return: null (la fonction appellera une fonction qui plot les calmap)
    """

    if create_csv:
        csv_for_price_per_date(origin_csv, destination_csv)

    plot_price_calendars(destination_csv)


def plot_price_calendars(path_csv):
    """
    :param path_csv: chemin vers csv {date, prix, nom_carburant}
    :return: plot une calheatmap par carburant
    """

    df = pd.read_csv(path_csv, sep=',', encoding='utf-8', low_memory=False, on_bad_lines='warn')

    # get all unique carburants
    carburants = df["name"].unique()
    # create a dataframe for each carburant
    df_carburants = [df[df["name"] == carburant] for carburant in carburants]
    dict_carburants = {}
    for c in df_carburants:
        dict_carburants.update({c["name"].iloc[0]: get_average_per_day(c)})

    # plot a calendar for each carburant
    for name, carb in dict_carburants.items():
        events = pd.Series(carb["price_avg"].values, index=pd.to_datetime(carb.index))

        fig = plt.figure(figsize=(16, 6))
        ax = fig.add_subplot(111)
        cax = calplot.yearplot(events, year=2023, ax=ax,  cmap='YlGnBu')
        title = name + " - prix moyen par jour en 2023"
        plt.title(title)
        divider = make_axes_locatable(cax)
        lcax = divider.append_axes("left", size="2%", pad=0.5)
        fig.colorbar(cax.get_children()[1], cax=lcax)
        plt.show()


def get_average_per_day(data):
    """
    :param data: dataframe {name, price, date}
    :return: dataframe avec un prix moyen par date (en index)
    """
    df = pd.DataFrame(columns=["price_avg"])
    # group by per date and sum price
    df["price_avg"] = data.groupby("date")["price"].mean()
    return df


def csv_for_price_per_date(path_original_csv, path_destination_csv):
    """
    :param path_original_csv: path du csv original
    :param path_destination_csv: path du csv de destination
    :return: un csv avec les prix par date
    """

    df = pd.read_csv(path_original_csv, sep=';', encoding='utf-8', low_memory=False, on_bad_lines='skip')
    df.drop_duplicates()  # drop duplicates (should be none) since they have a unique id

    df = df[["prix_maj", "prix_nom", "prix_valeur"]]
    df["prix_maj"] = pd.to_datetime(df["prix_maj"])
    df["prix_maj"] = df["prix_maj"].swifter.apply(lambda x: x.date())

    df.rename(columns={"prix_maj": "date", "prix_nom": "name", "prix_valeur": "price"}, errors="raise", inplace=True)

    df.dropna(inplace=True)  # drop lines with missing date or price or name

    df.to_csv(path_destination_csv, sep=',', encoding='utf-8', index=False)


main_plot_calmap(True)
import streamlit as st
import pandas as pd
from price_map import create_map  # Assuming price_map.py is in the same directory


def main():
    st.title("Fuel Price Analysis")

    # Load Data
    csv_path = "prix-carburants-fichier-instantane-test-ods-copie.csv"
    df = pd.read_csv(csv_path, sep=";")

    # Create sidebar options
    st.sidebar.write("## Options")
    info = st.sidebar.checkbox("Show DataFrame Info", value=True)
    describe = st.sidebar.checkbox("Show Descriptive Stats", value=True)
    price_map = st.sidebar.checkbox("Show Price Map", value=True)

    # Display basic DataFrame information as a table
    if info:
        st.write("### DataFrame Info")
        info_df = pd.DataFrame({
            'Column': df.columns,
            'Non-Null Count': df.count(),
            'Dtype': df.dtypes
        }).reset_index(drop=True)
        st.table(info_df)

    # Show descriptive statistics
    if describe:
        st.write("### Descriptive Statistics")
        st.write(df.describe())

    # Display the map
    if price_map:
        st.write("### Price Map")
        st.components.v1.html(create_map(df), width=800, height=600)

    # Future place for additional analysis modules
    # ...


# Running the app
if __name__ == "__main__":
    main()

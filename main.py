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

from turtle import st

import pandas as pd
import numpy as np
import swifter
import calplot
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


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
def data_service(csv):
    df = pd.read_csv(csv, sep=";")
    df = df.dropna()
    # print(df.columns)
    df_service = df[["id", "services_service", "geom"]]
    # print(df_service)

    # On enlève les doublons, qui dans notre cas ne nous interesse pas.
    df_service = df_service.drop_duplicates(subset="id")

    # On transforme la chaine de caractere en une liste avec la longitude et la latitude.
    df_service['geom'] = df_service['geom'].str.split(',')

    # On Sépare les services en une liste.
    df_service['services_separés'] = df_service['services_service'].str.split('//')

    # Voici les valeurs uniques
    valeurs_unique = df_service['services_separés'].explode().unique()
    # print(valeurs_unique)
    return df_service
def map_Services_Sanitaires(origin_csv):

    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Toilettes publiques", "Douches", "Espace bébé"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)


def map_Relais_Colis(origin_csv):
    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Relais colis"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)


def map_Alimentation(origin_csv):
    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Boutique alimentaire", "Restauration à emporter", "Restauration sur place", "Bar"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)


def map_Carburants(origin_csv):
    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Vente de fioul domestique", "Vente de pétrole lampant", "Vente de gaz domestique (Butane, Propane)", "Carburant additivé", "GNV", "Vente d'additifs carburants"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)


def map_Services_Vehicules(origin_csv):
    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Station de gonflage", "Location de véhicule", "Lavage manuel", "Lavage automatique", "Services réparation / entretien"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)


def map_Services_financiers(origin_csv):
    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Automate CB 24/24", "DAB (Distributeur automatique de billets)"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)

def map_Services_Divers(origin_csv):
    df_service = data_service(origin_csv)
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    # Créez un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    values_to_check = ["Boutique non alimentaire", "Aire de camping-cars", "Piste poids lourds", "Bornes électriques", "Wifi", "Laverie"]
    # Ajoutez des marqueurs au groupe de clusters
    for i in range(0, len(df_service)):
        services = df_service.iloc[i]['services_separés']
        if any(value in df_service.iloc[i]['services_separés'] for value in values_to_check):
            services_str = ', '.join(services)
            folium.Marker(
                location=[float(df_service.iloc[i]['geom'][0]), float(df_service.iloc[i]['geom'][1])],
                tooltip=df_service.iloc[i]['id'],
                popup=services_str,
            ).add_to(marker_cluster)
    # call to render Folium map in Streamlit
    folium_static(m)

main_plot_calmap(True)
import streamlit as st
import pandas as pd
#from price_map import create_map  # Assuming price_map.py is in the same directory


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
    service_map = st.sidebar.checkbox("Show Service Map", value=True)
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
        #st.components.v1.html(create_map(df), width=800, height=600)

    if service_map:
        st.subheader("Filtres de station-services")
        sub_option_1 = st.checkbox("Service Sanitaires")
        if sub_option_1:
            st.write("### Service Sanitaires")
            st.write("Toilettes publiques, Douches, Espace bébé")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        sub_option_2 = st.checkbox("Service Livraison")
        if sub_option_2:
            st.write("### Service Livraison")
            st.write("Relais colis")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        sub_option_3 = st.checkbox("Service Alimentaire")
        if sub_option_3:
            st.write("### Service Alimentaire")
            st.write("Boutique alimentaire, Restauration à emporter, Restauration sur place, Bar")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        sub_option_4 = st.checkbox("Service Carburants")
        if sub_option_4:
            st.write("### Service Carburants")
            st.write("Vente de fioul domestique, Vente de pétrole lampant, Vente de gaz domestique (Butane, Propane), Carburant additivé, GNV, Vente d'additifs carburants")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        sub_option_5 = st.checkbox("Service Véhicules")
        if sub_option_5:
            st.write("### Service Véhicules")
            st.write("Station de gonflage, Location de véhicule, Lavage manuel, Lavage automatique, Services réparation / entretien")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        sub_option_6 = st.checkbox("Service FInanciers")
        if sub_option_6:
            st.write("### Service FInanciers")
            st.write("Automate CB 24/24, DAB (Distributeur automatique de billets)")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        sub_option_7 = st.checkbox("Service Divers")
        if sub_option_7:
            st.write("### Service Divers")
            st.write("Boutique non alimentaire, Aire de camping-cars, Piste poids lourds, Bornes électriques, Wifi, Laverie")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)



# Running the app
if __name__ == "__main__":
    main()

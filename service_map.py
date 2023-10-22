import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import pandas as pd
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
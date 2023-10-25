import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
from price_map import create_map  # Assuming price_map.py is in the same directory
from price_calendar import main_plot_calmap
from service_map import data_service, map_Services_Sanitaires, map_Relais_Colis, map_Alimentation, map_Carburants, map_Services_Vehicules, map_Services_financiers, map_Services_Divers
from plot_alexis import st_line,st_scatter, read_csv,categorize_services,categorize_services1, matplot_scatter


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
    price_calendar = st.sidebar.checkbox("Show Price Calendar", value=True)
    matplot_scatter1 = st.sidebar.checkbox("Show Scatter matplotlib", value=True)
    st_line1 = st.sidebar.checkbox("Show ST Line", value=True)
    st_scatter1 = st.sidebar.checkbox("Show st SCATTER", value=True)

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
        st.components.v1.html(create_map(df), width=800, height=600)

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

    if price_calendar:
        st.write("### Price Calendar")
        main_plot_calmap(True)

    if matplot_scatter1:
        st.write("### Scatter plot")
        matplot_scatter(r"prix-carburants-fichier-instantane-test-ods-copie.csv")

    if st_line1:
        st.write("### ST LINE plot")
        st_line(r"prix-carburants-fichier-instantane-test-ods-copie.csv")

    if st_scatter1:
        st.write("### st scatter plot")
        st_scatter(r"prix-carburants-fichier-instantane-test-ods-copie.csv")


# Running the app
if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from price_map import create_map
from price_calendar import main_plot_calmap
from service_map import data_service, map_Services_Sanitaires, map_Relais_Colis, map_Alimentation, map_Carburants, map_Services_Vehicules, map_Services_financiers, map_Services_Divers
from plot_alexis import st_line,st_scatter, read_csv,categorize_services,categorize_services1, matplot_scatter
from avg_price_bar_chart import plot_avg_price_by_fuel
from fuel_histogram import plot_st_fuels
from pie_chart_sevices import bar_chart_small_services, pie_chart_services


def main():
    st.title("Fuel Price Analysis by UNG, PERIER and ZHANG")

    # Load Data
    csv_path = "prix-carburants-fichier-instantane-test-ods-copie.csv"
    df = pd.read_csv(csv_path, sep=";")

    # Create sidebar options
    st.sidebar.write("## Options")
    info = st.sidebar.checkbox("Show DataFrame Info", value=True)
    describe = st.sidebar.checkbox("Show Descriptive Stats", value=True)
    price_map = st.sidebar.checkbox("Show Price Map", value=True)
    service_map = st.sidebar.checkbox("Show Service Map", value=True)
    price_calendar = st.sidebar.checkbox("Show Price Calendar", value=True)
    matplot_scatter1 = st.sidebar.checkbox("Show Scatter matplotlib", value=True)
    st_line1 = st.sidebar.checkbox("Show ST Line", value=True)
    st_scatter1 = st.sidebar.checkbox("Show ST SCATTER", value=True)
    avg_price_barplot = st.sidebar.checkbox("Show Average Fuel Price Bar Chart", value=True)
    fuel_histogram = st.sidebar.checkbox("Show Fuel Histogram", value=True)
    bar_chart = st.sidebar.checkbox("Show Bar Chart", value=True)
    pie_chart = st.sidebar.checkbox("Show Pie Chart", value=True)

    # Display basic DataFrame information as a table
    if info:
        st.write("### DataFrame Infos")
        info_df = pd.DataFrame({
            'Column': df.columns,
            'Non-Null Count': df.count(),
            'Dtype': df.dtypes
        }).reset_index(drop=True)
        st.table(info_df)

    # Show descriptive statistics
    if describe:
        st.write("### Statistiques Descriptives")
        st.write(df.describe())

    # Display the prices map
    if price_map:
        st.write("### Carte des Prix")
        create_map(df)

    # Display the services map with its selectbox
    if service_map:
        st.subheader("Filtres de station-services")

        service_options = ["Service Sanitaires", "Service Livraison", "Service Alimentaire", "Service Carburants", "Service Véhicules", "Service Financiers", "Service Divers"]
        selected_service = st.selectbox("Select a service", service_options)

        if selected_service == "Service Sanitaires":
            st.write("### Service Sanitaires")
            st.write("Toilettes publiques, Douches, Espace bébé")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        if selected_service == "Service Livraison":
            st.write("### Service Livraison")
            st.write("Relais colis")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        if selected_service == "Service Alimentaire":
            st.write("### Service Alimentaire")
            st.write("Boutique alimentaire, Restauration à emporter, Restauration sur place, Bar")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        if selected_service == "Service Carburants":
            st.write("### Service Carburants")
            st.write("Vente de fioul domestique, Vente de pétrole lampant, Vente de gaz domestique (Butane, Propane), Carburant additivé, GNV, Vente d'additifs carburants")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        if selected_service == "Service Véhicules":
            st.write("### Service Véhicules")
            st.write("Station de gonflage, Location de véhicule, Lavage manuel, Lavage automatique, Services réparation / entretien")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        if selected_service == "Service Financiers":
            st.write("### Service FInanciers")
            st.write("Automate CB 24/24, DAB (Distributeur automatique de billets)")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)
        if selected_service == "Service Divers":
            st.write("### Service Divers")
            st.write("Boutique non alimentaire, Aire de camping-cars, Piste poids lourds, Bornes électriques, Wifi, Laverie")
            st.components.v1.html(map_Services_Sanitaires(r"prix-carburants-fichier-instantane-test-ods-copie.csv"),
                                  width=800, height=600)

    # Display the calendars of prices
    if price_calendar:
        st.write("### Calendriers des Prix")
        main_plot_calmap(True)

    if matplot_scatter1:
        matplot_scatter(r"prix-carburants-fichier-instantane-test-ods-copie.csv")

    if st_line1:
        st_line(r"prix-carburants-fichier-instantane-test-ods-copie.csv")

    if st_scatter1:
        st_scatter(r"prix-carburants-fichier-instantane-test-ods-copie.csv")

    # Display barplot of "Prix moyen par type de carburant"
    if avg_price_barplot:
        st.write("## Prix moyen par type de carburant")
        st.pyplot(plot_avg_price_by_fuel())

    # Display histogram of "Prix du carburant au cours du temps"
    if fuel_histogram:
        st.write("## Prix du carburant au cours du temps ")
        plot_st_fuels()

    if bar_chart:
        st.write("### Bar Chart")
        df_small_services = bar_chart_small_services()
        st.bar_chart(df_small_services)

    if pie_chart:
        st.write("### Pie Chart")
        st.pyplot(pie_chart_services())


# Running the app
if __name__ == "__main__":
    main()

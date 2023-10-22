import streamlit as st
import pandas as pd
from price_map import create_map  # Assuming price_map.py is in the same directory
from price_calendar import main_plot_calmap

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

    if price_calendar:
        st.write("### Price Calendar")
        main_plot_calmap(True)

    # Future place for additional analysis modules
    # ...


# Running the app
if __name__ == "__main__":
    main()

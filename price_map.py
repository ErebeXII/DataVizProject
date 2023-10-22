import branca
import streamlit as st


def calculate_color(value, vmin, vmax):
    # Map value to 0-1 range
    normalized_value = (value - vmin) / (vmax - vmin)

    if normalized_value <= 0.33:
        # green
        r, g, b = 0, 0.9, 0
    elif 0.33 < normalized_value <= 0.66:
        # yellow
        r, g, b = 0.7, 0.7, 0
    else:
        # red
        r, g, b = 0.9, 0, 0

    return [r, g, b, 0.8]


def create_map(df):

    """
    :param df: Dataframe
    :return: html of folium.Map
    """

    df = df.copy()
    df.dropna(subset=["geom", "prix_valeur", "com_code", "dep_code"], inplace=True)  # Added "dep_code"
    df = df[["geom", "prix_valeur", "com_code", "dep_code"]]  # Added "dep_code"

    # Extract longitude and latitude from geom column
    df["lon"] = df["geom"].apply(lambda x: float(x.split(",")[0]))
    df["lat"] = df["geom"].apply(lambda x: float(x.split(",")[1]))
    df.drop(columns="geom", inplace=True)

    # Add checkbox for choosing between "com_code" and "dep_code"
    use_dep_code = st.checkbox("Use Department Code instead of Commune Code")
    # Add checkbox for choosing between mean and median
    use_median = st.checkbox("Use Median instead of Mean")

    group_column = "dep_code" if use_dep_code else "com_code"
    agg_func = "median" if use_median else "mean"

    # Group by chosen column and aggregate
    df = df.groupby(group_column).agg({'lon': 'mean', 'lat': 'mean', 'prix_valeur': agg_func}).reset_index()

    vmin = df['prix_valeur'].min()
    vmax = df['prix_valeur'].max()

    df["color"] = df["prix_valeur"].apply(lambda x: calculate_color(x, vmin, vmax))

    st.map(df, latitude="lon", longitude="lat", color="color")  # Fixed lat and lon


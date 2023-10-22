import branca
from folium.plugins import MarkerCluster
import folium
import webbrowser


def create_map(df):

    """
    :param df: Dataframe
    :return: html of folium.Map
    """

    df = df.copy()
    df.dropna(subset=["geom", "prix_valeur", "com_code"], inplace=True)
    df = df[["geom", "prix_valeur", "com_code"]]

    # Extract longitude and latitude from geom column
    df["lon"] = df["geom"].apply(lambda x: float(x.split(",")[0]))
    df["lat"] = df["geom"].apply(lambda x: float(x.split(",")[1]))
    df.drop(columns="geom", inplace=True)

    # Group by commune code and get the mean of the values
    df = df.groupby("com_code").mean().reset_index()

    # Create map
    c = folium.Map(location=[df["lon"].mean(), df["lat"].mean()], prefer_canvas=True, zoom_start=6)

    price_colormap = branca.colormap.LinearColormap(
        colors=["green", "yellow", "red"],
        vmin=df["prix_valeur"].min(),
        vmax=df["prix_valeur"].max()
    )

    # Create clustering of points when there are too many of them
    marker_cluster = MarkerCluster().add_to(c)

    # For each row, create a point on the map
    for index, row in df.iterrows():
        color = price_colormap(row["prix_valeur"])
        folium.CircleMarker(
            location=(row["lon"], row["lat"]),
            tooltip=str(row["prix_valeur"]) + "€, Code commune: " + str(row["com_code"]),
            color=color,
            fill=True,
            radius=30
        ).add_to(marker_cluster)

    # c.save("price_map.html")
    # webbrowser.open("price_map.html", new=2)  # new=2 opens in a new tab, if possible

    return c.get_root().render()

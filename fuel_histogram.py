import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime


def plot_fuel_histogram(fuel_type, df_grouped):
    subset = df_grouped[df_grouped["name"] == fuel_type]

    fig, ax = plt.subplots()
    ax.bar(subset["date"], subset["price"], label=fuel_type)
    ax.set_title(f"Prix moyen du {fuel_type} en fonction du temps")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix moyen")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_st_fuels():
    df = pd.read_csv("prix-carburants-par_date.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"].dt.year == 2023]

    df_grouped = df.groupby([pd.Grouper(key="date", freq="D"), "name"])["price"].mean().reset_index()
    fuel_types = df_grouped["name"].unique()

    fuel_index = st.slider("Glissez pour choisir le carburant. ", min_value=0, max_value=len(fuel_types) - 1, step=1)
    selected_fuel = fuel_types[fuel_index]

    fig = plot_fuel_histogram(selected_fuel, df_grouped)
    st.pyplot(fig)


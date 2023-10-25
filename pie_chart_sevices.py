import pandas as pd
import matplotlib.pyplot as plt

proportion_small_services = 0.025

def pie_chart_services(path="prix-carburants-fichier-instantane-test-ods-copie.csv"):

    df = pd.read_csv(path, sep=";")

    services = df["services_service"].str.split('//').explode().str.strip()
    services_count = services.value_counts()

    # Remove the small services from the dataframe
    proportion = services_count.sum()*proportion_small_services
    small_services = services_count[services_count < proportion]
    services_count["other"] = small_services.sum()
    # store the small services in a variable to use later
    df_small_services = services_count[services_count < proportion]
    # Remove the small services from the dataframe
    services_count = services_count[services_count > proportion]

    # Plot the pie chart
    plt.figure(figsize=(15, 10))
    plt.pie(services_count, labels=services_count.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Services")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def bar_chart_small_services(path="prix-carburants-fichier-instantane-test-ods-copie.csv"):
    df = pd.read_csv(path, sep=";")

    services = df["services_service"].str.split('//').explode().str.strip()
    services_count = services.value_counts()

    proportion = services_count.sum()*proportion_small_services

    df_small_services = services_count[services_count < proportion]
    # plot the small services as a bar chart
    plt.figure(figsize=(15, 10))
    plt.bar(df_small_services.index, df_small_services.values)
    plt.title("Distribution of Services (small proportion)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt

pie_chart_services()
bar_chart_small_services()

#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import seaborn as sns
import pandas as pd
from . import stats as s
import matplotlib.pyplot as plt

def outliers(df):
    """Remove outliers as defined by asssets more than 3 STD away
    from average on the columns price, Bedroom and Living_area"""
    std = df.select_dtypes('float').std()
    distance = abs(df.select_dtypes('float')-df.select_dtypes('float').mean()).div(std)
    price_outliers = distance.loc[distance["Price"] > 3, "Price"]
    bedroom_outliers = distance.loc[distance["Bedroom"] > 3, "Bedroom"]
    living_outliers = distance.loc[distance["Living_area"] > 3, "Living_area"]
    outliers=pd.concat([price_outliers, bedroom_outliers,living_outliers], axis=1)

#    plot = sns.kdeplot(outliers)
#    plot.set(title="Outliers", ylabel="Listing ID", xlabel="STD away from average")
#    plt.show()
    return df[~df.index.isin(living_outliers.index)]

def hist_living(df):
    """Creates a histogram of living area on the given df
    """
    plot = sns.histplot(data=df, x="Living_area")
    plot.set(title="Distribution of Living Area", xlabel="Living Area")
    plot.axvline(x=df["Living_area"].mean(), c='red', ls="--")
    plt.show()

def per_province(df):
    """Plots average listing price per province
    """
    plot = sns.barplot(data=df.loc[:,["Price", "Province"]].groupby("Province", as_index=False).mean(), x="Province", y="Price")
    plot.set_xticklabels(plot.get_xticklabels(),rotation=45, horizontalalignment='right')
    plot.set(title="Average listing price per Province")
    plt.show()

def square_meter_per_province(df):
    """Computes and returns the square meter price and plots average
    square meter price per province"""
    df["Square_meter"]= df["Price"]/df["Living_area"]
    plot = sns.barplot(data=df, x="Province", y="Square_meter", hue="Type", errorbar=None)
    plot.set(ylabel="Avg Price per m²", title="Average m² price per Province")
    plot.set_xticklabels(plot.get_xticklabels(),rotation=45, horizontalalignment='right')
    plot.legend(labels=["Apartment", "House"])
    return df
    plt.show()

def map(df):
    """Makes a scatter plot of the coordinates using the square meter price as
    point size
    """
    plot = sns.scatterplot(data=df, x="lng", y="lat", size="Square_meter", sizes=(1,1000), alpha=0.3, legend=False)
    plot.set(title="Map of m² price in Belgium",xlabel="Longitude", ylabel="Latitude")
    plt.show()

def numeric_corr(df):
    """Computes the correlation for numeric values and plots a heat map
    """
    numeric_corr = df[["Bedroom", "Living_area", "Garden_area", "Surface_of_land", "Facade", "Price"]].corr()
    plot = sns.heatmap(data = numeric_corr)
    plot.set(title="Correlation between Price and numeric variables")
    plt.show()

def cat_corr(df):
    """Computes the correlation for categorical values and plots a heat map
    """
    keys= []
    values= []
    for col in df.select_dtypes(include='object').columns:
        keys.append(col)
        values.append(s.correlation_ratio(df[~df[col].isnull()][col],df[~df[col].isnull()]["Price"]))
    cat_corr =pd.DataFrame.from_records({"Cat": keys, "Price" : values}, index="Cat").sort_values(by="Price", ascending=False).iloc[1:,:]
    plot = sns.heatmap(data=cat_corr)
    plot.set(title="Correlation between Categories and price")
    plt.show()

def localities_count(df):
    """Computes the cumulative number of listings per locality (order from
    fewer to more listings per locality
    """
    grouped = df.groupby("Locality").agg({"city" : "count"}).groupby("city").agg({"city": "count"})
    grouped = grouped/grouped.sum()
    grouped["prop_city"] = grouped.cumsum()
    plot = sns.barplot(data = grouped, x=grouped.index[0:50], y=grouped.prop_city[0:50])
    plot.set(title="Cumulative amount of Localities per number of listings per locality", ylabel="% of total", xlabel="Listings per Locality")
    plot.set_xlim(-1,25)
    plt.show()

def cities_count(df):
    """Computes the cumulative number of listings per city (order from
    fewer to more listings per city
    """
    grouped = df.groupby("city").agg({"Locality" : "count"}).groupby("Locality").agg({"Locality": "count"})
    grouped = grouped/grouped.sum()
    grouped["prop_city"] = grouped.cumsum()
    plot = sns.barplot(data = grouped, x=grouped.index, y="prop_city")
    plot.set(xlim=(-1,25), title="Cumulative amount of Cities per number of listings per locality", ylabel="% of total", xlabel="Listings per City")
    plt.show()

def cities_corr(df):
    """Computes the correlation between price and numeric values for each
    city. Plots a density graph for those correlations.
    """
    numeric_corr = []
    for city in df["city"].unique():
        df_by_city = df[df["city"] == city]
        if len(df_by_city.index) > 3:
            numeric_corr.append(df_by_city[["Bedroom", "Living_area", "Garden_area", "Surface_of_land", "Facade", "Price"]].corr()["Price"].to_frame(name=city))
    corr_by_city = pd.concat(numeric_corr, axis=1).transpose()
    corr_by_city = corr_by_city.iloc[:,:-1]
    plot = sns.kdeplot(corr_by_city)
    plot.set(title = "Distribution of correlation between Price and numeric values within each city"
        , xlabel="Correlation"
        , ylabel="Density"
        ,xlim=(-1.2,1.2)
        )
    plt.show()

def cat_corr_city(df):
    """Computes the correlation between price and categorical values for each
    city. Plots a density graph for those correlations.
    """
    cat_corr = []
    for city in df["city"].unique():
        df_by_city = df[df["city"] == city].drop(["URL", "Locality", "District", "city", "Listing_address"] , axis=1)
        keys= []
        values= []
        if len(df_by_city.index) > 3:
            for col in df_by_city.select_dtypes(include='object').columns:
                keys.append(col)
                values.append(s.correlation_ratio(df_by_city[~df_by_city[col].isnull()][col],df_by_city[~df_by_city[col].isnull()]["Price"]))
            cat_corr.append(pd.Series(values, index=keys, name=city))
    corr_by_city = pd.concat(cat_corr, axis=1).transpose()

    plot = sns.kdeplot(corr_by_city)
    plot.set(title = "Distribution of correlation between Price and categories within each city"
        , xlabel="Correlation"
        , ylabel="Density"
        ,xlim=(-0.5,1.2)
        )
    plt.show()

def living_price(df, district = None):
    """Plots living_area vs Price for any given df. If district is passed do so
    only for the given district"""
    if district:
        plot = sns.scatterplot(data=df[df["District"] == district]
                               , x="Living_area"
                               , y="Price"
                               , hue="Type"
                               , alpha=0.5)
    else:
        plot = sns.scatterplot(data=df
                               , x="Living_area"
                               , y="Price"
                               , hue="Type"
                               , alpha=0.5)
    plot.set(title="Price vs Living area separated by Type"
             , xlabel="Living Area"
             , ylabel="Price")
    plt.show()

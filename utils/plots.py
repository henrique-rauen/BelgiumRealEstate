#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import seaborn as sns
import pandas as pd
import utils.stats as s
import matplotlib.pyplot as plt

def plot(df):
    std = df.select_dtypes('float').std()
    distance = abs(df.select_dtypes('float')-df.select_dtypes('float').mean()).div(std)
    price_outliers = distance.loc[distance["Price"] > 3, "Price"]
    bedroom_outliers = distance.loc[distance["Bedroom"] > 3, "Bedroom"]
    living_outliers = distance.loc[distance["Living_area"] > 3, "Living_area"]
    outliers=pd.concat([price_outliers, bedroom_outliers,living_outliers], axis=1)

#    #Plot Outliers
#    plot = sns.kdeplot(outliers)
#    plot.set(title="Outliers", ylabel="Listing ID", xlabel="STD away from average")

    df_clean_outliers= df[~df.index.isin(living_outliers.index)]
#    #Plot Histogram of living area
#    plot = sns.histplot(data=df_clean_outliers, x="Living_area")
#    plot.set(title="Distribution of Living Area", xlabel="Living Area")
#    plot.axvline(x=df_clean_outliers["Living_area"].mean(), c='red', ls="--")

#    #Plot Price per province
#    plot = sns.barplot(data=df_clean_outliers.loc[:,["Price", "Province"]].groupby("Province", as_index=False).mean(), x="Province", y="Price")
#    plot.set_xticklabels(plot.get_xticklabels(),rotation=45, horizontalalignment='right')
#    plot.set(title="Average listing price per Province")

    df_clean_outliers["Square_meter"]= df_clean_outliers["Price"]/df_clean_outliers["Living_area"]
#   #Plot Square meters per province
    #plot = sns.barplot(data=df_clean_outliers, x="Province", y="Square_meter", hue="Type", errorbar=None)
    #plot.set(ylabel="Avg Price per m²", title="Average m² price per Province")
    #plot.set_xticklabels(plot.get_xticklabels(),rotation=45, horizontalalignment='right')
    #plot.legend(labels=["Apartment", "House"])

    #Plot map
#    plot = sns.scatterplot(data=df_clean_outliers, x="lng", y="lat", size="Square_meter", sizes=(1,1000), alpha=0.3, legend=False)
#    plot.set(title="Map of m² price in Belgium",xlabel="Longitude", ylabel="Latitude")

    #Numeric correlations
    numeric_corr = df_clean_outliers[["Bedroom", "Living_area", "Garden_area", "Surface_of_land", "Facade", "Price"]].corr()
#    plot = sns.heatmap(data = numeric_corr)
#    plot.set(title="Correlation between Price and numeric variables")


    #Category correlations
    keys= []
    values= []
    for col in df_clean_outliers.select_dtypes(include='object').columns:
        keys.append(col)
        values.append(s.correlation_ratio(df_clean_outliers[~df_clean_outliers[col].isnull()][col],df_clean_outliers[~df_clean_outliers[col].isnull()]["Price"]))
    cat_corr =pd.DataFrame.from_records({"Cat": keys, "Price" : values}, index="Cat").sort_values(by="Price", ascending=False).iloc[1:,:]
#    plot = sns.heatmap(data=cat_corr)
#    plot.set(title="Correlation between Categories and price")

    #Deeper look
    grouped = df_clean_outliers.groupby("Locality").agg({"city" : "count"}).groupby("city").agg({"city": "count"})
    grouped = grouped/grouped.sum()
    grouped["prop_city"] = grouped.cumsum()
#    plot = sns.barplot(data = grouped, x=grouped.index[0:50], y=grouped.prop_city[0:50])
#    plot.set(title="Cumulative amount of Localities per number of listings per locality", ylabel="% of total", xlabel="Listings per Locality")
#    plot.set_xlim(-1,25)


        #deeper look
    grouped = df_clean_outliers.groupby("city").agg({"Locality" : "count"}).groupby("Locality").agg({"Locality": "count"})
    grouped = grouped/grouped.sum()
    grouped["prop_city"] = grouped.cumsum()
#    plot = sns.barplot(data = grouped, x=grouped.index, y="prop_city")
#    plot.set(xlim=(-1,25), title="Cumulative amount of Cities per number of listings per locality", ylabel="% of total", xlabel="Listings per City")

    #Correlation by city
    numeric_corr = []
    for city in df_clean_outliers["city"].unique():
        df_by_city = df_clean_outliers[df_clean_outliers["city"] == city]
        if len(df_by_city.index) > 3:
            numeric_corr.append(df_by_city[["Bedroom", "Living_area", "Garden_area", "Surface_of_land", "Facade", "Price"]].corr()["Price"].to_frame(name=city))
    corr_by_city = pd.concat(numeric_corr, axis=1).transpose()
    corr_by_city = corr_by_city.iloc[:,:-1]
#    plot = sns.kdeplot(corr_by_city)
#    plot.set(title = "Distribution of correlation between Price and numeric values within each city"
#        , xlabel="Correlation"
#        , ylabel="Density"
#        ,xlim=(-1.2,1.2)
#        )

    #Categorical correlation by city
    cat_corr = []
    for city in df_clean_outliers["city"].unique():
        df_by_city = df_clean_outliers[df_clean_outliers["city"] == city].drop(["URL", "Locality", "District", "city", "Listing_address"] , axis=1)
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

def plot_liv(df, district = None):
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

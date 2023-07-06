#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import seaborn as sns
import matplotlib.pyplot as plt

def plot(df):
    #sns.relplot(data=df[df["Living_area"] > 50], y="Living_area", x="Price",kind="scatter", hue="Type")
#    sns.scatterplot(data=df[(df["Living_area"] > 50) & (df["Price"] < 1000000) &
#                 (df["Price"] > 80000)], x="Price", y="Living_area",hue="Type")
    #data = df.loc[:, ["Locality", "Price"]]
    data = df
    #data = data.groupby("Locality",as_index=False).Price.agg(["mean","count"])
    #data = data[data["count"]>10].sort_values("count")
    #print(data)
    data = data[(data["Living_area"] > 0) & (data["Living_area"] < 12000)]
    #print(data.groupby("Type", as_index=False).agg({"Living_area" :
    #                                                ["mean"]}))
    #sns.histplot(data=data,x="Living_area",hue="Type")
    data = data.groupby("Postal_code", as_index=False).agg({"Price": ["mean",
                                                                      "count"]
                                                            ,"lng" : ["max"]
                                                            ,"lat" : ["max"]
                                                           })
    #data[("Price", "count")] = data[("Price", "count")]*10
    sns.scatterplot(data=data,x=("lng", "max"),y=("lat", "max"),
                    size=("Price", "count"), sizes=(100,10000))
    plt.show()

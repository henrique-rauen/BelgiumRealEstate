#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import seaborn as sns
import matplotlib.pyplot as plt

def plot(df):
    print("trying to plot")
    #sns.relplot(data=df[df["Living_area"] > 50], y="Living_area", x="Price",kind="scatter", hue="Type")
#    sns.scatterplot(data=df[(df["Living_area"] > 50) & (df["Price"] < 1000000) &
#                 (df["Price"] > 80000)], x="Price", y="Living_area",hue="Type")
    data = df.loc[:, ["Locality", "Price"]]
    data = data.groupby("Locality",as_index=False).mean().sort_values(by="Price")
    sns.relplot(data=data,x="Locality", y="Price")
    plt.show()

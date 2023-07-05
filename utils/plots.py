#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import seaborn as sns
import matplotlib.pyplot as plt

def plot(df):
    print("trying to plot")
    sns.relplot(data=df[df["Living_area"] > 50], y="Living_area", x="Price",kind="scatter", hue="Type")
    plt.show()

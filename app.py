#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from src import model
import pandas as pd

dt = pd.read_csv("teste_data.csv")
#print(pd.get_dummies(dt["Type"]))
my_model = model.Model()
#dt = dt[dt["Open Fire"]==True]
dt = dt.tail(1060)
result = my_model.apply_model(dt)
print(result[["District", "Subtype", "Living_area","Open Fire","Surface_of_land","Price","Predictions"]])

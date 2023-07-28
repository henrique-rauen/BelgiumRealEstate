#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from . import utils as u
from . import model_funcs as m
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor


df = u.clean_df("../data/data.csv")
df = u.outliers(df)[0]
df_fancy = m.select_fancy_properties(df)
result = m.apply_model(LinearRegression(), df_fancy[["Price", "Living_area"]])
print(f"Avg Score for linear model on fancy residences: {result[1]}")

district_list=df_fancy["District"].value_counts()[0:10].index.to_list()
result = m.apply_model_district(LinearRegression(), df_fancy, district_list)
print(f"Avg Score for linear model on fancy residences by top 10 districts: {result[1]}")

result = m.apply_model(LinearRegression(), df_fancy.loc[~df_fancy["District"].isin(district_list), ["Price", "Living_area"]])
print(f"Avg Score for linear model on fancy residences outside top 10 districts: {result[1]}")
print(result[0].get_params())
#Looking at non linear models
df_dummies = pd.get_dummies(df[["Type"
       , "Subtype"
       , "Open Fire"
       , "State of the building"
       , "Kitchen"
       , "Furnished"
       , "District"
       ]])
df_dummies = pd.concat([df[["Price"
                           , "Living_area"
                           , "Bedroom"
                           , "Garden"
                           , "Open Fire"
                           , "Swimming_pool"
                            ]], df_dummies], axis=1)

print("Avg Score for decision tree: ", m.apply_model(
                                       DecisionTreeRegressor(max_leaf_nodes = 27)
                                       , df_dummies, True)[1])

#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from utils import clean_df
from plot_funcs import living_price, outliers
import model_funcs as m
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

def select_fancy_properties(df):
    fancy_subtypes = ['triplex', 'castle', "exceptional property"]
    df_fancy = df[df["Subtype"].isin(fancy_subtypes)]
    df_fancy = pd.concat([df_fancy
                        , df[df["Surface_of_land"] > 2000]
                        , df[df["Open Fire"] == True]
                        ])
    df_fancy.drop_duplicates(inplace=True)
    return df_fancy

def select_non_fancy_properties(df):
    non_fancy_subtypes = ["flat studio"
                          ,"loft"
                          ,"kot"
                          ,"other property"
                          ,"mixed use building"
                         ]
    df_non_fancy = df[df["Subtype"].isin(non_fancy_subtypes)]
    df_non_fancy = pd.concat([df_non_fancy
                        , df_non_fancy[df_non_fancy["Kitchen"] == "not installed"]
                        , df_non_fancy[df_non_fancy["Kitchen"] == "usa not installed"]
                        , df_non_fancy[df_non_fancy["State of the building"] == "TO_BE_DONE_UP"]
                        , df_non_fancy[df_non_fancy["State of the building"] == "TO_RENOVATE"]
                        , df_non_fancy[df_non_fancy["State of the building"] == "TO_RESTORE"]
                        ])
    df_non_fancy.drop_duplicates(inplace=True)
    return df_non_fancy

df = clean_df("../data/data.csv")
df = outliers(df)
df_fancy = select_fancy_properties(df)
result = m.apply_model(LinearRegression(), df_fancy[["Price", "Living_area"]])
print(f"Avg Score for linear model on fancy residences: {result[1]}")

district_list=df_fancy["District"].value_counts()[0:10].index.to_list()
result = m.apply_model_district(LinearRegression(), df_fancy, district_list)
print(f"Avg Score for linear model on fancy residences by top 10 districts: {result[1]}")

result = m.apply_model(LinearRegression(), df_fancy.loc[~df_fancy["District"].isin(district_list), ["Price", "Living_area"]])
print(f"Avg Score for linear model on fancy residences outside top 10 districts: {result[1]}")

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

#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
#Last Modified: 2023-07-05 10:59
import numpy as np
import pandas as pd

def clean_df(data):
    if isinstance(data,str): #Assumed to be file Path
        df = pd.read_csv(data)
    elif isinstance(data,pd.DataFrame):
        df = data
    else:
        print("unable to recognize argument")
        return None
    unwanted_data = ({"Type" : "apartment group"
                    })
    cleaned = remove_unwanted_data(df, unwanted_data)
    return cleaned

def fill_NaN(df,dic_defaults={}):
    for key,value in dic_defaults.items():
        for column in value:
            df[column]=df[column]

def remove_unwanted_data(df,dic_unwanted):
    for key,value in dic_unwanted.items():
        df = df[df[key] != value]
    return df

def remove_empty_spaces(df):
    
    return df

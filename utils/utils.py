#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
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
    unwanted_data = ({"Type" : "apartment group",
                      "Listing_ID": np.NaN
                    })
    cleaned = remove_unwanted_data(df, unwanted_data)
    NaN_defaults = ({False :  ["Furnished"]
                    })
    cleaned = fill_NaN(df, NaN_defaults)
    return cleaned

def fill_NaN(df,dic_defaults={}):
    for key,value in dic_defaults.items():
        for column in value:
            df[column]=df[column].fillna(key)
    return df

def remove_unwanted_data(df,dic_unwanted):
    for key,value in dic_unwanted.items():
        df = df[df[key] != value]
    return df

def convert_column_type(df,dic_convert):
    for key,value in dic_convert.items():

        df = df[df[key] != value]
    return df

def remove_empty_spaces(df):
    
    return df

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
    unwanted_data = ({"Type" : "apartment group"
                    })
    df = remove_unwanted_data(df, unwanted_data)
    NaN_defaults = ({False :  ["Furnished"]
                    ,-1 : ["Listing_ID", "Price"]
                    })
    df = fill_NaN(df, NaN_defaults)
    convert_column = ({int : ["Listing_ID"]
                    })
    df = convert_column_type(df,convert_column)
    return df

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
        for column in value:
            df[column] = df[column].apply(key)
    return df

def remove_empty_spaces(df):
    
    return df

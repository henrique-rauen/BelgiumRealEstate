#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
#Last Modified: 2023-07-05 10:10
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
    cleaned = remove_empty_spaces(df)
    return cleaned

def remove_empty_spaces(df):
    
    return df

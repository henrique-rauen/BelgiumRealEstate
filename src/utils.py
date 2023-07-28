#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import numpy as np
import pandas as pd

def clean_df(data):
    """Returns a df object cleaned using the rules specified below"""
    if isinstance(data,str): #Assumed to be file Path
        df = pd.read_csv(data)
    elif isinstance(data,pd.DataFrame):
        df = data
    else:
        print("unable to recognize argument")
        return None
    zips = pd.read_json("data/zipcode-belgium.json") #Adds the info from zip
    zips=zips[~zips.zip.duplicated()]
    zips["zip"]=zips["zip"].astype("string")
    df = pd.merge(df, zips, left_on="Postal_code", right_on="zip")
    df = fill_NaN(df, {False :  ["Furnished", "Garden"]
                         ,-1 : ["Listing_ID", "Price", "city", "Postal_code",
                                "Living_area"]
                        ,"not_available" : ["Kitchen", "State of the building", "District"]
                      })
    df = remove_unwanted_partial(df, {"Postal_code" : " "
                                        ,"Price" : "-"
                                     })
    df = remove_unwanted_data(df, {"Type" : "apartment group"
                                    ,"Listing_ID" : -1
                                    ,"Price" : -1
                                    ,"city" : -1
                                    , "Living_area" : -1
                                  })
    df = convert_column_type(df, {float : ["Listing_ID", "Bedroom", "Living_area",
                                            "Surface_of_land", "Facade",
                                            "Garden_area", "Price",
                                         "Postal_code"]
                                 })
    df = remove_empty_spaces(df, ["Type", "Subtype", "Listing_address",
                                 "Locality", "District", "Kitchen",
                                 "State of the building"
                                 ])
    df.set_index("Listing_ID",inplace=True)
    df = df[~df.index.duplicated()]
    df = df[~df.duplicated()]
    df = df[df["Postal_code"] <9999] #Weird zip code, few results get the knife
    dic_provinces = {(1000,1299) : "Brussels",
                     (1300,1499) : "Waals-Brabant",
                     (1500,1999) :"Vlaams-Brabant",
                     (3000,3499): "Vlaams-Brabant",
                     (2000,2999): "Antwerpen",
                     (3500,3999): "Limburg",
                     (4000,4999): "Luik",
                     (5000,5999): "Namen",
                     (6000,6599): "Henegouwen",
                     (7000,7999): "Henegouwen",
                     (6600,6999): "Luxemburg",
                     (8000,8999): "West-Vlaanderen",
                     (9000,9999): "Oost-Vlaanderen"
                    }
    df["Province"] = np.nan
    for k, v in dic_provinces.items():
        (df.loc[
            (df["Postal_code"] >= k[0]) &
            (df["Postal_code"] <= k[1])
            ,"Province"])= v
    return df

def outliers(df):
    """Remove outliers as defined by asssets more than 3 STD away
    from average on the columns price, Bedroom and Living_area"""
    std = df.select_dtypes('number').std()
    distance = abs(df.select_dtypes('number')-df.select_dtypes('number').mean()).div(std)
    price_outliers = distance.loc[distance["Price"] > 3, "Price"]
    bedroom_outliers = distance.loc[distance["Bedroom"] > 3, "Bedroom"]
    living_outliers = distance.loc[distance["Living_area"] > 3, "Living_area"]
    outliers=pd.concat([price_outliers, bedroom_outliers,living_outliers], axis=1)
    return df[~df.index.isin(outliers.index)], outliers

def fill_NaN(df,dic_defaults={}):
    """ Receives a df and a dictionary in the following format:
        {value_instead_of_NaN : [column1,column2, ...]}
        Substitues in columns NaN values for value_instead_of_NaN"""
    for key,value in dic_defaults.items():
        for column in value:
            df[column]=df[column].fillna(key)
    return df

def remove_unwanted_partial(df,dic_partial):
    """ Receives a df and a dictionary in the following format:
        {column_name : unnaceptable_str}
        Remove rows from df where column column_name CONTAINS unnaceptable_str
        """
    for key,value in dic_partial.items():
        if df[key].dtype == str:
            df = df[~df[key].str.contains(value)]
    return df

def remove_unwanted_data(df,dic_unwanted):
    """ Receives a df and a dictionary in the following format:
        {column_name : unnaceptable_value}
        Remove rows from df where column_name EQUALS unnaceptable_value
        """
    for key,value in dic_unwanted.items():
        df = df[df[key] != value]
    return df

def convert_column_type(df,dic_convert):
    """ Receives a df and a dictionary in the following format:
        {python_func : [column1, column2...]}
        Apply the function python_func to all columns on columns list
        """
    for key,value in dic_convert.items():
        for column in value:
            df[column] = df[column].apply(key)
    return df

def remove_empty_spaces(df, columns):
    """ Receives a list containing column names and apply the python strip
    function to them"""
    for col in columns:
        df[col] = df[col].apply(str.strip)
    return df

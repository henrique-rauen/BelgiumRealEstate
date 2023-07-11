#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import numpy as np

def correlation_ratio(categories, values):
    """Calculates the correlation ratio between a numeric variable and a
    category. Receives 2 pd.Series containing the categories and the values"""
    categories = np.array(categories)
    values = np.array(values)

    ss_category = 0
    ss_outside = 0
    if len(set(categories)) == 1:
        return np.NaN
    for category in set(categories): #Iterate only through distinct categories
        subgroup = values[np.where(categories == category)[0]]
        ss_category += sum((subgroup-np.nanmean(subgroup))**2)
        ss_outside += len(subgroup)*(np.nanmean(subgroup)-np.nanmean(values))**2
    return (ss_outside / (ss_outside + ss_category))**.5

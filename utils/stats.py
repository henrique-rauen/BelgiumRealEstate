#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import numpy as np
def correlation_ratio(categories, values):
    categories = np.array(categories)
    values = np.array(values)

    ss_category = 0
    ss_total = 0
    for category in set(categories): #Iterate only through distinct categories
        subgroup = values[np.where(categories == category)[0]]
        ss_category += sum((subgroup-np.mean(subgroup))**2)
        ss_total += len(subgroup)*(np.mean(subgroup)-np.mean(values))**2

    return (ss_total / (ss_total + ss_category))**.5

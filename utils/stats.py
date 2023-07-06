#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import numpy as np
def correlation_ratio(categories, values):
    categories = np.array(categories)
    values = np.array(values)

    ssw = 0
    ssb = 0
    for category in set(categories): #Iterate only through distinct categories
        subgroup = values[np.where(categories == category)[0]]
        ssw += sum((subgroup-np.mean(subgroup))**2)
        ssb += len(subgroup)*(np.mean(subgroup)-np.mean(values))**2

    return (ssb / (ssb + ssw))**.5

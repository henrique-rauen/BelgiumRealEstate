#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
#Last Modified: 2023-07-05 10:32
import src.utils as u
import src.explorations as pe
import pandas as pd
import numpy as np
import src.stats as s
from sklearn.model_selection import train_test_split

df = u.clean_df("data/data.csv")
#print(df)
pe.plot(df)
df.to_csv("teste_data.csv",index=False)

#df = pd.read_csv("teste_data.csv")
#std = df.select_dtypes('float').std()
#distance = abs(df.select_dtypes('float')-df.select_dtypes('float').mean()).div(std)
#living_outliers = distance.loc[distance["Living_area"] > 3, "Living_area"]
#df = df[~df.index.isin(living_outliers.index)]
#
#df_dummies = pd.get_dummies(df[["Type", "Province"]])
#df_regression = pd.concat([df[["Price", "Living_area"]], df_dummies], axis=1)
#
#X = df_regression[["Living_area", "Type_apartment", "Province_Antwerpen", "Province_Brussels", "Province_Henegouwen", "Province_Limburg", "Province_Luik", "Province_Luxemburg", "Province_Namen", "Province_Oost-Vlaanderen", "Province_Vlaams-Brabant", "Province_Waals-Brabant"]].to_numpy()
##X=np.append(X,np.ones(X.shape[0]).reshape(-1,1), axis=1)
##print(X)
#y = df_regression["Price"].to_numpy().reshape(-1,1)
#
#initial_guess = np.random.rand(X.shape[1],1)
#
#(X_train, X_test, y_train, y_test) = train_test_split(X,y)
#
#
#result = s.grad_descent(s.gradient_mae,s.linear_regression,X_train, y_train, initial_guess,0.01,1000)
#
#print(f"Score on the training data: {s.coef_determination(X_train,y_train)}")
#print(f"Score on the test data: {s.coef_determination(y_test,s.linear_regression(X_test, result))}")

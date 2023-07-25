#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler
import pandas as pd
import numpy as np

def train_model(model, df, show_individual_scores=False):
    """ For a given 'model' and 'df', applies the model 20 times with random test
    sampling and returns the last model and the avg score of the 20 iterations.
    If 'show_individual_scores is set to True, prints train and test scores for
    all 20 models"""
    X = df.drop(columns=["Price"]).to_numpy()
    y = df["Price"].to_numpy()
    avg_score = 0
    for i in range(20):
        (X_train, X_test, y_train, y_test) = train_test_split(X,y,test_size= 0.25)
        transformer = MaxAbsScaler().fit(X_train)
        X_train = transformer.transform(X_train)
        X_test = transformer.transform(X_test)
        regressor = model
        regressor.fit(X_train,y_train)
        score = regressor.score(X_test,y_test)
        avg_score = (avg_score * i + score)/(i+1)
        if show_individual_scores:
            print(f"Train score: {regressor.score(X_train, y_train)}, Test score: {score}")
    return regressor, avg_score

def train_model_district(model, df, district_list):
    """For a given 'model' and 'df', applies the model per district on
    'district_list'. Returns a dictionary whose keys are the districts and the
    items are the models for each district and the average score of all models"""
    df_dummies = pd.get_dummies(df["Type"])
    df_dummies.drop(columns=df_dummies.columns[-1], inplace=True)
    df_dummies = pd.concat([df[["Price", "Living_area", "District"]], df_dummies], axis=1)
    overall_score = []
    models ={}
    for district in district_list:
        df_regression = df_dummies[df_dummies["District"] == district]
        print(df_regression.shape)
        reg, score = train_model(model, df_regression.drop(columns=["District"]))
        overall_score.append(score)
        models[district] = reg
        print(f"Avg test score for district {district}: {score}")
    return models, np.mean(overall_score)

    def prepare_df(df, columns=None, filters=None):
        if columns:
            df = df[columns]
        if filters:
            df = df[df[filters[0]] == filters[1]]
        return df

    def predict_from_model(model, df):
        predictions = model.fit(df.to_numpy())
        df = df.assing("Predictions", predictions)
        return df

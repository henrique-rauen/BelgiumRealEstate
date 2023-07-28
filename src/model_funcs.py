#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def select_fancy_properties(df):
    fancy_subtypes = ['triplex', 'castle', "exceptional property"]
    df_fancy = df[df["Subtype"].isin(fancy_subtypes)]
    df_fancy = pd.concat([df_fancy
                        , df[df["Surface_of_land"] > 2000]
                        , df[df["Open Fire"] == True]
                        ])
    df_fancy.drop_duplicates(inplace=True)
    return df_fancy

def select_non_fancy_properties(df):
    non_fancy_subtypes = ["flat studio"
                          ,"loft"
                          ,"kot"
                          ,"other property"
                          ,"mixed use building"
                         ]
    df_non_fancy = df[df["Subtype"].isin(non_fancy_subtypes)]
    df_non_fancy = pd.concat([df_non_fancy
                        , df_non_fancy[df_non_fancy["Kitchen"] == "not installed"]
                        , df_non_fancy[df_non_fancy["Kitchen"] == "usa not installed"]
                        , df_non_fancy[df_non_fancy["State of the building"] == "TO_BE_DONE_UP"]
                        , df_non_fancy[df_non_fancy["State of the building"] == "TO_RENOVATE"]
                        , df_non_fancy[df_non_fancy["State of the building"] == "TO_RESTORE"]
                        ])
    df_non_fancy.drop_duplicates(inplace=True)
    return df_non_fancy

def train_model(df,model=LinearRegression(), show_individual_scores=False):
    """ For a given 'model' and 'df', applies the model 20 times with random test
    sampling and returns the last model and the avg score of the 20 iterations.
    If 'show_individual_scores is set to True, prints train and test scores for
    all 20 models"""
    df = prepare_df(df,columns=["Price"
                               ,"Living_area"
                               ,"apartment"],dummy_type=True)
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
    return [[regressor,transformer], avg_score]

def train_model_district(df, district_list,model=LinearRegression()):
    """For a given 'model' and 'df', applies the model per district on
    'district_list'. Returns a dictionary whose keys are the districts and the
    items are the models for each district and the average score of all models"""
    overall_score = []
    models ={}
    for district in district_list:
        df_regression = df[df["District"] == district]
        reg, score = train_model(df_regression, model)
        overall_score.append(score)
        models[district] = reg
    return [models, np.mean(overall_score)]

def prepare_df(df, columns=None, filters=None, dummy_type=False):
    if filters:
        df = df[df[str(filters[0])] == filters[1]]
    if dummy_type:
        df_dummy = pd.DataFrame({"apartment" : df["Type"]=="apartment"})
        df = pd.concat([df, df_dummy], axis=1)
    if columns:
        df = df[columns]
    return df

def predict_from_model(model, df):
    df = prepare_df(df,columns=["Living_area"
                               ,"apartment"],dummy_type=True)
    X = df.to_numpy()
    if len(X) > 0:
        X = model[1].transform(X)
        predictions = model[0].predict(X)
    else:
        predictions = []
    df = df.assign(Predictions = predictions)
    return df

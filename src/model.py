#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from utils import clean_df
from plot_funcs import outliers
from model_funcs import predict_from_model, prepare_df
import modelling as m
import pickle

class Model():
    def __init__(self):
        try:
            with open("fancy_district_model.pkl", "rb") as file:
                self._fancy_district_model = pickle.load(file)
            with open("fancy_model.pkl", "rb") as file:
                self._fancy_model = pickle.load(file)
            with open("ordinary_district_model.pkl", "rb") as file:
                self._ordinary_district_model = pickle.load(file)
            with open("ordinary_model.pkl", "rb") as file:
                self._ordinary_model = pickle.load(file)
        except:
            self.retrain_model(self,df)
            self.__init__(self)
        #Deafult train and prediction columns
        self._predict_columns = ["Living_area"]
        self._train_columns = ["Living_area","Price"]
        #Default Filter Operations and values
        self._fancy_filters = {"Subtype" : [pd.DataFrame.__eq__,['triplex'
                                                                ,'castle'
                                                                ,"exceptional property"]
                                            ]
                               ,"Surface_of_land": [pd.DataFrame.__gt__, 2000]
                               ,"Open Fire": [pd.DataFrame.__eq__, [True]]
                              }

    def retrain_model(self, df):
        df = clean_df(df)
        df = outliers(df)
        df_fancy = select_fancy_properties(df)
        district_list=df_fancy["District"].value_counts()[0:10].index.to_list()
        #Apply model to fancy homes by district
        result = m.apply_model_district(LinearRegression(), df_fancy, district_list)
        with open("fancy_district_model.pkl", "wb") as file:
            pickle.dumps(result[0],file)
        #Apply model to remaining fancy homes
        result = m.apply_model(LinearRegression()
                            ,df_fancy.loc[
                                    ~df_fancy["District"].isin(district_list)
                                    ,["Price", "Living_area"]
                                        ]
                              )
        with open("fancy_model.pkl", "wb") as file:
            pickle.dumps(result[0],file)
        df_ordinary = df[~df.index.isin(df_fancy.index)]
        district_list=df["District"].value_counts()[0:15].index.to_list()
        #Apply model to ordinary homes by district
        result = m.apply_model_district(LinearRegression(), df_ordinary, district_list)
        with open("ordinary_district_model.pkl", "wb") as file:
            pickle.dumps(result[0],file)
        #Apply model to remaining ordinary homes
        result = m.apply_model(LinearRegression()
                            ,df_ordinary.loc[
                                    ~df_ordinary["District"].isin(district_list)
                                    ,["Price", "Living_area"]
                                        ]
                              )
        with open("ordinary_model.pkl", "wb") as file:
            pickle.dumps(result[0],file)

    def apply_model(self, df):
        df["Predictions"] = 0
        #Select Fancy properties
        df_fancy = select_fancy_properties(df)
        df_fancy = prepare_df(df_fancy,columns=self._predict_columns)
        fancy_district_list = self._fancy_district_model.keys()
        #Update Predictions for fancy properties in top districts
        for district in fancy_district_list:
            local_df = prepare_df(df_fancy,filters=["District", district])
            pred = predict_from_model(self._fancy_district_model[district]
                                    ,local_df)
            df.loc[pred.index, "Predictions"] = pred["Predictions"]
        #Update Predictions for fancy properties outside top 10 districts
        local_df = df_fancy.loc[~df_fancy["District"].isin(fancy_district_list)
                                ,["Price", "Living_area"]
                                ]
        pred = predict_from_model(self._fancy_model, local_df)
        df.loc[pred.index, "Predictions"] = pred["Predictions"]

        #Select Ordinary properties
        df_ordinary = df[~df.index.isin(df_fancy.index)]
        df_ordinary = prepare_df(df_ordinary,columns=self._predict_columns)
        ordinary_district_list = self.ordinary_district_model.keys()
        #Update Predictions for ordinary properties in top districts
        for district in ordinary_district_list:
            local_df = prepare_df(df_ordinary,filters=["District", district])
            pred = predict_from_model(self._ordinary_district_model[district]
                                    ,local_df)
            df.loc[pred.index, "Predictions"] = pred["Predictions"]
        #Update Predictions for ordinary properties outside top districts
        local_df = df_ordinary.loc[~df_ordinary["District"].isin(ordinary_district_list)
                                ,["Price", "Living_area"]
                                ]
        pred = predict_from_model(self._ordinary_model, local_df)
        df.loc[pred.index, "Predictions"] = pred["Predictions"]

        return df

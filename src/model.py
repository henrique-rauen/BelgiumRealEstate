#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from . import utils as u
from . import plot_funcs as pf
from . import model_funcs as mf
from . import modelling as m
import pickle

class Model():
    def __init__(self):
        print("Trying to open model files...")
        try:
            with open("models/fancy_district_model.pkl", "rb") as file:
                self._fancy_district_model = pickle.load(file)
            with open("models/fancy_model.pkl", "rb") as file:
                self._fancy_model = pickle.load(file)
            with open("models/ordinary_district_model.pkl", "rb") as file:
                self._ordinary_district_model = pickle.load(file)
            with open("models/ordinary_model.pkl", "rb") as file:
                self._ordinary_model = pickle.load(file)
            print("Success!")
        except:
            print("Model files not found, trying to train new model based "
                  + "on data/data.csv")
            try:
                df = u.clean_df("data/data.csv")
                self.retrain_model(df)
                self.__init__()
            except:
                print("Unable to train model, object will be empty")
        #Deafult train and prediction columns
        self._predict_columns = ["Living_area", "Type"]
        self._train_columns = self._predict_columns + ["Price"]

    def retrain_model(self, df):
        df = pf.outliers(df)
        df_fancy = m.select_fancy_properties(df)
        #Apply model to fancy homes by district
        district_list=df_fancy["District"].value_counts()[0:10].index.to_list()
        result = mf.train_model_district(df_fancy, district_list)
        with open("models/fancy_district_model.pkl", "wb") as file:
            pickle.dump(result[0],file)
        #Apply model to remaining fancy homes
        local_df = df_fancy.loc[~df_fancy["District"].isin(district_list)]
        result = mf.train_model(local_df)
        with open("models/fancy_model.pkl", "wb") as file:
            pickle.dump(result[0],file)
        df_ordinary = df[~df.index.isin(df_fancy.index)]
        #Apply model to ordinary homes by district
        district_list=df["District"].value_counts()[0:15].index.to_list()
        result = mf.train_model_district(df_ordinary, district_list)
        with open("models/ordinary_district_model.pkl", "wb") as file:
            pickle.dump(result[0],file)
        #Apply model to remaining ordinary homes
        local_df = df_ordinary.loc[~df_ordinary["District"].isin(district_list)]
        result = mf.train_model(local_df)
        with open("models/ordinary_model.pkl", "wb") as file:
            pickle.dump(result[0],file)

    def _preprocess_data(self, df):
        df_fancy = m.select_fancy_properties(df)
        df_fancy_in_district = (df_fancy[df_fancy["District"]
                                .isin(self._fancy_district_model.keys())])
        df_fancy_out_district = (df_fancy[~df_fancy["District"]
                                .isin(self._fancy_district_model.keys())])
        df_ordinary = df[~df.index.isin(df_fancy.index)]
        df_ordinary_in_district = (df_ordinary[df_ordinary["District"]
                                .isin(self._ordinary_district_model.keys())])
        df_ordinary_out_district = (df_ordinary[~df_ordinary["District"]
                                .isin(self._ordinary_district_model.keys())])
        return (df_fancy_in_district
                ,df_fancy_out_district
                ,df_ordinary_in_district
                ,df_ordinary_out_district)

    def apply_model(self, df):
        df["Predictions"] = 0
        (df_fancy_in
         ,df_fancy_out
         ,df_ord_in
         ,df_ord_out) = self._preprocess_data(df)
        #Fancy properties in districts
        for district in df_fancy_in.District.unique():
            local = mf.prepare_df(df_fancy_in
                                  ,filters=["District", district]
                                  ,columns=self._predict_columns
                                  ,dummy_type=True)
            pred = mf.predict_from_model(self._fancy_district_model[district]
                                    ,local)
            df.loc[pred.index, "Predictions"] = pred["Predictions"]
        #Fancy properties out of districts
        local = mf.prepare_df(df_fancy_out
                                  ,columns=self._predict_columns
                                  ,dummy_type=True)
        pred = mf.predict_from_model(self._fancy_model,local)
        df.loc[pred.index, "Predictions"] = pred["Predictions"]
        #Ordinary properties in districts
        for district in df_ord_in.District.unique():
            local = mf.prepare_df(df_ord_in
                                  ,filters=["District", district]
                                  ,columns=self._predict_columns
                                  ,dummy_type=True)
            pred = mf.predict_from_model(self._ordinary_district_model[district]
                                    ,local)
            df.loc[pred.index, "Predictions"] = pred["Predictions"]
        #Fancy properties out of districts
        local = mf.prepare_df(df_ord_out
                                  ,columns=self._predict_columns
                                  ,dummy_type=True)
        pred = mf.predict_from_model(self._ordinary_model,local)
        df.loc[pred.index, "Predictions"] = pred["Predictions"]
        return df

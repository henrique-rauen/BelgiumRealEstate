#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from src import model
import pandas as pd
from fastapi import FastAPI, Body

description = """
This webApp allows you access to a modelling suit capable of predicting prices
of residences in Belggium using a few parameters.
"""

app = FastAPI()
title = "Immo Eliza modelling suit"
description = description
summary = "THE place to be if you want to know the price of your residence!"
contact = {"name": "Henrique Rauen", "url": "github.com/henrique-rauen"
           , "email": "rickgithub@hsj.email"}

@app.get("/")
def get():
    msg = {"data_format": "{'data' : {'Living_area': list(int) 'Type':"
           + "list('house' | 'apartment'), 'Subtype': list('triplex' | "
           + "'castle' | 'exceptional property' | 'others'), 'District':"
           + "list(str), 'Open Fire': list(bool)"
           +", 'Surface_of_land': list(int)}}"
         , "options": "Multiple simultaneous requests are allowed"
          }
    return msg

@app.post("/get_prediction/")
def get_prediction(payload : dict = Body()):
    mandatory_fields = ["Living_area"
                        ,"Type"
                        ,"District"
                        ,"Subtype"
                        ,"Open Fire"
                       ,"Surface_of_land"
                       ]
    msg ={}
    if "data" in payload.keys():
        if not all(v in payload["data"].keys() for v in mandatory_fields):
            msg["status_code"]= 400
            msg["error"]="Not all required fields were found"
            msg["prediction"]=[]
            #msg = ({'result' : 'Not all required fields were added, make sure the input is'
            #        + ' correct'})
        else:
            my_model = model.Model()
            data = pd.DataFrame.from_dict(payload["data"])
            data["Type"] = data["Type"].fillna("house")
            data["Living_area"] = data["Living_area"].fillna(0)
            result = my_model.apply_model(data)
            msg["status_code"]= 200
            msg["prediction"]=result["Predictions"].values.tolist()
            #msg = result.to_json()
    else:
        msg["status_code"]= 400
        msg["error"]="Input must constain 'data' field"
        msg["prediction"]=[]
    return msg

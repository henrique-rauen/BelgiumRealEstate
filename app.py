#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from src import model
import pandas as pd
from fastapi import FastAPI, Body

app = FastAPI()

#@app.get("/model")
#def get():
#
#    return msg

@app.post("/get_prediction/")
def get_prediction(payload : dict = Body()):
    mandatory_fields = ["Living_area"
                        ,"Type"
                        ,"District"
                        ,"Subtype"
                        ,"Open Fire"
                        ,"Surface_of_land"
                       ]
    if not all(v in payload.keys() for v in mandatory_fields):
        return ({'result' : 'Not all required fields were added, make sure the input is'
                + ' correct'})
    my_model = model.Model()
    data = pd.DataFrame.from_dict(payload)
    data["Type"] = data["Type"].fillna("house")
    data["Living_area"] = data["Living_area"].fillna(0)
    result = my_model.apply_model(data)
    return result.to_json()

#dt = pd.read_csv("teste_data.csv")
#my_model = model.Model()
##dt = dt[dt["Open Fire"]==True]
#dt = dt.head(6060)
#result = my_model.apply_model(dt)
#print(result[["District", "Subtype", "Living_area","Open Fire","Surface_of_land","Price","Predictions"]])

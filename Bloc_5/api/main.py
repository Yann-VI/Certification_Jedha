from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel, validator, ConfigDict
from typing import Literal, List, Union
import joblib
import json
import pandas as pd 
from fastapi.encoders import jsonable_encoder

app = FastAPI(
title="Getaround API",
description="""Welcome to my rental price predictor API !\n
Insert your car details to receive an estimation (ML model) on daily rental car price.
**Use the endpoint `/predict` to estimate the daily rental price of your car !**
"""
)

@app.get("/")
async def root():
    message = """Welcome to the Getaround API. Append /docs to this address to see the documentation for the API on the Pricing dataset."""
    return message



# Defining required input for the prediction endpoint
class Features(BaseModel):
    model_key: Literal['Citroën','Peugeot','PGO','Renault','Audi','BMW','Mercedes','Opel','Volkswagen','Ferrari','Mitsubishi','Nissan','SEAT','Subaru','Toyota','other'] 
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: Literal['diesel','petrol','other']
    paint_color: Literal['black','grey','white','red','silver','blue','beige','brown','other']
    car_type: Literal['convertible','coupe','estate','hatchback','sedan','subcompact','suv','van']
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool


# endpoint to predict the price of a car
#@app.post("/predict")
#async def predict(features:Features):
    """ 
Example :

{
  "model_key": "Audi",
  "mileage": 25000,
  "engine_power": 130,
  "fuel": "diesel",
  "paint_color": "blue",
  "car_type": "sedan",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": true,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": true
}

"""

 #   features = dict(features)
 #   input_df = pd.DataFrame(columns=['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps',
 #      'has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires'])
   # input_df.loc[0] = list(features.values())
    # Load the model & preprocessor
# Redirect automatically to /docs (without showing this endpoint in /docs)

# Make predictions
@app.post("/predict", tags=["Predictions"])
async def predict(cars: List[Features]):

    # Read input data
    car_features = pd.DataFrame(jsonable_encoder(cars))

    model = joblib.load('model_best.pkl')
    prep = joblib.load('preprocessor.pkl')
    X = prep.transform(car_features)
    pred = model.predict(X)
    return {"prediction" : pred[0]}


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
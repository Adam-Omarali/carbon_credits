#api - https://developers.google.com/earth-engine/apidocs


from typing import Union

from fastapi import FastAPI, Query
import ee
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#http://127.0.0.1:8000/getcanopybypoint/?lon=-122.21&lat=58.12
#-122.21, 58.12 -> 23
@app.get("/getcanopybypoint/")
def get_canopy(lon: float = Query(..., description="Longitude of the point"),
                lat: float = Query(..., description="Latitude of the point")):
    
    service_account = os.environ.get("SERVICE_ACCOUNT")
    credentials = ee.ServiceAccountCredentials(service_account, '.service_key.json')
    ee.Initialize(credentials)
    point = ee.Geometry.Point([lon, lat])
    img = ee.Image('users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1')

    zonal_max = img.select('b1').reduceRegion(    
        reducer=ee.Reducer.median(),
        geometry=point
    )

    return {zonal_max.get('b1').getInfo()}


# @app.get("/getcanopybyrectangle/")
# def get_canopy_area(lon: float = Query(..., description="Longitude of the point"),
#                 lat: float = Query(..., description="Latitude of the point"),
#                 width: float = Query(..., description="Width of Rectangle"),
#                 hegiht: float = Query(..., description="Height of Rectangle")):
    
#     service_account = os.environ.get("SERVICE_ACCOUNT")
#     credentials = ee.ServiceAccountCredentials(service_account, '.service_key.json')
#     ee.Initialize(credentials)
#     point = ee.Geometry.Rectangle([lon, lat])
#     img = ee.Image('users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1')

#     zonal_max = img.select('b1').reduceRegion(    
#         reducer=ee.Reducer.median(),
#         geometry=point
#     )

#     return {zonal_max.get('b1').getInfo()}

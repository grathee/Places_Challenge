# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 09:16:38 2016
@author: Geetika Rathee
"""
import numpy as np
import json
from geopy.geocoders import Nominatim
import os
from osgeo import ogr, osr

data = np.loadtxt('/home/user/Projects/AssignmentLesson15/places.txt', dtype=str)
#places = np.array(places_data, dtype='float')

print len(data)
coords_places = []

for places in data:
    geolocator = Nominatim()
    location = geolocator.geocode(places)
    print location
    y_coord = location.latitude 
    x_coord = location.longitude
    coords = [x_coord, y_coord]
    coords_places.append(coords)
    
os.chdir('/home/user/Projects/AssignmentLesson15')
print os.getcwd()

driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

## choose your own name
## make sure this layer does not exist in your 'data' folder
fn = "places_challenge.shp"
layername = "placeslayer"

## Create shape file
ds = drv.CreateDataSource(fn)

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
## Now check your data folder and you will see that the file has been created!

places_array = np.array(coords_places)

# SetPoint(self, int point, double x, double y, double z = 0)
i = 0

for i in range(len(coords_places)):
    pointi = ogr.Geometry(ogr.wkbPoint)
    pointi.SetPoint(0,places_array[i,0], places_array[i,1]) 
    layerDefinition = layer.GetLayerDefn()
    featurei = ogr.Feature(layerDefinition)
    featurei.SetGeometry(pointi)   
    layer.CreateFeature(featurei)
    i +=1
   
print "The new extent"
print layer.GetExtent()

ds.Destroy()
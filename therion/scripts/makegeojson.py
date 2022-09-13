import os
from os.path import isfile, join, dirname, abspath
import sys
import re
import argparse
import shutil
import subprocess
import tempfile
import pandas as pd

import shapefile
from json import dumps
import pyproj as proj
transformer = proj.Transformer.from_crs("epsg:32718", "epsg:4326")

# produce the cave centrelines

CONFIG_FILE = """
source ../data/index.th

export map -fmt esri -o ../data/gis
export model -fmt esri -o ../data/gis
"""

# write temporary config file
with open("temp.thconfig", 'w') as f:
    f.write(CONFIG_FILE)
    f.close()
subprocess.check_output("therion temp.thconfig", shell = True)
subprocess.check_output("rm temp.thconfig", shell = True)
subprocess.check_output("rm therion.log", shell = True)

# read the synthesis
DATA = pd.read_csv('../data/BROUILLON_cadastre/UP_MDD_DDA_Temp_synthese_Cavites_NumCad.csv')

SYNTHESE = DATA[['CAD_NUM','NomCadastre','Alt.','Dev. Topo','Prof.','UP','Explorateurs']]


reader = shapefile.Reader("../data/gis/stations3d.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
POINTS_FIXES = []

for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    # filter by centerline

    if 'ENT' in atr['_NAME']:

        try:
            vals = (SYNTHESE[SYNTHESE['CAD_NUM'] == atr['_NAME']].values[0])
            print(vals[0], vals[1])
            atr['_CAD_NUM'] = vals[0].strip('ENT_')
            atr['_CAVENAME'] = vals[1]
            atr['_LENGTH'] = vals[3]
            atr['_DEPTH'] = vals[4]
            atr['_ALTITUDE'] = vals[2]
            atr['_EXPED'] = vals[5]
            atr['_EXPLORATEURS'] = vals[6]
        except IndexError:
            atr['_CAD_NUM'] = atr['_NAME'].strip('ENT_')
            atr['_CAVENAME'] = 'not known'
            atr['_LENGTH'] = "not known"
            atr['_DEPTH'] = "not known"
            atr['_ALTITUDE'] = "not known"
            atr['_EXPED'] = "not known"
            atr['_EXPLORATEURS'] = "not known"
            pass

        #print(atr)
        geom = sr.shape.__geo_interface__
        X,Y = geom['coordinates']

        X2,Y2 =  transformer.transform(X,Y)
        geom['coordinates'] = (Y2,X2)


        POINTS_FIXES.append(dict(type="Feature", geometry=geom, properties=atr))

geojson = open("../data/gis/points_fixes.js", "w")
geojson.write("var pointsFixes = \n")
geojson.write(dumps({"type": "FeatureCollection", "features": POINTS_FIXES}, indent=2) + "\n")
geojson.close()

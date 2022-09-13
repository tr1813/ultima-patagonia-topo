import shapefile
from json import dumps
import os
from os.path import isfile, join, dirname, abspath
import subprocess


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
# read the shapefile for centrelines

reader = shapefile.Reader("../data/gis/lines2D.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    # filter by centerline
    if (atr['_TYPE'] == 'centerline'):
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    # write the GeoJSON file

geojson = open("../data/gis/lines2D.js", "w")
geojson.write("var visees = \n")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()


# read the shapefile for cadastral zones
#
# reader = shapefile.Reader("../data/gis/cadastre.geojson")
# fields = reader.fields[1:]
# field_names = [field[0] for field in fields]
# buffer = []
# for sr in reader.shapeRecords():
#     atr = dict(zip(field_names, sr.record))
#     # filter by centerline
#     if (atr['_TYPE'] == 'centerline'):
#         geom = sr.shape.__geo_interface__
#         buffer.append(dict(type="Feature", geometry=geom, properties=atr))
#
#     # write the GeoJSON file
#
# geojson = open("../data/gis/cadastre.js", "w")
# geojson.write("var visees = \n")
# geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
# geojson.close()

reader = shapefile.Reader("../data/gis/stations3d.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    # filter by centerline
    
    if 'ENT' in atr['_NAME']:      
        print(atr)
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    # write the GeoJSON file

geojson = open("../data/gis/points_fixes.js", "w")
geojson.write("var points_fixes = \n")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()

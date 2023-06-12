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

# read the generated therion file.
reader = shapefile.Reader("../data/gis/stations3d.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []

for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    # filter by centerline

    if 'ENT' in atr['_NAME']:
        #print(atr)
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    # write the GeoJSON file

THERION_STATUS_LIST = [(feature['properties']['_NAME'],feature['properties']['_COMMENT'],feature['geometry']['coordinates'][0],feature['geometry']['coordinates'][1]) for feature in buffer]
synthese_therion = pd.DataFrame(THERION_STATUS_LIST,columns = ['CadNum','Commentaire','X (UTM 18 Sud)','Y (UTM 18 Sud)'])

## read the cavity synthesis
excel_data = pd.read_csv("../data/SYNTHESE_POINTAGES.csv")
synthese_excel = excel_data[['Nom_complet','NomCadastre','Commentaire',
                                   'X (UTM 18 Sud)','Y (UTM 18 Sud)',
                                   'Alt.','Dev. Topo', 'Prof.','Explorateurs', 'UP']]


# check for each element in the therion generated file that there is a corresponding location
k=1
CADASTRE_NUMBER = {}
for element in synthese_excel.iterrows():

    LINE = []
    #print(element[1].values)
    LINE.append(element[1].values[0])
    for fixed_point in THERION_STATUS_LIST:
        try:
            if int(fixed_point[2]) == int(element[1][3]):
                if int(fixed_point[3]) == int(element[1][4]):
                    #print(fixed_point[0],element[1][0])
                    LINE.append(fixed_point[0])
                    LINE.append(element[1].values)

        except ValueError:
            #print("coordinates are likely NaN")
            pass
    if len(LINE) == 1:
        LINE.append("ENT_NEW_{}".format(k))
        k+=1
        LINE.append(element[1].values)

    CADASTRE_NUMBER = {**CADASTRE_NUMBER, LINE[1]:LINE[2]}

    # transform dictionary to dataframe
NOUVELLE_SYNTHESE = pd.DataFrame(CADASTRE_NUMBER).transpose()
# rename columns
NOUVELLE_SYNTHESE.columns = ['NomComplet','NomCadastre','Commentaire',
                            'X_UTM18S','Y_UTM18S','Z','Dévelopement',
                            'Dénivellé',"Explorateurs",'UP']
# put cadaster number as index and sort.
NOUVELLE_SYNTHESE.sort_index(inplace = True)

# put cadaster number as index and sort.
synthese_therion.index = synthese_therion['CadNum']
synthese_therion.sort_index(inplace = True)


# join the dataframes
SYNTHESE_POINTAGES = NOUVELLE_SYNTHESE.join(synthese_therion, rsuffix = "_therion", how = 'outer')

print(SYNTHESE_POINTAGES.columns)
# save to csv
SYNTHESE_POINTAGES[['NomComplet','NomCadastre','Commentaire','X_UTM18S',
                    'Y_UTM18S','Z','Dévelopement',
                    'Dénivellé',"Explorateurs",'UP']].to_csv('../SYNTHESE_POINTAGES.csv')

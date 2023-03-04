import pandas as pd


# read the data into a pandas dataframe.
df = pd.read_csv("./therion/data/SYNTHESE_POINTAGES.csv")

print(df.head())

LINEFORMAT = """
<wpt lat="{latitude}" lon="{longitude}"> 
<sym>cave</sym>
<name> {name} </name>  
<cmt> {complete_name}: {comment} </cmt>  
<geoidheight> {altitude}  </geoidheight>     
 </wpt>
"""

FILEFORMAT = """
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<gpx version="1.1" creator="Centre Terre">
  <metadata> Fichier GPX cree a partir de la synthese des pointages Ultima Patagonia </metadata>
{data}
</gpx>
"""

DATA = ""

for index,i in df.iterrows():
    if i.comment == "nan":
        comment = ""
    else:
        comment = i.comment
    if i.longitude != "inf"  and i.latitude != "inf":
        print(type(i.longitude))
        FORMATTED = LINEFORMAT.format(latitude=i.latitude,
        longitude = i.longitude, 
        comment = i.comment,
        name = i.cadnum,
        complete_name= i.complete_name,
        altitude = i.altitude,
        )   
        DATA += FORMATTED

FILE = FILEFORMAT.format(data = DATA)

with open("./therion/data/SYNTHESE_POINTAGES.gpx", "w+") as f:
    f.writelines(FILE)

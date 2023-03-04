import pandas as pd
import time


# 2010-01-04T23:37:42Z
timenow =  time.localtime()
timestamp = f"{timenow.tm_year}-{timenow.tm_mon}-{timenow.tm_mday}T{timenow.tm_hour}:{timenow.tm_min}:{timenow.tm_sec}Z"


TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<gpx
  version="1.0"
  creator="Centre Terre"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns="http://www.topografix.com/GPX/1/0"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
<time>'{time}'</time>
<bounds minlat="-52" minlon="-72" maxlat="49" maxlon="-70"/>
{data}
</gpx>"""

WPT_TEMPLATE = """
<wpt lat="{latitude}" lon="{longitude}">
  <ele>{elevation}</ele>
  <name>{name}</name>
  <cmt>{comment}</cmt>
  <desc>{description}</desc>
  <sym>{symbol}</sym>
</wpt>"""

def pyToGPX(fp):

  # "../../therion/data/SYNTHESE_POINTAGES.csv"
  data = pd.read_csv(fp)

  waypoints = ""

  for index,line in data.iterrows():

    if ("camp" in line.complete_name) or ("Camp" in line.complete_name):
      symbol= "Lodging"
    else:
      symbol = "Waypoint"

    formatted = WPT_TEMPLATE.format(
      
      latitude= line.latitude,
      longitude= line.longitude,
      elevation= line.altitude,
      comment= line.cadnum,
      name= line.complete_name,
      description= line.comment,
      symbol= symbol
    )

    if "inf" not in formatted:
      waypoints+=formatted

  with open(fp.strip("csv") + "gpx", "w+") as f:
      f.write(TEMPLATE.format(data=waypoints,time = timestamp))

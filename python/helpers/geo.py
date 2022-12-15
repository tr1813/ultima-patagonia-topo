from dataclasses import dataclass, field
from typing import Tuple
from  shapely.geometry import shape, Point
import fiona
import pyproj as proj
from os.path import abspath

@dataclass
class coordinatePairUTM:
    """A class that expects two floats"""
    x : float
    y : float
    cadnum_root : str = field(init=False)
    sector_name : str = field(init=False)
    _orig_lat : float = field(init=False)
    _orig_long : float = field(init=False)
    
    def add_lat_long(self,lat,long) -> None:
        """Attributes exploration zone to the cave"""
        self._orig_lat,self._orig_long = lat,long
    
    def add_lat_long_from_xy(self) -> None:
        self._orig_lat,self._orig_long = transformer(crs_in='epsg:32718',crs_out='epsg:4326').transform(self.x,self.y)

    def add_sector(self) -> None:
        pt = Point(self._orig_long,self._orig_lat)
        fp = abspath("../therion/data/gis/secteurs.shp")
        multipolygons = read_multipolygons(fp)
        intersects = [(pt.within(poly),properties) for poly,properties in multipolygons]
        
        self.cadnum_root = "undefined"
        self.sector_name = "undefined"
        for intersect,property in intersects:
            if intersect:
                self.cadnum_root = property["Cadastre_I"]
                self.sector_name = property["Nom"]

@dataclass
class coordinatePairLatLong:
    """A class containing Latitude and Longitude values"""
    lat : str
    long : str
    hemisphere : tuple = field(init=False, default_factory=tuple)
    lat_asfloat : float = field(init=False)
    long_asfloat : float = field(init=False)

    def __post_init__(self) -> None:
        """convert however the latitude and longitude are given to decimal format."""

        self.parse_hemisphere()
        if (self.lat.__contains__('°')) and (self.lat.__contains__("'")) and (self.lat.__contains__("''")):
            self.parse_degree_minutes_seconds()
        elif(self.lat.__contains__('°')) and (self.lat.__contains__("'")):
            self.parse_degree_decimal_minutes()
        else:
            self.parse_decimal_degrees()

    def parse_hemisphere(self) -> None:
        """Parses the lat/long coordinates given and determines in which hemisphere to go"""
        if self.lat.__contains__('N'):
            NH = 1
        else:
            NH = -1

        if self.long.__contains__('E'):
            EH = 1
        else:
            EH = -1
        self.hemisphere = (NH,EH)

    def parse_decimal_degrees(self) -> None:
        """Parses lat/long coordinates to a decimal float"""
        self.lat_asfloat = self.hemisphere[0] * float(self.lat.strip('N').strip('S').split('°')[0])
        self.long_asfloat = self.hemisphere[1] * float(self.long.strip('E').strip('W').split('°')[0])

    def parse_degree_decimal_minutes(self) -> None:
        """Parses lat/long coordinates to a decimal float"""

        lat_split = self.lat.strip('N').strip('S').split('°')
        long_split = self.long.strip('E').strip('W').split('°')
        lat_degree = float(lat_split[0])
        long_degree = float(long_split[0])
        lat_mins = float(lat_split[1].split("'")[0])
        long_mins = float(long_split[1].split("'")[0])
        self.lat_asfloat = self.hemisphere[0] * (lat_degree + lat_mins/60)
        self.long_asfloat = self.hemisphere[1] * (long_degree + long_mins/60)

    def parse_degree_minutes_seconds(self) -> None:
        """Parses lat/long coordinates to a decimal float"""

        lat_split = self.lat.strip('N').strip('S').split('°')
        long_split = self.long.strip('E').strip('W').split('°')
        lat_degree = float(lat_split[0])
        long_degree = float(long_split[0])
        lat_mins = float(lat_split[1].split("'")[0])
        long_mins = float(long_split[1].split("'")[0])
        lat_secs = float(lat_split[1].split("'")[1])
        long_secs = float(long_split[1].split("'")[1])
        
        self.lat_asfloat = self.hemisphere[0] * (lat_degree + lat_mins/60 + lat_secs/3600)
        self.long_asfloat = self.hemisphere[1] * (long_degree + long_mins/60 + long_secs/3600)
        
def read_multipolygons(filepath: str) -> list:
    """Reads a shapefile of exploration zones and makes a list of polygons"""
    dataset = fiona.open(filepath)
    multipolygons = [(shape(poly["geometry"]), poly["properties"]) for poly in dataset] # type: ignore

    return multipolygons 

def transformer(crs_out: str ,crs_in: str) -> proj.Transformer:
    """A function returning a transformer instance based on crs codes"""
    return proj.Transformer.from_crs(crs_in, crs_out)

TRANSFORMER_LATLONG = transformer(crs_in="epsg:4326", crs_out="epsg:32718") 

def convert_coords(coord : coordinatePairLatLong) -> coordinatePairUTM:
    """Convert from lat-long to UTM18S"""
    
    X,Y = TRANSFORMER_LATLONG.transform(coord.lat_asfloat,coord.long_asfloat)
    return coordinatePairUTM(x=X,y=Y)



import profile
import pstats
profile = profile.Profile()

#profile.runcall(convert_coords)
ps = pstats.Stats(profile)
ps.print_stats()
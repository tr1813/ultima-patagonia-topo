from dataclasses import dataclass,field
from enum import Enum
import pandas as pd
import numpy as np
from os.path import abspath, exists

from helpers.geo import * 
#from geo import *
from subprocess import check_output, CalledProcessError

class Expedition(str, Enum):
    """A class to represent the different expeditions"""

    UP2006 = "UP2006"
    UP2008 = "UP2008"
    UP2010 = "UP2010"
    UP2014 = "UP2014"
    UP2017 = "UP2017"
    UP2019 = "UP2019"
    UP2023 = "UP2023"
    unknown = "unknown"

def assignExpedition(name: str) -> Expedition:
    """Assign the correct expedition given a date"""
    target = Expedition.unknown

    for expedition in Expedition:
        if expedition.name.__contains__(name):
            target = expedition
    
    return target

@dataclass
class Cave:
    """A class that contains the information about a specific cavity"""
    cadnum : str
    exped : Expedition
    comment : str
    altitude : str
    _index : int 
    coordinates : coordinatePairUTM = coordinatePairUTM(x=-999.,y=-999.)
    name : str = "undefined"
    length: float = 0
    depth : float = 0
    complete_name: str = "undefined"
    explorers : str = "undefined"
    _search_string : str = field(init=False)
    _folder_path : str = field(init=False)
    _sector_folder_path : str = field(init=False)


    def __post_init__(self) -> None:
        self._search_string=f"{self.cadnum} {self.name}"

        # set the local folder path for the caves

    def add_coordinates(self, coords : coordinatePairUTM) -> None:
        """A method for adding coordinates to the Cave entry"""
        self.coordinates = coordinatePairUTM(coords.x,coords.y)
        self.coordinates.add_lat_long_from_xy()
        self.coordinates.add_sector()
        self._folder_path = f"../therion/data/{self.cadnum[:-3]}/{self.name}"
        self._sector_folder_path = f"../therion/data/{self.cadnum[:-3]}/{self.cadnum[:-3]}.th"


    def makeTheriontemplate(self) -> str:
        """ Generate an empty therion file using the cave data"""

        TEMPLATE = f"""survey {self.name} -title '{self.complete_name}' \\
            -attr cadnum {self.cadnum} \\
            -attr exped {self.exped}\n
            
        \tcentreline
        \t\tcs epsg:32718
        \t\t#fix ENT {self.coordinates.x} {self.coordinates.y} {self.altitude}

        \t#explo-date {self.exped}
        \t#team "{self.explorers}"
        
        \tunits length meters
        \t units compass clino degrees
        \tdata normal from to tape compass clino
        \t#<RENSEIGNER LES DONNEES ICI>

        \tendcentreline

        endsurvey
        """

        return TEMPLATE


    def make_folder(self) -> None:
        """A method which creates an empty folder for the cave of interest."""
        filepath = abspath(self._folder_path).strip('\n')
        print(filepath)

        try:
            check_output(f'mkdir {filepath}', shell=True)
            cavename = self.name.strip("\n").strip(' ')
            TH_FILE = f'{filepath}/{cavename}.th'
            print("Name of the filepath",TH_FILE)
            MD_FILE = f"{filepath}/NOTES.md"

            if not exists(TH_FILE):
                with open(TH_FILE, 'w+') as th_file:
                    th_file.write(self.makeTheriontemplate())
                with open(MD_FILE, 'w+') as md_file:
                    md_file.write(self.comment)
                
        except CalledProcessError:
            TH_FILE = f"{filepath}/{self.name}.th"
            MD_FILE = f"{filepath}/NOTES.md"
            
            if not exists(TH_FILE):
  
                with open(TH_FILE, 'w+') as th_file:
                    th_file.write(self.makeTheriontemplate())
                with open(MD_FILE, 'w+') as md_file:
                    md_file.write(self.comment)
            pass

    def make_entry_in_sector_file(self) -> None:
        """adds an entry line to the sector .th file"""
        with open(self._sector_folder_path, "r+") as f:
            lines = f.readlines()

            startindex = [x for x,line in enumerate(lines) if ("centreline" in line) or ("centerline" in line)]
            formatted = f"""
    #input {self.name}/{self.name}.th
            """
            lines.insert(startindex[0]-1,formatted)
            f.seek(0)
            endindex = [x for x,line in enumerate(lines) if ("endcentreline" in line) or ("endcenterline" in line)]
            name_as = f'"{self.complete_name}"'
            formatted = f"""
    fix ENT_{self.cadnum}	{self.coordinates.x} {self.coordinates.y}	{self.altitude}	
    station ENT_{self.cadnum} {name_as}
    #equate ENT_{self.cadnum} 0@{self.name}
    
  """
            lines.insert(endindex[0],formatted)
            f.seek(0)
            f.writelines(lines)

class CaveExistsError(Exception):
    pass

class CaveNotFoundError(Exception):
    pass

@dataclass
class CaveCadaster:
    """A class that expects a list of caves and contains methods for reporting info about these caves"""
    caves : list[Cave] = field(default_factory=list)

    def add_entry(self, cave: Cave) -> None:
        """Enter an instance of a Cave to the database"""
        self.caves.append(cave)

    def check_existing(self, cave: Cave) -> None:
        """Check from a cave's coodinates that it does not already exist in the cadaster"""

        for existing_cave in self.caves:
            if cave.coordinates.x != float('nan'):
                dist = np.sqrt((cave.coordinates.x - existing_cave.coordinates.x)**2 + (cave.coordinates.y - existing_cave.coordinates.y)**2)
                if dist < 1:
                    raise CaveExistsError("the cave exists already")

    def find_cave(self,search_string: str) -> Cave:
        """Return a Cave instance given a cadastral number"""

        targets = []
        for cave in self.caves:
            if cave._search_string.__contains__(search_string):
                targets.append(cave)

        if len(targets)==1: # only if one target found
            return targets[0]
        elif len(targets)>1:
            raise CaveNotFoundError("there may be two caves with this cadastral number")
        else:
            raise CaveNotFoundError("there is no cave with this cadastral number")

    def delete_cave(self, search_string: str) -> None:
        cave = self.find_cave(search_string)

        proceed = input("Are you sure you want to delete this cave entry? Type <y/n> to proceed.")
        if proceed == 'y':
            self.caves.remove(cave)
            print(f"Deleting the cave '{cave.name}' from the database")
        else:
            print(f"keeping the cave '{cave.name}' in the database")

    def generate_dataframe(self) -> pd.DataFrame:
        """A method which generates a pandas.DataFrame out of the list of caves objects"""
        lines = []
        for cave in self.caves:
            line = [cave.cadnum,
            cave.coordinates.sector_name,
            cave.complete_name,
            f'{cave.name}',
            cave.comment,
            cave.coordinates.x,
            cave.coordinates.y,
            cave.altitude,
            cave.length,
            cave.depth,
            cave.explorers,
            cave.exped,
            f"{cave.coordinates._orig_lat:.7f}",
            f"{cave.coordinates._orig_long:.7f}"
            ]

            lines.append(line)

        cols = ['cadnum',
        'secteur',
        'complete_name',
        'name',
        'comment',
        'X_UTM18S',
        'Y_UTM18S',
        'altitude',
        'length',
        'depth',
        'explorers',
        'exped',
        'latitude',
        'longitude']

        return pd.DataFrame(lines,columns=cols)
    
    def write_to_file(self, output_path: str)-> None:
        """Writing the pandas.DataFrame to a file formatted exactly as expected for rereading into cave cadaster"""
        df = self.generate_dataframe()
        df.sort_values(by='cadnum', inplace =True)
        df.to_csv(output_path)

def generate_entry_from_file(df: pd.DataFrame, row: int) -> Cave:
    """A function to generate an entry from a specific line of a formatted dataframe"""
    line = df.loc[row]

    coords  = coordinatePairUTM(x=line.X_UTM18S,y=line.Y_UTM18S)
    coords.add_lat_long(lat=line.latitude,long=line.longitude)
    coords.add_sector()

    cave = Cave(
        cadnum=line.cadnum,
        exped= assignExpedition(str(line.exped)),
        comment=line.comment,
        altitude= line.altitude,
        coordinates=coords,
        name= line['name'],
        complete_name= line.complete_name,
        explorers= line.explorers,
        length= line.length,
        depth= line.depth,
        _index = row
    ) # type: ignore
    return cave
  
def initialise_database(filepath : str) -> CaveCadaster:
    """Reads a csv file containing the cave data into a CaveCadaster object"""
    df = pd.read_csv(filepath)
    cadaster = CaveCadaster()

    for row in range(len(df)):
        cadaster.add_entry(generate_entry_from_file(df,row))
    
    return cadaster

# play with a subclass for the different sectors of cave exploration.
@dataclass
class CadasterSector(CaveCadaster):
    """A cave cadaster subclass"""
    
    parent : CaveCadaster = CaveCadaster()
    name : str = 'undefined'
    root_cadnum : int = 999
    caves: list[Cave] = field(init = False, default_factory=list)
    next_cad_num : int = field(init=False)

    def __post_init__(self) -> None:
        self.caves = [cave for cave in self.parent.caves if str(cave.cadnum)[:3].__contains__(str(self.root_cadnum))]
        self.next_cad_num = self.root_cadnum*1000+len(self.caves)+1

    def add_entry(self, cave: Cave) -> None:
        self.next_cad_num +=1
        return super().add_entry(cave)


## test


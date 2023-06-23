from dataclasses import dataclass, field
import re

@dataclass 
class Date:
    """A class which represents a string formatted date"""
    year : int = 2000
    month : int = 1
    day : int = 1
    date_string : str = field(init = False)

    def __post_init__(self) -> None:
        self.date_string = f"{self.year}.{self.month:02d}.{self.day:02d}"

@dataclass 
class StationWithComment:
    name : str
    comment : str
    command : str = field(init=False)

    def __post_init__(self) -> None:
        self.command = f'station {self.name} "{self.comment}"'

@dataclass
class LineLRUD:
    from_station : str
    left : float
    right : float 
    up : float
    down : float

@dataclass 
class DataLine:
    from_station : str
    to_station : str
    tape : float
    compass : float


@dataclass
class NormalDataLine(DataLine):
    clino : float

@dataclass
class DivingDataLine(DataLine):
    to_depth : float
    from_depth : float

@dataclass
class Centreline:

    explo_date : Date = Date()
    explorers : list[str] = field(init= False, default_factory= list)
    type : str = "normal"
    data_header : list[str] = field(init= False, default_factory= list)
    units_length : dict[str, str] = field(default_factory=lambda: {"units length" : "meters"})
    units_compass_clino :  dict[str, str] = field(default_factory=lambda: {"units compass clino": "degrees"})
    lrud_reader : list[str] = field(default_factory=lambda: ["data", "dimensions", "station", "left", "right", "up", "down"])
    data : list[DataLine] = field(init=False, default_factory= list)
    lrud_data : list[LineLRUD] = field(init=False, default_factory= list)
    commented_stations : list[StationWithComment] = field(init=False, default_factory=list)
    _string_repr : str = field(init=False, default_factory= str)

    def __post_init__(self) -> None:
        if self.type == 'normal':
            self.data_header = ["data", "normal", "from", "to", "tape", "compass", "clino"]
        elif self.type == "normal_backclino":
            self.data_header = ["data", "normal", "from", "to", "tape", "compass", "backclino"]
        elif self.type == "normal_backcompass":
            self.data_header = ["data", "normal", "from", "to", "tape", "backcompass", "clino"]
        elif self.type == "normal_backcompass_backclino":
            self.data_header = ["data", "normal", "from", "to", "tape", "backcompass", "backclino"]
        elif self.type == "diving":
            self.data_header = ["data", "diving",  "from", "fromdepth","to", "todepth", "tape", "compass"]
        elif self.type == "diving_backcompass":
            self.data_header = ["data", "diving",  "from", "fromdepth","to", "todepth", "tape", "backcompass"]
                    
    def add_explorers(self, explorers : list[str]) -> None:
        self.explorers += explorers

    def add_dataline(self, line: DataLine) -> None:
        self.data+= [line]

    def add_station_line(self, station : StationWithComment) -> None:
        self.commented_stations.append(station)

    def add_LRUDdataline(self, line: LineLRUD) -> None:
        self.lrud_data+= [line]

    def add_Date(self, date: str) -> None:
        DATE = date.split(".")
        self.date = Date(year=int(DATE[0]),month=int(DATE[0]),day=int(DATE[2]))
        self.explo_date = Date(year=int(DATE[0]),month=int(DATE[1]),day=int(DATE[2]))

    def update_type(self, type: str):
        self.type = type
        self.__post_init__()

    def add_string_repr(self) -> None:
        
        explorers = ""
        for explorer in self.explorers:
            explorers += f"explo-team {explorer}\n\t"

        formatted_data : str = ""
        formatted_lrud : str = ""
        formatted_comments : str = ""


        for line,lrud_line in zip(self.data,self.lrud_data):
            if "clino" in self.data_header:
                formatted_data += f"""
        {line.from_station}\t{line.to_station}\t{line.tape}\t{line.compass}\t{line.clino}\t""" # type: ignore
                formatted_lrud += f"""
        {lrud_line.from_station}\t{lrud_line.left}\t{lrud_line.right}\t{lrud_line.up}\t{lrud_line.down}\t"""
                
            elif "todepth" in self.data_header:
                formatted_data += f"""
        {line.from_station}\t{line.from_depth}\t{line.to_station}\t{line.to_depth}\t{line.tape}\t{line.compass}\t""" # type: ignore
                formatted_lrud += f"""
        {lrud_line.from_station}\t{lrud_line.left}\t{lrud_line.right}\t{lrud_line.up}\t{lrud_line.down}\t"""
                
        for comment in self.commented_stations:
            formatted_comments += f"""
        {comment.command}"""

        self._string_repr = f"""
    centreline
    
        explo-date {self.explo_date.date_string}
        date {self.explo_date.date_string}

        {explorers}
        {join(self.data_header)}
        {formatted_data}

        {join(self.lrud_reader)}
        {formatted_lrud}

        {formatted_comments}

    endcentreline"""

@dataclass
class Survey:
    name : str
    entrance : str = field(init= False, default_factory= str)
    centrelines : list[Centreline] = field(init= False, default_factory= list)
    _string_repr : str = field(init=False, default_factory= str)


    def add_centrelines(self, centrelines:  list[Centreline]) -> None:
        self.centrelines += centrelines
    
    def add_entrance(self, entrance : str) -> None:
        self.entrance = entrance

    def add_string_repr(self) -> None:

        centrelines = ""
        for centreline in self.centrelines:
            centrelines += f"{centreline._string_repr}\n"

        self._string_repr = f"""
## a survey compiled from Visual Topo Data using the visual_therion.py script

survey "{self.name}" -entrance {self.entrance}
{centrelines}
endsurvey
"""

@dataclass
class StrategyParser:
    input_str : str
    compass : str = "normal"
    clino : str = "normal"
    strategy_name: str = "normal"

    def __post_init__(self) -> None:
        if "Dir,Dir,Inv" in self.input_str:
            self.clino = "back"
            self.strategy_name = "normal_backclino"

        elif "Inv,Inv,Dir" in self.input_str or "Inv,Dir,Dir" in self.input_str:
            self.compass = "back"
            if "Prof" in self.input_str:
                self.strategy_name = "diving_backcompass"
            else: 
                self.strategy_name = "normal_backcompass"

        elif "Inv,Inv,Inv" in self.input_str:
            self.compass = "back"
            self.clino = "back"
            self.strategy_name = "normal_backcompass_backclino"

        elif ("Dir Dir Dir" in self.input_str) and ("Prof") in self.input_str:
            self.strategy_name = "diving"


def join(l : list[str])-> str:
    newstr = ""

    for elem in l:
        newstr += f"{elem} "

    return newstr

def find_entrance_stn(data: list[str], format : str) -> str:
    if format == "tro":
        """Search the visual topo file for the entrance station"""
        for c,l in enumerate(data):
            if 'Entree' in l:
                entrance_stations = re.findall(r"(?<=Entree\s).+",l)
    else: 
        for c,l in enumerate(data):
            if '<Entree>' in l:
                entrance_stations = re.findall(r"(?<=<Entree>)[0-9a-z]+",l)
    
    return entrance_stations[0] # type: ignore


def return_centreline_params(data: list[str], fmt: str):
    if fmt == "tro":
        return return_centreline_params_tro(data)
    else: 
        return return_centreline_params_trox(data)

def return_centreline_params_trox(data):
    start,end = [],[]
    survey_dates = []
    surveyor_groups = []

    for c,l in enumerate(data):
        if ('Param' in l) and ('/Param' not in l):
            if 'Comment' in data[c+1]:
                if len(start) >= 1:
                    end.append(c-1)
                start.append(c+2)
            else:
                if len(start) >= 1:
                    end.append(c-1)
                start.append(c+1)

            reg_explodate = re.findall(r'(?<=Date\=")\d\d\/\d\d\/\d\d\d\d', l)
            reg_explodate = [elem for elem in reg_explodate[0].split("/")]
            explodate = "{yyyy}.{mm}.{dd}".format(yyyy =reg_explodate[2], mm =reg_explodate[1], dd = reg_explodate[0])
            if len(explodate) == 0:
                survey_dates.append('')
            else:
                survey_dates.append(re.sub(r"/",".",explodate))
            tp = re.findall(r"(?<=Topo réalisée par )[\w+\s]*",l)
            if len(tp) == 0:
                surveyor_groups.append('')
            else:
                surveyor_groups.append(tp[0].split(' '))
        elif 'Configuration' in l:
            end.append(c-1)

    return surveyor_groups,survey_dates,start,end


def return_centreline_params_tro(data):
    # find the parameters of the file.
    start,end = [],[]
    survey_dates = []
    surveyor_groups = []

    for c,l in enumerate(data):
        if 'Param' in l:
            if len(start) >= 1:
                end.append(c-1)
            start.append(c+1)


            explodate = re.findall(r"\d\d.\d\d.\d\d", l)
            if len(explodate) == 0:
                survey_dates.append('')
            else:
                survey_dates.append(re.sub(r"-",".",explodate[0]))
            tp = re.findall(r"(?<=Topo réalisée par )[\w+\s]*",l)
            if len(tp) == 0:
                surveyor_groups.append('')
            else:
                surveyor_groups.append(tp[0].split(' '))
        elif 'Configuration' in l:
            end.append(c-1)

    return surveyor_groups,survey_dates,start,end



def parseFloat(x: str) -> float:
        try: 
            X = float(x)
            return X
        except ValueError:
            X = 0.
            return X


def parse_CommentedStations(lines : list[str]) -> list[StationWithComment]:
    parsed_lines = [[elem for elem in line.split(";") if elem != ""] for line in lines[1:]]
    stations_list = []
    for line in parsed_lines: 
        if len(line) > 1:
            stn_name = [elem for elem in line[0].split(" ") if elem != ""][0]
            comment = line[1]
            station = StationWithComment(stn_name,comment)
            stations_list.append(station)
    return stations_list

def parse_LRUDS(lines: list[str], format : str) -> list[LineLRUD]:
    if format == "tro":
        LRUDlines = [[elem for elem in line.split(" ") if elem != ""] for line in lines[:]]
    elif format == "trox":
        print("parsing a trox file")
        LRUDlines = []
        LRUDlines.append([elem.split("=")[-1].strip('"') for elem in lines[0].split(" ")[1:] if elem != ""])
        LRUDlines = LRUDlines + [["*"]+[elem.split("=")[-1].strip('"') for elem in line.split(" ")[1:] if elem != ""] for line in lines[:]]
    else:
        LRUDlines = [[]]
    lrud_lines = []


    for c,line in enumerate(LRUDlines):
        if "*" in line[0] and len(line) >=9:
            LRUDline =LineLRUD(LRUDlines[c][1],parseFloat(line[5]),parseFloat(line[6]),parseFloat(line[7]),parseFloat(line[8])) 
        elif len(line) >=9:
            LRUDline =LineLRUD(line[1],parseFloat(line[5]),parseFloat(line[6]),parseFloat(line[7]),parseFloat(line[8]))
        else:
            print("skipping empty line {}".format(c))
        if len(line) >=9:
            if line[0] != line[1]:
            #check there is no asterisk 
                lrud_lines.append(LRUDline) # type:ignore

    return lrud_lines

def parse_normal_data(lines: list[str], format: str ) -> list[NormalDataLine]:

    if format == "tro":
        datalines = [[elem for elem in line.split(" ") if elem != ""] for line in lines[1:]]
    elif format == "trox":
        print("parsing a trox file")
        datalines: list = []
        datalines.append([elem.split("=")[-1].strip('"') for elem in lines[0].split(" ")[1:] if elem != ""])

        for line in lines[1:]:
            if "Dep=" in line: 
                datalines.append([elem.split("=")[-1].strip('"') for elem in line.split(" ")[1:] if elem != ""])
            else: 
                datalines.append(["*"]+[elem.split("=")[-1].strip('"') for elem in line.split(" ")[1:] if elem != ""])
    else:
        datalines = [[]]
    
    dataLines = []

    for c,line in enumerate(datalines):
        if "*" in line[0] and len(line) >=9:
            dataLine = NormalDataLine(datalines[c-1][1],line[1],float(line[2]),float(line[3]),float(line[4]))
            print(line)
        elif len(line) >=9:
            dataLine = NormalDataLine(line[0],line[1],float(line[2]),float(line[3]),float(line[4]))
        else:
            print("skipping empty line {}".format(c))
        if dataLine.tape != 0:  # type:ignore
            dataLines.append(dataLine) # type:ignore

    return dataLines

def parse_diving_data(lines: list[str], format: str) -> list[DivingDataLine]:

    if format == "tro":
        datalines = [[elem for elem in line.split(" ") if elem != ""] for line in lines[1:]]
    elif format == "trox":
        print("parsing a trox file")
        datalines = []
        datalines.append([elem.split("=")[-1].strip('"') for elem in lines[0].split(" ")[1:] if elem != ""])
        datalines = datalines + [["*"]+[elem.split("=")[-1].strip('"') for elem in line.split(" ")[1:] if elem != ""] for line in lines[1:]]
    else:
        print("oops empty")
        datalines = [[]]


    dataLines = []

    for c,line in enumerate(datalines[:]): # keep and index and ignore the first one.
        if len(line) >=9:
            if "*" in line and len(datalines[c-1]) > 9:
                dataLine = DivingDataLine(from_depth= float(datalines[c][4]),
                from_station= datalines[c-1][1],
                to_depth= float(line[4]),
                to_station=line[1],
                tape= float(line[2]),
                compass =float(line[3]))
            else:
                dataLine = DivingDataLine(from_depth= float(datalines[c][4]),
                from_station= line[0],
                to_depth= float(line[4]),
                to_station=line[1],
                tape= float(line[2]),
                compass =float(line[3]))
        
            if dataLine.tape != 0:
                dataLines.append(dataLine)

    return dataLines

def make_centrelines_list(data : list[str], format: str ) -> list[Centreline]:
    
    surveyor_groups,survey_dates,starts,ends = return_centreline_params(data, fmt= format) # type:ignore

    centrelines : list[Centreline] = []

    for start,end,date in zip(starts,ends,survey_dates):
        newCentreline = Centreline()
        newCentreline.add_Date(date)
        if format == "tro":
            header = data[start-1]
        else:
            if "Comment" in data[start-1]:
                header = ""
                for elem in data[start-2].split(" ")[1:]:
                    header += elem.split("=")[-1].strip('"')+" "
            else:
                header = ""
                for elem in data[start-1].split(" ")[1:]:
                    header += elem.split("=")[-1].strip('"')+" "

        print("data header:    ", newCentreline.data_header)
        strategy = StrategyParser(header)

        newCentreline.update_type(strategy.strategy_name)
        station_lines = parse_CommentedStations(data[start:end])

        if "normal" in strategy.strategy_name:
            lrudLines = parse_LRUDS(data[start:end], format = format)
            dataLines = parse_normal_data(data[start:end], format= format)

            for dataLine,lrudLine in zip(dataLines,lrudLines):
                newCentreline.add_dataline(dataLine)
                newCentreline.add_LRUDdataline(lrudLine)
            

        elif "diving" in strategy.strategy_name:
            lrudLines = parse_LRUDS(data[start:end], format = format)
            dataLines = parse_diving_data(data[start:end], format = format)

            for dataLine,lrudLine in zip(dataLines,lrudLines):
                newCentreline.add_dataline(dataLine)
                newCentreline.add_LRUDdataline(lrudLine)

        for line in station_lines:
            newCentreline.add_station_line(line)

        newCentreline.add_string_repr()
        centrelines.append(newCentreline)

    return centrelines


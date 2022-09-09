import os
from os.path import isfile, join, dirname, abspath
import sys
import re
import argparse
import shutil
import subprocess
import tempfile

from helpers.survey import Survey, SurveyLoader, NoSurveysFoundException
from helpers.therion import compile_template

# Parse arguments

parser = argparse.ArgumentParser(description="Create a skeleton scrap")

parser.add_argument(
    "survey_file",
    help='The survey file (*.tro) to work from. e.g. "data/107/BahiaBlanca/BahiaBlanca.tro"',
)

parser.add_argument(
    "cave_name",
    help='The name of the cave or survey',
)

args = parser.parse_args()

# create the therion file template
THtemplate = """
survey {surveyName} -title {surveyName} -entrance {entranceStation}
{Centrelines}
endsurvey
"""

# create the centreline template
centreline_template = """
centreline
{surveyDate}
{surveyTeams}
\tunits length meters
\tunits compass clino degrees
{dataheader}
{data}
\tdata dimensions station left right up down
{lrud}
endcentreline"""

# data header lines
dive_topo = "\tdata diving to todepth from fromdepth tape compass"
normal_topo = "\tdata normal from to tape compass clino"

def writeDate(explodate):
    try:
        month = explodate[3:5]
        year = explodate[-2:]
        if int(year) < 50:
            year4digits = '20'+ year

        day = explodate[:2]

        date =  'date {}.{}.{}\n'.format(year4digits,month,day)

    except:
        date = ''

    return date

def writeSurveyors(surveyors):
    lines = ""
    for surveyor in surveyors:
        if surveyor != 'et':
            lines+= '\t team "{}"\n'.format(surveyor)

    return lines

def getData(data,s,e):
    style = data[s-1] # either 'normal' or 'diving' maybe with inversions
    stn1 = []
    stn2 = []
    fromdepth = []
    todepth = []
    tape = []
    compass = []
    clino = []
    left = []
    right = []
    up = []
    down = []
    print("this is the style in use: {}".format(style))
    for c,l in enumerate(data[s+1:e]):
        # check the station 1 name.

        data_line = l.split(' ')
        data_line[:] = [x for x in data_line if x]

        if len(data_line) > 9:
            if data_line[0] =='*':
                previous = data[s+c].split(' ')
                previous[:] = [x for x in previous if x]

                previous_stn = previous[1]

                data_line[0] = previous_stn

            if 'Prof' not in style:
                for key,val in enumerate((stn1,stn2,tape,compass,clino,left, right, up, down)):
                    val.append(data_line[key])

            else:
                print('found diving data')
                previous = data[s+c].split(' ')
                previous[:] = [x for x in previous if x]
                if len(previous) >5:

                    previous_depth = previous[4]

                    data_line[9] = previous_depth
                    for key,val in enumerate((stn1,stn2,tape,compass,todepth,left, right, up, down,fromdepth)):
                        val.append(data_line[key])
                elif data_line[0] != data_line[1]:
                    data_line[9] = 'not known'
                    for key,val in enumerate((stn1,stn2,tape,compass,todepth,left, right, up, down,fromdepth)):
                        val.append(data_line[key])

    if 'Prof' not in style:
        if 'Inv' in style: ## check out where inverted readings occur.
            print("This is a style with inversions!")
            STYLE = {reading:style for reading,style in zip(style.split(" ")[1:4],style.split(" ")[6].split(','))}
            print(STYLE)

            if (STYLE['Deca'] == 'Inv') & ((STYLE['Degd'] == 'Inv') & (STYLE['Clino'] == 'Inv')):
                print("all inverted")
                formatted_data =  (stn2,stn1,tape,[(float(c)+180)%360 for c in compass],[-float(c) for c in clino],left,right,up,down)
            elif (STYLE['Degd'] == 'Inv') & (STYLE['Clino'] == 'Inv'):
                print("both inverted!")
                print(compass)
                print([(float(c)+180)%360 for c in compass])
                formatted_data =  (stn1,stn2,tape,[(float(c)+180)%360 for c in compass],[-float(c) for c in clino],left,right,up,down)
            elif (STYLE['Deca'] == 'Inv') & (STYLE['Degd'] == 'Inv'):
                print("Deca inverted and direction too")
                formatted_data =  (stn2,stn1,tape,compass,clino,left,right,up,down)

            elif (STYLE['Degd'] == 'Inv'):
                formatted_data =  (stn1,stn2,tape,[(float(c)+180)%360 for c in compass],clino,left,right,up,down)
            elif (STYLE['Clino'] == 'Inv'):
                formatted_data =  (stn1,stn2,tape,compass,[-float(c) for c in clino],left,right,up,down)
            elif (STYLE['Deca']== 'Inv'):
                formatted_data =  (stn2,stn1,tape,compass,clino,left,right,up,down)
            else:
                print('this possibly an unknown style')
        else:
            formatted_data =  (stn1,stn2,tape,compass,clino,left,right,up,down)
    else:
        if 'Inv' in style: ## check out where inverted readings occur.
            print("This is a style with inversions!")
            STYLE = {reading:style for reading,style in zip(style.split(" ")[1:4],style.split(" ")[5].split(','))}
            print(STYLE)
            if (STYLE['Deca'] == 'Inv') &  (STYLE['Prof'] == 'Inv'):
                print("all inverted")
                formatted_data =  (stn1,todepth,stn2,fromdepth,tape,compass,left, right, up, down)
        else:
            formatted_data = (stn2,todepth,stn1,fromdepth,tape,compass,left, right, up, down)
    return formatted_data

def FindEntrancestn(data):
    for c,l in enumerate(data):
        if 'Entree' in l:
            entrance_stations = re.findall(r"(?<=Entree\s).+",l)
    return entrance_stations

def returnCentrelineparams(data):
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

def cleanNames(string):

    string = string.encode('utf-8').replace(b'o\xcc\x82',b'o').decode('utf-8')
    string = string.encode('utf-8').replace(b'e\xc3\xa9',b'e').decode('utf-8')
    string = string.encode('utf-8').replace(b'e\xc3\xa8',b'e').decode('utf-8')
    string = string.encode('utf-8').replace(b'\xc3\x81',b'').decode('utf-8')
    string = string.encode('utf-8').replace(b'\xcc\x81',b'').decode('utf-8')
    string  = string.encode('utf-8').replace(b'\xc3\xaf',b'i').decode('utf-8')
    string.replace('\s','_')
    return string

def writeCentreline(data,start,end,surveyor_group,survey_date):
    shot = "{stn1}\t{stn2}\t{tape}\t{compass}\t{clino}\n\t\t"
    dive_shot = "{stn2}\t{todepth}\t{stn1}\t{fromdepth}\t{tape}\t{compass}\n\t\t"
    station_dims = "{stn}\t{left}\t{right}\t{up}\t{down}\n\t\t"
    data_lines = ""
    lrud_lines = ""

    if 'Prof' not in data[start-1]:
        datastyle = 'normal'
        stn1,stn2,tape,compass,clino,left,right,up,down = getData(data,start,end)


        header = normal_topo
        print(len(stn1))
        print("this is the header I'm using: {}".format(normal_topo))

        for c in range(len(stn1)):
            if stn1[c]!=stn2[c]:

                # format the dataline string
                data_line = shot.format(stn1=stn1[c],
                        stn2=stn2[c],
                        tape=tape[c],
                        compass=compass[c],
                        clino=clino[c])
                data_lines+= '\t'+data_line

            # format the left right up down string
            lrud_line =  station_dims.format(stn=stn2[c],
                            left=left[c],
                            right=right[c],
                            up=up[c],
                            down=down[c])

            lrud_lines+= '\t'+re.sub(r"\*","-",lrud_line)

    # if not normal data, write up the diving style data
    elif 'Param Deca Degd Prof' in data[start-1]:
        print('found diving data')
        datastyle = 'diving'
        header = dive_topo
        print(header)

        # collect data
        stn2,todepth,stn1,fromdepth,tape,compass,left,right,up,down = getData(data,start,end)

        # format the dive shots
        for c in range(len(stn1)):
            data_line = dive_shot.format(stn2=stn2[c],
                                todepth=todepth[c],
                                stn1=stn1[c],
                                fromdepth=fromdepth[c],
                                tape=tape[c],
                                compass=compass[c])

            if 'not known' in data_line:
                data_lines+= '#\t'+data_line
            else:
                data_lines+= '\t'+data_line

            # format the left right up down datashots
            lrud_line =  station_dims.format(stn=stn2[c],
                            left=left[c],
                            right=right[c],
                            up=up[c],
                            down=down[c])

            # append to the list of lrud lines
            lrud_lines+= '\t'+re.sub(r"\*","-",lrud_line)
    else:
        header = normal_topo

    surveyDate = writeDate(survey_date)
    surveyTeams = writeSurveyors(surveyor_group)

    # format the centreline template
    CENTRELINE = centreline_template.format(surveyTeams = surveyTeams,
                                      surveyDate = surveyDate ,
                                      data = data_lines,
                                      lrud=lrud_lines,
                                     dataheader=header)

    return CENTRELINE

def writeTemplate(filepath, new_filepath,cave_name):

    with open (filepath,'r', encoding='latin-1') as f1:
        data = f1.readlines()
        f1.close()

    surveyor_groups,survey_dates,starts,ends = returnCentrelineparams(data)

    centrelines = ""

    entrance = FindEntrancestn(data)
    for start,end,surveyor_group,survey_date in zip(starts,ends,surveyor_groups,survey_dates):

        centrelines+= "\n"+writeCentreline(data,start,end,surveyor_group,survey_date)

    # format the template file
    TEMPLATE = THtemplate.format(surveyName=cave_name,
                               Centrelines =centrelines,
                               entranceStation =entrance[0])

    print("filepath: {}".format(new_filepath))
    with open(new_filepath,'w+',encoding='utf-8') as f:
        f.write(TEMPLATE)
        f.close()

ENTRY_FILE = abspath(args.survey_file)
EXIT_FILE = "{}_convert.th".format(abspath(ENTRY_FILE)[:-4])
CAVE_NAME = args.cave_name

print(abspath(ENTRY_FILE),CAVE_NAME)
writeTemplate(abspath(ENTRY_FILE),EXIT_FILE,CAVE_NAME)

print(EXIT_FILE)


#subprocess.run(['python3',abspath('scripts/create_2d.py'),'raw convert/4_plus_1_convert.th',CAVE_NAME,'--projection', 'plan'])

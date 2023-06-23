
import argparse
from os.path import abspath, dirname

# the behaviour of the class is sort of tested
from helpers.therion_classes import * 



parser = argparse.ArgumentParser(description="Create a skeleton scrap")

parser.add_argument(
    "survey_file",
    help='The survey file (*.tro) to work from. e.g. "data/107/BahiaBlanca/BahiaBlanca.tro"',
)

parser.add_argument(
    "cave_name",
    help='The name of the cave or survey',
)

parser.add_argument(
    "format",
    help='the format of the Visual Topo File',
)

args = parser.parse_args()

ENTRY_FILE = abspath(args.survey_file)
FORMAT = args.format
CAVE_NAME = args.cave_name
EXIT_FILE = f"{dirname(ENTRY_FILE)}/{CAVE_NAME}.th"

with open (ENTRY_FILE,'r', encoding='latin-1') as f:
        data = f.readlines()

# create a named survey
newSurvey = Survey(name=CAVE_NAME)

# add the entrance
newSurvey.add_entrance(find_entrance_stn(data, FORMAT))

# read the data to centrelines and add to survey
centrelines = make_centrelines_list(data, format= FORMAT)
newSurvey.add_centrelines(centrelines)

# make a formatted string
newSurvey.add_string_repr()
print(newSurvey._string_repr)

with open(EXIT_FILE, 'w+') as f:
    f.write(newSurvey._string_repr)
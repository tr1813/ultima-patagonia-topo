
import argparse
from os.path import abspath, dirname

# the behaviour of the class is sort of tested
from helpers.therion_classes import * 

with open ("test/test1.trox",'r', encoding='latin-1') as f:
        data = f.readlines()

# create a named survey
newSurvey = Survey(name="GrotteDeLAncien")

newSurvey.add_entrance(find_entrance_stn(data, "trox"))

centrelines = make_centrelines_list(data, format= "trox")

newSurvey.add_centrelines(centrelines)

# make a formatted string
newSurvey.add_string_repr()

print(newSurvey.centrelines[0].data_header)
print(newSurvey._string_repr)

with open("test_1.th", 'w+') as f:
    f.write(newSurvey._string_repr)


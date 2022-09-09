import os
from os.path import isfile, join, dirname, abspath
import sys
import re
import argparse
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser(description="Create a skeleton scrap")

parser.add_argument(
    "survey_file",
    help='The survey file (*.th) to work from. e.g. "data/107/BahiaBlanca/BahiaBlanca.th"',
)

parser.add_argument(
    "xoffset",
    help='some x offset for the entrance station',
)

parser.add_argument(
    "yoffset",
    help='some y offset for the entrance station',
)


args = parser.parse_args()

ENTRY_FILE = abspath(args.survey_file)
XOFFSET = float(args.xoffset)
YOFFSET = float(args.yoffset)
CAVE_NAME = ENTRY_FILE.split('.')[0]
template = '''
source {survey}

input layouts/metapost/scalebar_arrow.thl

layout local
  copy custom_scalebar
  scale 1 500
  #grid top
  #grid-size 20 20 10 m
  symbol-colour point station-name [20 20 80]
  colour map-fg [90 90 90]
  map-header 0 100 sw
  origin {x} {y} {z} m
  overlap 0.2 cm
endlayout

cs UTM18S
export atlas -o {cavename}-trace-topo-p.pdf -layout local -layout-debug station-names -projection plan
export atlas -o {cavename}-trace-topo-e.pdf -layout local -layout-debug station-names -projection extended
'''

SECTOR = ENTRY_FILE.split('/')[-3]


INDEX_FILE = abspath('data/'+SECTOR+'/'+SECTOR+".th")


with open(ENTRY_FILE, "r", encoding = 'utf-8') as f:
    HEADER = f.readlines()[:2]
    f.close()

for line in HEADER:
    if '-attr cad_num' in line:
        CAD_NUM = int(line.split('-attr cad_num')[1].split('-attr')[0])
        print(CAD_NUM)
with open(INDEX_FILE, "r", encoding = 'utf-8') as f:
    FIXES = f.readlines()
    f.close()

for line in FIXES:
    if 'fix' in line:
        if str(CAD_NUM) in line:
            print(line)
            try:
                line_no_space = [x for x in line.split(' ') if x]
                print(line_no_space)
                X,Y,Z = line_no_space[2:5]
                X = float(X)
                Y = float(Y)
                Y = float(Z)
            except ValueError:
                try:
                    X,Y,Z = line.split('\t')[1:4]
                    X = X.split(' ')[0]
                    Y = Y.split(' ')[0]
                    Z =Z.split(' ')[0]
                except ValueError:
                    print("there's something wrong with the fix line")

            print(X,Y,Z)

TEMPLATE = template.format(survey = ENTRY_FILE,
x = float(X)-XOFFSET,y = float(Y)-YOFFSET,z = float(Z)+10 ,cavename = CAVE_NAME)

with open("temp.th",'w+',encoding='utf-8') as f:
    f.write(TEMPLATE)
    f.close()

print(TEMPLATE)

subprocess.check_output("therion temp.th", shell = True)

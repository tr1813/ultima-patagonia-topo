#!/bin/bash

therion index.thconfig;
rm "../outputs/resume_explorations.csv";
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/resume_explorations.csv
.mode csv
SELECT c.EXPLO_DATE,s.FULL_NAME,c.LENGTH, c.DUPLICATE_LENGTH,p.SURNAME,c.TOPO_DATE, GROUP_CONCAT(p2.SURNAME, ";") as SURVEYORS
FROM SURVEY as s, CENTRELINE as c, PERSON as p, EXPLO as e, TOPO as t, PERSON as p2 
WHERE c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND e.PERSON_ID == p.ID AND e.CENTRELINE_ID == c.ID and t.PERSON_ID == p2.ID AND t.CENTRELINE_ID == c.ID 
GROUP BY  c.ID
ORDER BY c.EXPLO_DATE;
.quit
EOF

rm "../outputs/resume_explorations_106.csv";
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/resume_explorations_106.csv
.mode csv
SELECT c.EXPLO_DATE,s.FULL_NAME,c.LENGTH, c.DUPLICATE_LENGTH,p.SURNAME,c.TOPO_DATE, GROUP_CONCAT(p2.SURNAME, ";") as SURVEYORS
FROM SURVEY as s, CENTRELINE as c, PERSON as p, EXPLO as e, TOPO as t, PERSON as p2 
WHERE c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND e.PERSON_ID == p.ID AND e.CENTRELINE_ID == c.ID and t.PERSON_ID == p2.ID AND t.CENTRELINE_ID == c.ID  AND s.FULL_NAME LIKE "%106%"
GROUP BY  c.ID
ORDER BY c.EXPLO_DATE;
.quit
EOF

rm "../outputs/resume_explorations_107.csv";
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/resume_explorations_107.csv
.mode csv
SELECT c.EXPLO_DATE,s.FULL_NAME,c.LENGTH, c.DUPLICATE_LENGTH,p.SURNAME,c.TOPO_DATE, GROUP_CONCAT(p2.SURNAME, ";") as SURVEYORS
FROM SURVEY as s, CENTRELINE as c, PERSON as p, EXPLO as e, TOPO as t, PERSON as p2 
WHERE c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND e.PERSON_ID == p.ID AND e.CENTRELINE_ID == c.ID and t.PERSON_ID == p2.ID AND t.CENTRELINE_ID == c.ID  AND s.FULL_NAME LIKE "%107%"
GROUP BY  c.ID
ORDER BY c.EXPLO_DATE;
.quit
EOF

rm "../outputs/resume_explorations_glaciers.csv";
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/resume_explorations_glaciers.csv
.mode csv
SELECT c.EXPLO_DATE,s.FULL_NAME,c.LENGTH, c.DUPLICATE_LENGTH,p.SURNAME,c.TOPO_DATE, GROUP_CONCAT(p2.SURNAME, ";") as SURVEYORS
FROM SURVEY as s, CENTRELINE as c, PERSON as p, EXPLO as e, TOPO as t, PERSON as p2 
WHERE c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND e.PERSON_ID == p.ID AND e.CENTRELINE_ID == c.ID and t.PERSON_ID == p2.ID AND t.CENTRELINE_ID = c.ID  AND (s.FULL_NAME LIKE "403%" or s.FULL_NAME LIKE "%402%")
GROUP BY  c.ID
ORDER BY c.EXPLO_DATE;
.quit
EOF

rm "../outputs/resume_explorations_Pirates.csv";
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/resume_explorations_Pirates.csv
.mode csv
SELECT stn1.NAME, stn2.NAME, sh.ADJ_LENGTH, sh.ADJ_BEARING, sh.ADJ_GRADIENT, c.EXPLO_DATE,s.FULL_NAME
FROM SURVEY as s, CENTRELINE as c, SHOT as sh, STATION as stn1, STATION as stn2
WHERE sh.CENTRELINE_ID ==c.ID AND c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND s.FULL_NAME LIKE "%CuevaPirates.106%" AND sh.TO_ID == stn2.ID AND sh.FROM_ID = stn1.ID AND stn2.NAME != "-" AND stn2.NAME != "."
ORDER BY c.EXPLO_DATE;
.quit
EOF

rm ../outputs/allShots.csv
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/allShots.csv
.mode csv
SELECT stn1.NAME,stn1.Z, stn2.NAME, stn2.Z, sh.ADJ_LENGTH, sh.ADJ_BEARING, sh.ADJ_GRADIENT, c.EXPLO_DATE,s.FULL_NAME
FROM SURVEY as s, CENTRELINE as c, SHOT as sh, STATION as stn1, STATION as stn2
WHERE sh.CENTRELINE_ID ==c.ID AND c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND sh.TO_ID == stn2.ID AND sh.FROM_ID = stn1.ID AND stn2.NAME != "-" AND stn2.NAME != "."
ORDER BY c.EXPLO_DATE;
.quit
EOF

sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.headers on
.output ../outputs/longestCaves.csv
.mode csv
SELECT MIN(stn.Z),MAX(stn.Z),c.LENGTH, c.EXPLO_DATE,s.FULL_NAME
FROM SURVEY as s, CENTRELINE as c, STATION as stn
WHERE c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND stn.SURVEY_ID = s.ID
GROUP BY s.FULL_NAME
ORDER BY c.EXPLO_DATE;
.quit
EOF
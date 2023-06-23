#!/bin/bash

therion index.thconfig;
rm "../outputs/resume_explorations.csv";
sqlite3 <<EOF 
.read ../outputs/ultima-patagonia.sql
.output ../outputs/resume_explorations.csv
.mode csv
SELECT c.EXPLO_DATE,s.FULL_NAME,c.LENGTH, c.DUPLICATE_LENGTH,p.SURNAME, GROUP_CONCAT(p2.SURNAME, ";") as SURVEYORS
FROM SURVEY as s, CENTRELINE as c, PERSON as p, EXPLO as e, TOPO as t, PERSON as p2 
WHERE c.LENGTH > 0 AND c.SURVEY_ID == s.ID AND e.PERSON_ID == p.ID AND e.CENTRELINE_ID == c.ID and t.PERSON_ID == p2.ID AND t.CENTRELINE_ID = c.ID 
GROUP BY  c.ID
ORDER BY c.EXPLO_DATE;
.quit
EOF
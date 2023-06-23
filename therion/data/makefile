#!/bin/bash
sql : 
	therion index.thconfig;
	rm "../outputs/resume_explorations.csv";
	sqlite3 ".read ../outputs/ultima-patagonia.sql";
	sqlite3 ".output ../outputs/resume_explorations.csv";
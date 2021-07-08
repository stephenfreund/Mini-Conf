# make all - -makes eveyrhing
#
# New directions
#  * Download (full events) reasearchr.ics and researchr.json and 
#         save in current directory
#  * make calendars  -- generates track calendars as csv's in auto
#  * make sessions  -- generates track_colocated.csv in auto.  Has all workshop sessions in it.
#  * copy from auto into ../sitedata to use on the site.
# To deploy:
#  * Just copying changes local version 
#  * `make deploy-staging`  changes staging.pldi21.org
#  * `make deploy` changes www.pldi21.org.  
#
# Handling new tracks:
#  * copy/paste in Makefile below.
#  * add map from ROOM name to track uid in ./researchr_parse_colocated_events_from_ics.py.
#    (see sitedata/tracks.csv for the names you need...)
#
#
# What's left? MAPS

#
# OLD NOTES FOR STEVE:
#
#   * Download full JSON and ICS data from Researchr.  Stored as researchr.json and researchr.ics.
#   * make sessions -- generates csv file in auto.  Move this to ../sitedata if it looks ok.  This
#       is used for home page and schedule page.
#   * make slideslive -- human readable versions Steve will provide to SlidesLive producer
#
#   * Note: sessions may be bigger than what workshops actually schedule.  I think this is handled
#       in the script for sessions now.
#
#   TODO: researchr_parse_colocated_events_from_ics and slideslive version: Needs to handle the rooms
#       for the other workshops. HOPL, Infer, LCTES, ISMM, ...
#
#   TODO: autmoate getting of ical file once Elmer gives us a URL.
#
sessions:
	python3 ./researchr_parse_colocated_sessions_from_json.py --ics researchr.ics  --json researchr.json --out auto/track_colocated.csv

#
# calendars and slideslive
#
#   * Download full JSON and ICS data from Researchr.  Stored as researchr.json and researchr.ics.
#   * make calendars -- generates csv files in auto.  Move these to ../sitedata if they look ok.
#
# DO NOT MAKE TUTORIALS WITH THESE
# 
calendars:
	mkdir -p auto
	python3 ./researchr_parse_colocated_events_from_ics.py --room "PLMW" --ics researchr.ics --json researchr.json --out auto/track_plmw.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "ARRAY" --ics researchr.ics --json researchr.json --out auto/track_array.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "SOAP" --ics researchr.ics --json researchr.json --out auto/track_soap.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "LCTES" --ics researchr.ics --json researchr.json --out auto/track_lctes.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "HOPL" --ics researchr.ics --json researchr.json --out auto/track_hopl.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "ISMM" --ics researchr.ics --json researchr.json --out auto/track_ismm.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "PLanQC" --ics researchr.ics --json researchr.json --out auto/track_planqc.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "Infer Practitioners" --ics researchr.ics --json researchr.json --out auto/track_infer.csv
	python3 ./researchr_parse_colocated_events_from_ics.py --room "MAPS" --ics researchr.ics --json researchr.json --out auto/track_maps.csv

slideslive:
	mkdir -p slideslive_auto
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "Tutorials" --ics researchr.ics --json researchr.json --out slideslive_auto/track_tutorials.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "PLMW" --ics researchr.ics --json researchr.json --out slideslive_auto/track_plmw.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "ARRAY" --ics researchr.ics --json researchr.json --out slideslive_auto/track_array.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "SOAP" --ics researchr.ics --json researchr.json --out slideslive_auto/track_soap.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "LCTES" --ics researchr.ics --json researchr.json --out slideslive_auto/track_lctes.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "HOPL" --ics researchr.ics --json researchr.json --out slideslive_auto/track_hopl.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "ISMM" --ics researchr.ics --json researchr.json --out slideslive_auto/track_ismm.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "PLanQC" --ics researchr.ics --json researchr.json --out slideslive_auto/track_planqc.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "Infer Practitioners" --ics researchr.ics --json researchr.json --out slideslive_auto/track_infer.csv
	python3 ./researchr_parse_colocated_events_from_ics_for_slideslive.py --room "MAPS" --ics researchr.ics --json researchr.json --out slideslive_auto/track_maps.csv

diffs:
	echo "auto/track_colocated.csv"
	diff ../sitedata/track_colocated.csv auto/track_colocated.csv; exit 0
	echo ""
	@for track in array plmw soap lctes hopl ismm planqc infer maps ; do \
		echo ; \
		echo $$track... ; \
		diff  ../sitedata/track_$$track.csv auto/track_$$track.csv ; \
		echo ; \
	done

	@for track in array plmw soap lctes hopl ismm planqc infer maps ; do \
		echo ; \
		echo $$track... ; \
		diff  slideslive_orig/track_$$track.csv slideslive_auto/track_$$track.csv ; \
		echo ; \
	done


#
# Download SlidesLive Sheet
#
talks:
	curl https://docs.google.com/spreadsheets/d/aaaaaaaaaaaa/gviz/tq?tqx=out:csv > auto/prerecorded_slideslive.csv

#
# Download Researchr session data.
#
researchr:
	@echo "Downloading researchr files into ."
	@curl https://pldi21.sigplan.org/dataexport/6e281914-95db-4521-8793-2408625936e4/confero.json/false > researchr.json
	@curl https://pldi21.sigplan.org/downloadICal/full-program/event-calendar.ics > researchr.ics


all: talks researchr sessions calendars slideslive diffs


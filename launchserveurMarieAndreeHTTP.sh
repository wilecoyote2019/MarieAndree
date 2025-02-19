#!/bin/bash
#
#Script qui lance l'interface python 
#V3.0
#16/02/2025
#

. /home/oam/.venv/bin/activate 
streamlit run --browser.gatherUsageStats "False" /home/oam/MarieAndree_v3/serveurMarieAndreeHTTP.py




#2> /home/oam/HTTPServerMarieAndre.log


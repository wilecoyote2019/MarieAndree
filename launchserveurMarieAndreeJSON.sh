#!/bin/bash
#
#Script qui lance le backend 
#V3.0
#16/02/2025
#
. /home/oam/.newvenv/bin/activate
export OPENAI_API_KEY={OPENAI_API_KEY}
python3 /home/oam/MarieAndree_v3/serveurMarieAndreeJSON.py



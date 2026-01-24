#!/bin/bash

# Setup simples da API ONS

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ons_api.py

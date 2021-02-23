#!/bin/bash
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd frontend
npm install
cd ..
echo "Setup finished"
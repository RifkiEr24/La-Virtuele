#!/bin/bash
pip install virtualenv
virtualenv backend/env
source backend/env/bin/activate
pip install -r backend/requirements.txt
cd frontend
npm install
cd ..
echo "Setup finished"
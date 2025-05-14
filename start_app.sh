#!/bin/bash

python3 src/backend/update_db.py &
python3 src/backend/app.py

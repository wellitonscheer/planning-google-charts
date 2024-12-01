#!/bin/bash

current_path=$(pwd)

python_file="$current_path/extract_data.py"

python "$python_file"

python -m webbrowser "http://localhost:50000"

python -m http.server 50000
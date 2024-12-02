@echo off

REM Get the current path the script is running in
set current_path=%cd%

REM Concatenate to form an absolute path to the Python file
set python_file=%current_path%\extract_data.py

REM Execute the Python file
python "%python_file%"

REM Open the created link in the default browser
start http://localhost:50000

REM Start the HTTP server on port 50000
start python -m http.server 50000

REM Keep the terminal window open
pause
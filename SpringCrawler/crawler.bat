@echo off
setlocal ENABLEDELAYEXPANSION

if \"%~1\"==\"\" (
    echo Usage: crawler.bat ^<seed-file^> ^<num-pages^> ^<depth>^ ^<output_dir>^
    exit /b 1
)
if \"%~2\"==\"\" (
    echo Usage: crawler.bat ^<seed-file^> ^<num-pages^> ^<depth>^ ^<output_dir>^
    exit /b 1
)

set SEED_FILE=%~1
set NUM_PAGES=%~2

if not exist venv (
    python -m venv venv
)

call venv\\Scripts\\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

scrapy crawl url -a seed_file=%SEED_FILE% -a num_pages=%NUM_PAGES%
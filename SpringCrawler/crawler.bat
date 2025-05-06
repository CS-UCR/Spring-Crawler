@echo off
setlocal ENABLEDELAYEDEXPANSION

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
set DEPTH=%~3
set OUTPUT_DIR=%~4

if not exist venv (
    python -m venv venv
)

call venv\\Scripts\\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

set SCRAPY_CMND=scrapy crawl url -a seed_file=%SEED_FILE% -a num_pages=%NUM_PAGES%

if not "%DEPTH%"=="" (
    set SCRAPY_CMND=!SCRAPY_CMND! -a max_depth=%DEPTH%
)

if not "%OUTPUT_DIR%"=="" (
    set SCRAPY_CMND=!SCRAPY_CMND! -a output_dir=%OUTPUT_DIR%
)

cmd /c %SCRAPY_CMND% 
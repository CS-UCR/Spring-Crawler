#!/bin/bash
set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./crawler.sh <seed-file> <num-pages> <depth> <output-dir>"
    exit 1
fi

SEED_FILE=$1
NUM_PAGES=$2

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

scrapy crawl url -a seed_file=$SEED_FILE -a num_pages=$NUM_PAGES
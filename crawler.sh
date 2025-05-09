#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./crawler.sh <seed-file> <num-pages> <depth> <output-dir>"
    echo "The seed-file and num-pages must be specified."
    exit 1
fi

SEED_FILE=$1
NUM_PAGES=$2
DEPTH=$3
OUTPUT_DIR=$4

pip install --upgrade pip
pip install -r ../requirements.txt

SCRAPY_CMND="scrapy crawl url -a seed_file=$SEED_FILE -a num_pages=$NUM_PAGES"

if [ -n "$DEPTH" ]; then
  SCRAPY_CMND="$SCRAPY_CMND -a max_depth=$DEPTH"
fi

if [ -n "$OUTPUT_DIR" ]; then
  SCRAPY_CMND="$SCRAPY_CMND -a output_dir=$OUTPUT_DIR"
fi

eval "$SCRAPY_CMND"
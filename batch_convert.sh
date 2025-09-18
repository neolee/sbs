#!/bin/bash

# Sample: ./batch_convert.sh local/notebooks local/output

if [ $# -ne 2 ]; then
    echo "Usage: ./batch_convert.sh <input_dir> <output_dir>"
    exit 1
fi

input_dir=$1
output_dir=$2

for file in "$input_dir"/*.ipynb; do
    if [ -f "$file" ]; then
        base=$(basename "$file" .ipynb)
        echo "Convert $file to $output_dir/$base.md"
        python ipynb2sbs.py "$file" "$output_dir/$base.md"
    fi
done

echo "Batch conversion completed."
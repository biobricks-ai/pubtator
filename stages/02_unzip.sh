#!/usr/bin/env bash

# Script to unzip files

# Get local path
localpath=$(pwd)
echo "Local path: $localpath"

# Set download path
export downloadpath="$localpath/download"
echo "Download path: $downloadpath"

# Set list path
listpath="$localpath/list"
echo "List path: $listpath"

# Create raw path
export rawpath="$localpath/raw"
mkdir -p $rawpath
echo "Raw path: $rawpath"

# Unzip files in parallel
cat $listpath/downloaded_files.txt | xargs -P14 -n1 bash -c '
  filename="${0%.*}"
  echo $downloadpath/$0
  echo $rawpath/$filename
  if [[ "$downloadpath/$0" == *.gz && "$downloadpath/$0" != *.tar.gz ]]; then
    gunzip -d "$downloadpath/$0" -c > "$rawpath/$filename"
  fi
'

tar -xzvf "$downloadpath/BioCXML.0.tar.gz" -C "$rawpath"

# Move BioCXML files to raw/BioCXML
mv raw/output/BioCXML raw/BioCXML
cd raw/BioCXML
for file in *; do
  num=$(echo "$file" | grep -oP '\d+')
  if [[ $num ]]; then
    newnum=$(printf "%06d" "$num")
    if [[ $newnum != $num ]]; then
      mv "$file" "${file/$num/$newnum}"
    fi
  fi
done
cd ..
rm -r output

# List unzipped files
find $rawpath -type f -name "*"  -exec basename {} \; > $listpath/raw_files.txt


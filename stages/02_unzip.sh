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
cat $listpath/files.txt | tail -n +2 | xargs -P14 -n1 bash -c '
  filename="${0%.*}"
  echo $downloadpath/$0
  echo $rawpath/$filename
  if [[ "$downloadpath/$0" == *.gz && "$downloadpath/$0" != *.tar.gz ]]; then
    gunzip -d "$downloadpath/$0" -c > "$rawpath/$filename"
  elif [[ "$downloadpath/$0" == *.tar.gz ]]; then
    tar -xzvf "$downloadpath/$0" -C "$rawpath"
  fi'

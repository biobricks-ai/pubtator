#! /usr/bin/bash

# Get local path
localpath=$(pwd)
echo "Local path: $localpath"

# Set list path
listpath="$localpath/list"
mkdir -p $listpath
echo "List path: $listpath"

# Set raw path
export rawpath="$localpath/raw"
echo "Raw path: $rawpath"
export rawpathbioc="$rawpath/BioCXML"
echo "Raw path BioC: $rawpathbioc"

# Create brick directory
export brickpath="$localpath/brick"
mkdir -p $brickpath
echo "Brick path: $brickpath"

# Create a BioC path
export brickpathbioc="$brickpath/BioC.parquet"
mkdir -p $brickpathbioc
echo "Brick path BioC: $brickpathbioc"

# Process raw files and create parquet files in parallel
# calling a Python function with arguments input and output filenames
cat $listpath/raw_files.txt | grep '\.BioC\.XML$' | xargs -P10 -n1 bash -c '
  infilename="$rawpathbioc/$0"
  filename=$(basename $0 .XML)
  outfilename="$brickpathbioc/$filename.parquet"
  echo $infilename
  python stages/build_xml.py $infilename $outfilename
'

# process the remaining files
cat $listpath/raw_files.txt | grep -v '\.BioC\.XML$' | xargs -P10 -n1 bash -c '
  infilename="$rawpath/$0"
  filename=$(basename $0)
  outfilename="$brickpath/$filename.parquet"
  echo $infilename
  python stages/build_tsv.py $infilename $outfilename
'
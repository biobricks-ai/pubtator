#! /usr/bin/bash

export localpath="$(pwd)"

export brickpath="$localpath/brick"

export downloadpath="$localpath/download"
echo "Download path: $downloadpath"


for file in "$downloadpath"/*.gz;
do
if [[ "$file" == *.gz && "$file" != *.tar.gz ]];
then
echo "$file"
outfile="$brickpath/$(basename "$file" .gz).parquet"
duckdb -c "copy (select * from read_csv('$file', delim='\t', columns = {
    'PMID': 'INT',
    'Type': 'VARCHAR',
    'Concept ID': 'VARCHAR',
    'Mentions': 'VARCHAR',
    'Resource': 'VARCHAR'
})) to '$outfile' (format 'parquet')"
fi
done
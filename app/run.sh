#!/bin/bash

# docker compose down

echo "----Container creation----"
docker compose up -d

sleep 3
echo "----Database creation----"
cd queries/
python3 db2_fast_creation.py
cd ..

echo "----Embedding vectors insertion----"
./vectors.sh

echo "----Index creation----"
cd queries/
python3 db4_index.py
cd ..

echo "----Firefox----"
# firefox http://localhost:8080/

echo "----Fin----"

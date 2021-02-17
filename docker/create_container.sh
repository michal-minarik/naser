#!/usr/bin/env bash
#build container

MAJOR=1
MINOR=1

cp ../arse.py .
cp ../config.json .
cp ../sample_input.xlsx input.xlsx

docker build -t arse:$MAJOR.$MINOR .

#!/usr/bin/env bash

cp ../arse.py .
cp ../config.json .
cp ../sample_input.xlsx input.xlsx

docker build -t arse:0.0.2 .

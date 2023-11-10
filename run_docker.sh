#!/bin/bash

# Measure 100 times for each environment
docker run --rm -v "$PWD/Py310":/home/Results ubuntu/python:3.10 python3.10 100
docker run --rm -v "$PWD/Py312":/home/Results ubuntu/python:3.12 python3.12 100
docker run --rm -v "$PWD/Cinder":/home/Results cinder/python:3.10 /cinder/bin/python3 100

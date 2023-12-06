#!/bin/bash

# Measure 100 times for each environment
docker run --rm -v "$PWD/Py310":/home/Results deb/python:3.10 python3 2 linear_regression
docker run --rm -v "$PWD/Py312":/home/Results deb/python:3.12 python3 2 linear_regression
# docker run --rm -v "$PWD/Cinder":/home/Results cinder/python:3.10 /cinder/bin/python3 10 linear_regression

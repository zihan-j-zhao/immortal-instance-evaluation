#!/bin/bash

docker run --rm -v "$PWD/Py310":/home/Results deb/python:3.10 2 grayscale_4k
docker run --rm -v "$PWD/Py312":/home/Results deb/python:3.12 2 grayscale_4k


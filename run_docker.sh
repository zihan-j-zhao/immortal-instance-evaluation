#!/bin/bash

for i in {1..2}
do
    docker run --rm -v "$PWD/Py310":/home/Results deb/python:3.10 linear_regression
    docker run --rm -v "$PWD/Py310":/home/Results deb/python:3.10 grayscale_4k
    docker run --rm -v "$PWD/Py310":/home/Results deb/python:3.10 db_operations

    docker run --rm -v "$PWD/Py312":/home/Results deb/python:3.12 linear_regression
    docker run --rm -v "$PWD/Py312":/home/Results deb/python:3.12 grayscale_4k
    docker run --rm -v "$PWD/Py312":/home/Results deb/python:3.12 db_operations
done


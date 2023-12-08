all: imgs/py310 imgs/py312

imgs/py310:
		docker build -f ./Images/Dockerfile-py310 -t deb/python:3.10 .

imgs/py312:
		docker build -f ./Images/Dockerfile-py312 -t deb/python:3.12 .

.PHONY: clean
clean:
		rm -rf ./Py310/* ./Py312/*
		rm -f ./Measure/4k_grayscale.jpg

all: imgs/cinder imgs/py310 imgs/py312

imgs/cinder:
		docker build -f ./Images/Dockerfile-cinder310 -t cinder/python:3.10 --platform=linux/arm64/v8 .

imgs/py310:
		docker build -f ./Images/Dockerfile-py310 -t ubuntu/python:3.10 .

imgs/py312:
		docker build -f ./Images/Dockerfile-py312 -t ubuntu/python:3.12 .

.PHONY: clean
clean:
		rm -rf ./Py310/* ./Py312/* ./Cinder/*

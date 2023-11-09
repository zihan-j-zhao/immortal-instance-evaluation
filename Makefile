all: imgs/cinder imgs/py310 imgs/py312

imgs/cinder:
		$(warning Not implemented)

imgs/py310:
		docker build -f ./Images/Dockerfile-py310 -t ubuntu/python:3.10 .

imgs/py312:
		docker build -f ./Images/Dockerfile-py312 -t ubuntu/python:3.12 .

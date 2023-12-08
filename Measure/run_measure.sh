#!/bin/bash

for _ in $(seq $1)
do
    python3 ./main.py $2
done



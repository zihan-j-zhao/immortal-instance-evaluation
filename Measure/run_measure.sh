#!/bin/bash

for _ in $(seq $2)
do
    $1 ./main.py $3
    $1 ./main.py $3 -f
#    $1 ./main.py $3 -c
done



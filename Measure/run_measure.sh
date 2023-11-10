#!/bin/bash

for _ in $(seq $2)
do
    $1 ./main.py reduction 0
    $1 ./main.py reduction 1
done



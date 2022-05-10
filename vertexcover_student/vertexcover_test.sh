#!/bin/sh

for i in $(seq 1 10)
do
  if [ ${#i} -eq 1 ] ; then
    i="0$i"
  fi
  python3 vertexcover_test.py "instances/i$i.txt"
done
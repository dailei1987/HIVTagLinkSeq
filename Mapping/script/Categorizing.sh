#!/bin/bash
for N in {0..12}
do 
grep "^$N\_" paired/*.pair > ../ErrorCorrection/data/$N
done

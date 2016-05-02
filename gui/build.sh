#!/bin/bash

for i in *.ui
do
	pyuic5 $i -o ${i%\.*}.py 
done
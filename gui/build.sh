#!/bin/bash

ENV=ical-dev
source $WORKON_HOME/$ENV/bin/activate

# workon ical-dev

for i in *.ui
do
	pyuic5 $i -o ${i%\.*}.py 
done
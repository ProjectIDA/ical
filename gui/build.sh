#!/bin/bash

source activate pycal

for i in *.ui
do
	pyuic5 $i -o ${i%\.*}.py_raw
    cat ../Copyright.txt gui_docstring.txt ${i%\.*}.py_raw > ${i%\.*}.py
    rm ${i%\.*}.py_raw
done
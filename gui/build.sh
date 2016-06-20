#!/bin/bash

source activate pycal

# process forms
for i in *.ui
do
	pyuic5 $i -o ${i%\.*}.py_raw
    cat ../Copyright.txt gui_docstring.txt ${i%\.*}.py_raw > ${i%\.*}.py
    rm ${i%\.*}.py_raw
done

# process resources
for i in *.qrc
do
    pyrcc5 $i -o ${i%\.*}.py_raw
    cat ../Copyright.txt gui_docstring.txt ${i%\.*}.py_raw > ${i%\.*}.py
    rm ${i%\.*}.py_raw
done
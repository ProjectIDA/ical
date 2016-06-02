#!/bin/bash

conda_env='pycal' 
app_name='PyCal'

source activate $conda_env &> /dev/null
if [ $? -ne 0 ] 
then
    echo "ERROR ACTIVATING ENVIRONMENT: ${conda_env}"
    exit 1
fi

# clean previous builds...
rm -rf build/${app_name}
rm -rf dist/${app_name}
rm -rf dist/${app_name}.app

echo "Building ${app_name}.app..."
pyinstaller PyCal.spec &> /dev/null
if [ $? -ne 0 ] 
then
    echo "ERROR BUILDING ${app_name}. Run manually to see errors."
    exit 1
else
    echo 'PyInstaller Build successful.'
fi

pushd dist > /dev/null

echo "Code signing ${app_name}.app..."
codesign --force --deep -s 'Developer ID Application: Daniel Auerbach (4GW42VMWYK)' ${app_name}.app
if [ $? -ne 0 ] 
then
    echo "ERROR CODE SIGNING ${app_name}"
    popd > /dev/null
    exit 1
else
    echo 'Code signing complete.'
fi

echo 'Checking code signing...'
echo

codesign --verify --verbose=1 ${app_name}.app
spctl -a -v PyCal.app 2>&1 | grep "${app_name}.app: accepted"
if [ $? -ne 0 ]
then
    echo 'UNSUCCESSFUL CODE SIGNING.'
else
    echo 'Code signing successful. You are clear for launch.'
fi

popd > /dev/null

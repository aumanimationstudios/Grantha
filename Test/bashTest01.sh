#!/bin/bash
path=`realpath $1`
basePath=`basename ${path}`
#if [ $# -eq 0 ]
#  then
#    echo "No arguments supplied"
#fi

#[ -z "$1" ] && echo "No argument supplied"

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi

echo ${path}
#${basePath}
python ${path}
#python ${basePath}

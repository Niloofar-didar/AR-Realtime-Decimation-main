#!/bin/bash  
echo "Augmented Reality Simplify Object File"
if [ "$1" == "" ]
then
	echo "[Invalid CMD]\nUsage: ./arsimple.sh (Texture: Y or N) (% faces of original model (0.0-1.0)) (Input File Name)"
	exit
fi
if [ "$2" == "" ]
then
	echo "[Invalid CMD]\nUsage: ./arsimple.sh (Texture: Y or N) (% faces of original model (0.0-1.0)) (Input File Name)"
	exit
fi  

blender-2.80-linux-glibc217-x86_64/blender -b -P blenderSimplifyV2.py -- --ratio $1 --inm input/$2.obj --outm $2$1 --tris tris.txt


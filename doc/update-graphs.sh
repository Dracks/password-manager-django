#!/usr/bin/env bash

for i in $(ls *.puml); do
	echo $i
	java -jar plantuml.jar $i
done

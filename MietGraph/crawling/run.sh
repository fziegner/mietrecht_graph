#!/bin/bash

output=$1
log="/dev/stdout"

mkdir -p $output

scrapy crawl -o $output/jurabasic.json JuraBasic --logfile=$log
scrapy crawl -o $output/mietrechteinfach.json MietrechtEinfach --logfile=$log
scrapy crawl -o $output/mietrechtlexikon.json MietrechtLexikon --logfile=$log
scrapy crawl -o $output/bgb.json BGB --logfile=$log
scrapy crawl -o $output/bmgev.json BMGEV --logfile=$log
scrapy crawl -o $output/rechtslexikon.json Rechtslexikon --logfile=$log

#!/bin/bash

output=$1
log="/dev/stdout"

mkdir -p $output

scrapy crawl -o $output/bauprofessor.json Bauprofessor --logfile=$log
scrapy crawl -o $output/baunormenlexikondin.json BaunormenlexikonDIN --logfile=$log
scrapy crawl -o $output/baunormenlexikonvob.json BaunormenlexikonVOB --logfile=$log
scrapy crawl -o $output/beuthlex.json BeuthLex --logfile=$log
scrapy crawl -o $output/hoai.json HOAI --logfile=$log

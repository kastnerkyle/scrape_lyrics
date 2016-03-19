#!/bin/bash

echo '' > all_sites.txt
for i in *gz; do
    zcat $i | grep loc | awk -F '>' '{print $2}' | awk -F '<' '{print $1}' >> all_sites.txt
done

grep -v "File:" all_sites.txt > tmp.txt; mv tmp.txt all_sites.txt 
grep -v "blog" all_sites.txt > tmp.txt; mv tmp.txt all_sites.txt 
grep -v "Blog" all_sites.txt > tmp.txt; mv tmp.txt all_sites.txt 
grep -v "Category" all_sites.txt > tmp.txt; mv tmp.txt all_sites.txt 
grep -v "/:" all_sites.txt > tmp.txt; mv tmp.txt all_sites.txt 
grep "http://.*:.*" all_sites.txt > tmp.txt; mv tmp.txt all_sites.txt 

mkdir xml_gz_storage
mv *gz* xml_gz_storage

#!/bin/bash
# needs sitemap-index.xml
for i in $(xmllint sitemap-index.xml | grep loc | awk -F ">" '{print $2}' | awk -F "<" '{print $1}'); do
    #echo $i
    sleep 1;
    wget $i;
done;

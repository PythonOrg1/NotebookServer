#!/bin/sh
##
# bash file
##

#auto start tomcat
sh /usr/local/tomcat8/bin/startup.sh

#auto start node pm2
cd /usr/local/node/webapps/regendeeplearning
pm2 start processes.json

cd /usr/local/node/webapps/regendeeplearningDLSystem
pm2 start processes.json

# auto start notebook server
## release server
python3 /notebook/NotebookServer/project/main/main.py

## dev server
#python3 ~/notebook/NotebookServer/project/main/main.py

## jupyter notebook
jupyter notebook --allow-root --ip=0.0.0.0 --no-browser

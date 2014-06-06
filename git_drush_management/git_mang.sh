#!/bin/bash

NOW=$(date +"%m-%d-%y-%H-%M-%S")

#echo -n "Enter a command for which directory you want to save the SQL in (e.g. ~) "
#read sql_location

cd ~
cd public_html/drupal/
#cd $sql_location

drush sql-dump --result-file=../18.sql

drush vset --exact site_offline 1

#git fetch --tags

#git checkout -b $branch $tag

drush vset --exact site_offline 0

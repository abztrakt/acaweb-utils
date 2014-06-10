#!/bin/bash

NOW=$(date +"%m-%d-%y-%H-%M-%S")

source variable_list.sh
cd ~
#echo "We are in your home directory now"
cd $DRUPAL_LOCATION
#echo `pwd`
#echo "We're in!"

drush sql-dump --result-file=../$NOW.sql

#this goes above drupal site to where .sql was just saved 
cd ..
#echo This is your current directory: `pwd`

#check if sql file is in there
#then move file to $sql_location
mv $NOW.sql $SQL_LOCATION

cd ~
cd $DRUPAL_LOCATION

drush vset --exact site_offline 1

echo -n "Enter a name for the branch you want to create (e.g. eScience3.6) "
read BRANCH_NAME
echo -n "Enter a name for the tag you want to create (e.g. v3.6) "
read TAG_NAME

git fetch --tags

git checkout -b $BRANCH_NAME  $TAG_NAME

drush vset --exact site_offline 0

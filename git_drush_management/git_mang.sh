#!/bin/bash

NOW=$(date +"%m-%d-%y-%H-%M-%S")

echo -n "Choose your sites variable list (e.g. escience_variables.sh) "
read VARIABLES

source $VARIABLES
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

echo -n "Enter a name for the branch you want to create (e.g. v3.6) "
read BRANCH_NAME
echo -n "Enter a name for the tag you want to create (e.g. sitename-3.6) "
read TAG_NAME

git fetch --tags

drush vset --exact site_offline 1

git checkout -b $BRANCH_NAME  $TAG_NAME

drush -v updatedb

drush vset --exact site_offline 0

drush cache-clear all

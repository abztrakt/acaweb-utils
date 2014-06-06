#!/bin/bash

NOW=$(date +"%m-%d-%y-%H-%M-%S")

cd ~
echo "We are in your home directory now"
echo -n "Enter the location to cd into your Druapl directory (e.g. public_html/drupal) "
read drupal_location
cd $drupal_location
echo `pwd`
echo "We're in!"

drush sql-dump --result-file=../$NOW.sql

echo -n "Enter the location for which directory you want to move the SQL file into (e.g. testing/) "
read sql_location

#this goes above drupal site 
cd ..
mv $NOW.sql $sql_location
#cd back into ~ then back into $drupal_location instead of command below
cd drupal/

#check if sql file is in there
#then move file to $sql_location

drush vset --exact site_offline 1

echo -n "Enter a name for the branch you want to create (e.g. eScience3.6) "
read branch
echo -n "Enter a name for the tag you want to create (e.g. v3.6) "
read tag

git fetch --tags

echo `pwd`
git branch -a
git tag
git remote -v

git checkout -b $branch $tag

drush vset --exact site_offline 0

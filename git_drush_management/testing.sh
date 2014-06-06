#!/usr/bin/env drush

NOW=$(date +"%m-%d-%y-%H-%M-%S")
echo -n "Enter a command for which directory you want to save the SQL in (e.g. ~) "
read sql_location
echo -n "Enter a command to change directories into the drupal site from your ~ (e.g. public_html/drupal/) "
read drupal_location
echo -n "Enter a name for the tag you want to create (e.g. v3.6) "
read tag
echo -n "Enter a name for the branch you want to create (e.g. eScience3.6) "
read branch
#echo -n "Enter a URL for the branch you want to pull from (e.g. https://github.com/username/repo_name.git) "
#read url

drush sql-dump --result-file=/hw00/d58/muiter/$NOW.sql

#cd $drupal_location

#drush vset --exact site_offline 1

#git fetch --tags

#git checkout -b $branch $tag

#drush vset --exact site_offline 0

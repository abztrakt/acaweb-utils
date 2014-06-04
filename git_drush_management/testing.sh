#!/usr/bin/env drush

NOW=$(date +"%m-%d-%y-%H-%M-%S")
echo -n "Enter a name for the branch you want to create (e.g. v3.6) "
read branch
echo -n "Enter a name for the tag you want to create (e.g. eScience3.6) "
read tag
echo -n "Enter a URL for the branch you want to pull from (e.g. https://github.com/username/repo_name.git) "
read url
echo -n "Enter a unix command for which directory you want to save the SQL (e.g. v3.6) "
read sql_location
echo -n "Enter a unix command to change directories into the drupal site (e.g. v3.6) "
read cd_location

drush sql-dump --result-file=../$NOW.sql

drush vset --exact site_offline 1

git fetch --tags

git checkout -b --track $branch $tag 

drush vset --exact site_offline 0

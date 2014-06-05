NOW=$(date +"%m-%d-%y-%H-%M-%S")

cd ~
cd public_html/drupal/
drush sql-dump --result-file=../$NOW.sql

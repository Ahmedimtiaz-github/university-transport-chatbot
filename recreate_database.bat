@echo off
echo Recreating database...

mysql -u root -pWarmsi@123 -e "DROP DATABASE IF EXISTS bus_routes_db;"
mysql -u root -pWarmsi@123 -e "CREATE DATABASE IF NOT EXISTS bus_routes_db;"
mysql -u root -pWarmsi@123 bus_routes_db < setup_database.sql

echo Database recreation completed!
pause 
CREATE DATABASE wp_database;
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'wikipass';
GRANT ALL PRIVILEGES ON wp_database.* TO 'wp_user'@'localhost';
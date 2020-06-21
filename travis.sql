# Create Testuser
CREATE USER 'django'@'localhost' IDENTIFIED BY '0gn4jd';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP ON *.* TO 'django'@'localhost';
# Create DB
CREATE DATABASE IF NOT EXISTS 'django' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE 'django';
# Add Data
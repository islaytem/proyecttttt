-- base.sql
CREATE DATABASE IF NOT EXISTS base_db;

USE base_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

INSERT INTO users (username, password, is_admin) VALUES ('admin', 'adminpass', 1);

CREATE USER 'juanss'@'localhost' IDENTIFIED BY 'contra';
GRANT ALL PRIVILEGES ON base_db.* TO 'juanss'@'localhost' IDENTIFIED BY 'contra';
FLUSH PRIVILEGIES;
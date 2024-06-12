CREATE DATABASE IF NOT EXISTS dengue;
USE dengue;

CREATE TABLE IF NOT EXISTS dengue.devices (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(50) NULL DEFAULT NULL,
	brand VARCHAR(50) NULL DEFAULT NULL,
	model VARCHAR(50) NULL DEFAULT NULL,
	is_active TINYINT(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS dengue.sensors (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  devices_id INT NULL DEFAULT NULL,
  unit VARCHAR(50) NULL DEFAULT NULL,
  topic VARCHAR(50) NULL DEFAULT NULL,
  localizacao VARCHAR(100) NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS dengue.`read` (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  read_datetime DATETIME NOT NULL,
  sensors_id INT NOT NULL,
  `value` FLOAT NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS dengue.actuators (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  devices_id INT NULL DEFAULT NULL,
  unit VARCHAR(50) NULL DEFAULT NULL,
  topic VARCHAR(50) NULL DEFAULT NULL,
  localizacao VARCHAR(100) NULL DEFAULT NULL
);

CREATE TABLE dengue.`write` (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  write_datetime DATETIME NOT NULL,
  actuators_id INT NOT NULL,
  `value` FLOAT NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS dengue.roles (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) UNIQUE NOT NULL,
  `description` VARCHAR(512) NULL DEFAULT NULL
  );
  
CREATE TABLE IF NOT EXISTS dengue.users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  role_id VARCHAR(45) NULL DEFAULT NULL,
  username VARCHAR(45) UNIQUE NOT NULL,
  email VARCHAR(30) UNIQUE NOT NULL,
  `password` VARCHAR(256) NOT NULL
);
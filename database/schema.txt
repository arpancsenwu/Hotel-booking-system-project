CREATE DATABASE hotel_management;

USE hotel_management;

CREATE TABLE guests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    mobile_no VARCHAR(15) NOT NULL,
    room_no INT NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    checkin_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checkout_date TIMESTAMP NULL
);

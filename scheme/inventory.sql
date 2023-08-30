-- Crear la tabla
CREATE TABLE IF NOT EXISTS drive_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fileId VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    extension VARCHAR(255) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    visibility VARCHAR(20) NOT NULL,
    criticality VARCHAR(20)
);

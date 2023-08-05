

-- Crear la tabla
CREATE TABLE IF NOT EXISTS drive_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    extension VARCHAR(10) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    visibility VARCHAR(20) NOT NULL
);

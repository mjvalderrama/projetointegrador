CREATE TABLE protocolos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(50) NOT NULL UNIQUE,
    data DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    remetente VARCHAR(255),
    destinatario VARCHAR(255),
    assunto TEXT,
    status VARCHAR(50) NOT NULL
);

-- =====================================================
-- Script de Inicialización de Base de Datos
-- Sistema de Reconocimiento Facial
-- =====================================================

-- Eliminar base de datos si existe (opcional, cuidado en producción)
DROP DATABASE IF EXISTS face_recognition_db;

-- Crear base de datos
CREATE DATABASE face_recognition_db;

-- Usar la base de datos
USE face_recognition_db;

-- =====================================================
-- Tabla: users (Empleados registrados)
-- =====================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    image_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para mejorar búsquedas
    INDEX idx_name (name),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Tabla: recognition_logs (Historial de reconocimientos)
-- =====================================================
CREATE TABLE recognition_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recognition_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence_score DECIMAL(5,2),
    image_used VARCHAR(500),
    status ENUM('success', 'failed', 'not_found') DEFAULT 'success',
    
    -- Llave foránea
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Índices
    INDEX idx_user_id (user_id),
    INDEX idx_date (recognition_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Tabla: system_config (Configuraciones del sistema)
-- =====================================================
CREATE TABLE system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value VARCHAR(255) NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Datos iniciales de configuración
-- =====================================================
INSERT INTO system_config (config_key, config_value, description) VALUES
('tolerance', '0.5', 'Tolerancia para el reconocimiento facial (0.4-0.6)'),
('max_upload_size', '5242880', 'Tamaño máximo de archivo en bytes (5MB)'),
('allowed_extensions', 'jpg,jpeg,png', 'Extensiones de imagen permitidas');

-- =====================================================
-- Vista: user_statistics (Estadísticas de usuarios)
-- =====================================================
CREATE VIEW user_statistics AS
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(rl.id) as total_recognitions,
    MAX(rl.recognition_date) as last_recognition
FROM users u
LEFT JOIN recognition_logs rl ON u.id = rl.user_id
GROUP BY u.id, u.name, u.email;

-- =====================================================
-- Datos de prueba (opcional - comentar en producción)
-- =====================================================
-- INSERT INTO users (name, email, image_path) VALUES
-- ('Juan Pérez', 'juan.perez@example.com', 'static/uploads/juan_perez.jpg'),
-- ('María García', 'maria.garcia@example.com', 'static/uploads/maria_garcia.jpg'),
-- ('Carlos López', 'carlos.lopez@example.com', 'static/uploads/carlos_lopez.jpg');

-- =====================================================
-- Verificación de tablas creadas
-- =====================================================
SHOW TABLES;

-- =====================================================
-- Mostrar estructura de la tabla users
-- =====================================================
DESCRIBE users;

-- =====================================================
-- Script completado exitosamente
-- =====================================================
SELECT 'Base de datos inicializada correctamente!' as mensaje;

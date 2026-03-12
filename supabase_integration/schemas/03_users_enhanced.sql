-- Schema para Users (Usuarios) - Arquitectura Vertical Slicing + Hexagonal
-- Tabla para gestionar usuarios del sistema

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(10) NOT NULL CHECK (document_type IN ('CC', 'CE', 'PA', 'TI', 'RC')),
    document_number VARCHAR(30) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255), -- Hash de contraseña (opcional para registro social)
    role VARCHAR(50) NOT NULL DEFAULT 'CITIZEN' CHECK (role IN ('CITIZEN', 'ADMIN', 'MODERATOR', 'OFFICIAL')),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    phone_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints únicos para evitar duplicados
    CONSTRAINT unique_document UNIQUE (document_type, document_number)
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_document ON users(document_type, document_number);
CREATE INDEX IF NOT EXISTS idx_users_full_name ON users(full_name);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Políticas de seguridad (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Políticas para usuarios
CREATE POLICY "Allow insert operations" ON users
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON users
    FOR SELECT USING (is_active = true);

CREATE POLICY "Allow update operations" ON users
    FOR UPDATE USING (true);

-- Trigger para actualizar updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE users IS 'Tabla para gestionar usuarios del sistema de votación';
COMMENT ON COLUMN users.id IS 'Identificador único del usuario';
COMMENT ON COLUMN users.full_name IS 'Nombre completo del usuario';
COMMENT ON COLUMN users.document_type IS 'Tipo de documento (CC: Cédula de Ciudadanía, CE: Cédula de Extranjería, PA: Pasaporte, TI: Tarjeta de Identidad, RC: Registro Civil)';
COMMENT ON COLUMN users.document_number IS 'Número de documento';
COMMENT ON COLUMN users.email IS 'Correo electrónico único del usuario';
COMMENT ON COLUMN users.phone IS 'Número de teléfono (opcional)';
COMMENT ON COLUMN users.password IS 'Hash de la contraseña (opcional para registro social)';
COMMENT ON COLUMN users.role IS 'Rol del usuario (CITIZEN, ADMIN, MODERATOR, OFFICIAL)';
COMMENT ON COLUMN users.is_active IS 'Indica si el usuario está activo';
COMMENT ON COLUMN users.email_verified IS 'Indica si el correo ha sido verificado';
COMMENT ON COLUMN users.phone_verified IS 'Indica si el teléfono ha sido verificado';
COMMENT ON COLUMN users.last_login IS 'Fecha y hora del último inicio de sesión';
COMMENT ON COLUMN users.created_at IS 'Fecha y hora de creación del usuario';
COMMENT ON COLUMN users.updated_at IS 'Fecha y hora de última actualización';

-- Vista para usuarios activos con información básica
CREATE OR REPLACE VIEW active_users AS
SELECT 
    id,
    full_name,
    document_type,
    document_number,
    email,
    phone,
    role,
    created_at
FROM users 
WHERE is_active = true
ORDER BY created_at DESC;

COMMENT ON VIEW active_users IS 'Vista que muestra solo usuarios activos sin información sensible';

-- Función para buscar usuarios por diferentes criterios
CREATE OR REPLACE FUNCTION search_users(
    search_term TEXT DEFAULT NULL,
    role_filter VARCHAR(50) DEFAULT NULL,
    active_only BOOLEAN DEFAULT true
)
RETURNS TABLE (
    id UUID,
    full_name VARCHAR(255),
    document_type VARCHAR(10),
    document_number VARCHAR(30),
    email VARCHAR(255),
    phone VARCHAR(20),
    role VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.full_name,
        u.document_type,
        u.document_number,
        u.email,
        u.phone,
        u.role,
        u.is_active,
        u.created_at
    FROM users u
    WHERE 
        (active_only IS FALSE OR u.is_active = true)
        AND (role_filter IS NULL OR u.role = role_filter)
        AND (
            search_term IS NULL 
            OR 
            LOWER(u.full_name) LIKE LOWER('%' || search_term || '%')
            OR 
            LOWER(u.email) LIKE LOWER('%' || search_term || '%')
            OR 
            u.document_number LIKE '%' || search_term || '%'
        )
    ORDER BY u.created_at DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION search_users IS 'Función para buscar usuarios con múltiples filtros';

-- Trigger para auditoría de cambios importantes
CREATE TABLE IF NOT EXISTS user_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE, LOGIN
    old_values JSONB,
    new_values JSONB,
    changed_by UUID REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_audit_log_user_id ON user_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_user_audit_log_action ON user_audit_log(action);
CREATE INDEX IF NOT EXISTS idx_user_audit_log_created_at ON user_audit_log(created_at);

ALTER TABLE user_audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow insert operations" ON user_audit_log FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON user_audit_log FOR SELECT USING (true);

COMMENT ON TABLE user_audit_log IS 'Tabla de auditoría para cambios en usuarios';
COMMENT ON COLUMN user_audit_log.action IS 'Tipo de acción (CREATE, UPDATE, DELETE, LOGIN)';
COMMENT ON COLUMN user_audit_log.old_values IS 'Valores anteriores en formato JSON';
COMMENT ON COLUMN user_audit_log.new_values IS 'Nuevos valores en formato JSON';
COMMENT ON COLUMN user_audit_log.changed_by IS 'Usuario que realizó el cambio';
COMMENT ON COLUMN user_audit_log.ip_address IS 'Dirección IP desde donde se realizó el cambio';
COMMENT ON COLUMN user_audit_log.user_agent IS 'User agent del navegador o cliente';

-- Funciones comunes y utilidades para la base de datos

-- Función para actualizar timestamps (ya definida en schemas anteriores, pero la incluimos aquí para referencia)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Función para validar formato de email
CREATE OR REPLACE FUNCTION is_valid_email(email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
END;
$$ LANGUAGE plpgsql;

-- Función para generar slug a partir de texto
CREATE OR REPLACE FUNCTION generate_slug(text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN LOWER(
        REGEXP_REPLACE(
            REGEXP_REPLACE(text, '[^\w\s-]', '', 'g'),
            '[-\s]+', '-', 'g'
        )
    );
END;
$$ LANGUAGE plpgsql;

-- Función para obtener estadísticas del sistema
CREATE OR REPLACE FUNCTION get_system_statistics()
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_parties', (SELECT COUNT(*) FROM political_parties WHERE is_active = true),
        'total_members', (SELECT COUNT(*) FROM party_members),
        'active_consultations', (SELECT COUNT(*) FROM popular_consultations 
                                WHERE is_active = true 
                                AND start_date <= CURRENT_TIMESTAMP 
                                AND end_date >= CURRENT_TIMESTAMP),
        'total_votes', (SELECT COUNT(*) FROM consultation_votes),
        'last_updated', CURRENT_TIMESTAMP
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Trigger para validar email en political_parties
CREATE OR REPLACE FUNCTION validate_political_party_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT is_valid_email(NEW.email) THEN
        RAISE EXCEPTION 'El email % no es válido', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_political_party_email_trigger
    BEFORE INSERT OR UPDATE ON political_parties
    FOR EACH ROW EXECUTE FUNCTION validate_political_party_email();

-- Trigger para validar email en users
CREATE OR REPLACE FUNCTION validate_user_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT is_valid_email(NEW.email) THEN
        RAISE EXCEPTION 'El email % no es válido', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_user_email_trigger
    BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION validate_user_email();

-- Función para auditar cambios importantes
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(255) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by UUID,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_table_name ON audit_logs(table_name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_record_id ON audit_logs(record_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_changed_at ON audit_logs(changed_at);

-- Función de auditoría genérica
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_values, changed_at)
        VALUES (TG_TABLE_NAME, OLD.id, TG_OP, row_to_json(OLD), CURRENT_TIMESTAMP);
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_values, new_values, changed_at)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(OLD), row_to_json(NEW), CURRENT_TIMESTAMP);
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (table_name, record_id, action, new_values, changed_at)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(NEW), CURRENT_TIMESTAMP);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Aplicar auditoría a tablas importantes
CREATE TRIGGER audit_political_parties
    AFTER INSERT OR UPDATE OR DELETE ON political_parties
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_party_members
    AFTER INSERT OR UPDATE OR DELETE ON party_members
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_popular_consultations
    AFTER INSERT OR UPDATE OR DELETE ON popular_consultations
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

COMMENT ON TABLE audit_logs IS 'Tabla para auditoría de cambios en el sistema';
COMMENT ON FUNCTION get_system_statistics() IS 'Función que retorna estadísticas generales del sistema';
COMMENT ON FUNCTION is_valid_email(TEXT) IS 'Valida si un texto tiene formato de email válido';
COMMENT ON FUNCTION generate_slug(TEXT) IS 'Genera un slug amigable a partir de texto';

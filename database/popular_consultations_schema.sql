-- Schema para Popular Consultations (Consultas Populares)
-- Arquitectura Vertical Slicing + Hexagonal
-- Tabla para gestionar consultas populares y votaciones

CREATE TABLE IF NOT EXISTS popular_consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    questions JSONB NOT NULL CHECK (jsonb_typeof(questions) = 'array' AND jsonb_array_length(questions) > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'COMPLETED', 'CANCELLED')),
    is_active BOOLEAN DEFAULT true,
    created_by UUID, -- Referencia a usuarios
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_date_range CHECK (end_date > start_date)
);

-- Tabla para opciones de consulta
CREATE TABLE IF NOT EXISTS consultation_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_text VARCHAR(255) NOT NULL,
    option_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_option_order CHECK (option_order >= 0)
);

-- Tabla para votos
CREATE TABLE IF NOT EXISTS consultation_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_id UUID NOT NULL REFERENCES consultation_options(id) ON DELETE CASCADE,
    voter_id UUID NOT NULL, -- Referencia a sistema de identificación de votantes
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    UNIQUE(consultation_id, voter_id) -- Un voto por consulta por votante
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_popular_consultations_start_date ON popular_consultations(start_date);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_end_date ON popular_consultations(end_date);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_status ON popular_consultations(status);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_is_active ON popular_consultations(is_active);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_created_by ON popular_consultations(created_by);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_questions ON popular_consultations USING GIN(questions);

CREATE INDEX IF NOT EXISTS idx_consultation_options_consultation_id ON consultation_options(consultation_id);
CREATE INDEX IF NOT EXISTS idx_consultation_options_order ON consultation_options(option_order);

CREATE INDEX IF NOT EXISTS idx_consultation_votes_consultation_id ON consultation_votes(consultation_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_option_id ON consultation_votes(option_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_voter_id ON consultation_votes(voter_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_voted_at ON consultation_votes(voted_at);

-- Políticas de seguridad (Row Level Security)
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_options ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_votes ENABLE ROW LEVEL SECURITY;

-- Políticas para popular_consultations
CREATE POLICY "Allow insert operations" ON popular_consultations
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON popular_consultations
    FOR SELECT USING (is_active = true);

CREATE POLICY "Allow update operations" ON popular_consultations
    FOR UPDATE USING (true);

-- Políticas para consultation_options
CREATE POLICY "Allow insert operations" ON consultation_options
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON consultation_options
    FOR SELECT USING (true);

CREATE POLICY "Allow update operations" ON consultation_options
    FOR UPDATE USING (true);

-- Políticas para consultation_votes
CREATE POLICY "Allow insert operations" ON consultation_votes
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON consultation_votes
    FOR SELECT USING (true);

-- Trigger para actualizar updated_at
CREATE TRIGGER update_popular_consultations_updated_at 
    BEFORE UPDATE ON popular_consultations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE popular_consultations IS 'Tabla para gestionar consultas populares y votaciones ciudadanas';
COMMENT ON COLUMN popular_consultations.id IS 'Identificador único de la consulta';
COMMENT ON COLUMN popular_consultations.title IS 'Título descriptivo de la consulta';
COMMENT ON COLUMN popular_consultations.description IS 'Descripción detallada del contexto y propósito de la consulta';
COMMENT ON COLUMN popular_consultations.questions IS 'Array JSON de preguntas que se formularán a los ciudadanos (debe contener al menos una pregunta)';
COMMENT ON COLUMN popular_consultations.start_date IS 'Fecha de inicio del período de votación';
COMMENT ON COLUMN popular_consultations.end_date IS 'Fecha de fin del período de votación (debe ser posterior a start_date)';
COMMENT ON COLUMN popular_consultations.status IS 'Estado de la consulta (ACTIVE, INACTIVE, COMPLETED, CANCELLED)';
COMMENT ON COLUMN popular_consultations.is_active IS 'Indica si la consulta está actualmente activa para votación';
COMMENT ON COLUMN popular_consultations.created_by IS 'Usuario administrador que creó la consulta';

COMMENT ON TABLE consultation_options IS 'Tabla para opciones de respuesta de consultas';
COMMENT ON COLUMN consultation_options.id IS 'Identificador único de la opción';
COMMENT ON COLUMN consultation_options.consultation_id IS 'ID de la consulta padre';
COMMENT ON COLUMN consultation_options.option_text IS 'Texto de la opción';
COMMENT ON COLUMN consultation_options.option_order IS 'Orden de la opción';

COMMENT ON TABLE consultation_votes IS 'Tabla para registrar votos en consultas';
COMMENT ON COLUMN consultation_votes.id IS 'Identificador único del voto';
COMMENT ON COLUMN consultation_votes.consultation_id IS 'ID de la consulta votada';
COMMENT ON COLUMN consultation_votes.option_id IS 'ID de la opción seleccionada';
COMMENT ON COLUMN consultation_votes.voter_id IS 'ID del votante';
COMMENT ON COLUMN consultation_votes.voted_at IS 'Fecha y hora del voto';
COMMENT ON COLUMN consultation_votes.ip_address IS 'Dirección IP del votante';

-- Vista para resultados de consultas
CREATE OR REPLACE VIEW consultation_results AS
SELECT 
    c.id as consultation_id,
    c.title,
    c.questions,
    co.id as option_id,
    co.option_text,
    co.option_order,
    COUNT(cv.id) as vote_count,
    ROUND(
        (COUNT(cv.id) * 100.0 / 
         (SELECT COUNT(*) FROM consultation_votes cv2 WHERE cv2.consultation_id = c.id)
        ), 2
    ) as vote_percentage
FROM popular_consultations c
LEFT JOIN consultation_options co ON c.id = co.consultation_id
LEFT JOIN consultation_votes cv ON co.id = cv.option_id
WHERE c.is_active = true
GROUP BY c.id, c.title, c.questions, co.id, co.option_text, co.option_order
ORDER BY c.id, co.option_order;

COMMENT ON VIEW consultation_results IS 'Vista que muestra resultados de consultas con conteo y porcentajes';

-- Función para obtener consultas activas
CREATE OR REPLACE FUNCTION get_active_consultations()
RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    description TEXT,
    questions JSONB,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    is_active BOOLEAN,
    created_by UUID,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM popular_consultations
    WHERE is_active = true
    AND status = 'ACTIVE'
    AND start_date <= CURRENT_DATE
    AND end_date >= CURRENT_DATE
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Función para verificar si un usuario ya votó
CREATE OR REPLACE FUNCTION has_user_voted(p_consultation_id UUID, p_voter_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    vote_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO vote_count
    FROM consultation_votes
    WHERE consultation_id = p_consultation_id
    AND voter_id = p_voter_id;
    
    RETURN vote_count > 0;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener estadísticas de una consulta
CREATE OR REPLACE FUNCTION get_consultation_stats(p_consultation_id UUID)
RETURNS TABLE (
    total_votes BIGINT,
    unique_voters BIGINT,
    options_count BIGINT,
    participation_rate NUMERIC
) AS $$
DECLARE
    total_eligible_voters BIGINT := 1000; -- Este valor debería venir de una tabla de votantes registrados
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM consultation_votes WHERE consultation_id = p_consultation_id),
        (SELECT COUNT(DISTINCT voter_id) FROM consultation_votes WHERE consultation_id = p_consultation_id),
        (SELECT COUNT(*) FROM consultation_options WHERE consultation_id = p_consultation_id),
        CASE 
            WHEN total_eligible_voters > 0 THEN 
                (SELECT COUNT(*)::NUMERIC / total_eligible_voters * 100 
                 FROM consultation_votes 
                 WHERE consultation_id = p_consultation_id)
            ELSE 0 
        END;
END;
$$ LANGUAGE plpgsql;

-- Schema completo para el sistema de votación con Supabase
-- Versión corregida para modo demo y producción

-- =====================================================
-- TABLA DE CONSULTAS POPULARES
-- =====================================================
CREATE TABLE IF NOT EXISTS popular_consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'FINISHED', 'CANCELLED')),
    min_votes INTEGER DEFAULT 1,
    created_by UUID, -- Sin referencia para modo demo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA DE OPCIONES DE VOTACIÓN
-- =====================================================
CREATE TABLE IF NOT EXISTS voting_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL DEFAULT 0,
    votes_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA DE VOTOS
-- =====================================================
CREATE TABLE IF NOT EXISTS votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_id UUID NOT NULL REFERENCES voting_options(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    party_member_id UUID, -- Referencia a party_members
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(consultation_id, user_id) -- Un voto por usuario por consulta
);

-- =====================================================
-- TABLA DE PERMISOS DE VOTACIÓN
-- =====================================================
CREATE TABLE IF NOT EXISTS voting_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    can_vote BOOLEAN NOT NULL DEFAULT true,
    granted_by UUID,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(consultation_id, user_id)
);

-- =====================================================
-- ÍNDICES
-- =====================================================

-- Índices para consultas populares
CREATE INDEX IF NOT EXISTS idx_popular_consultations_status ON popular_consultations(status);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_dates ON popular_consultations(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_created_by ON popular_consultations(created_by);

-- Índices para opciones de votación
CREATE INDEX IF NOT EXISTS idx_voting_options_consultation ON voting_options(consultation_id);
CREATE INDEX IF NOT EXISTS idx_voting_options_order ON voting_options(consultation_id, order_index);

-- Índices para votos
CREATE INDEX IF NOT EXISTS idx_votes_consultation ON votes(consultation_id);
CREATE INDEX IF NOT EXISTS idx_votes_user ON votes(user_id);
CREATE INDEX IF NOT EXISTS idx_votes_option ON votes(option_id);
CREATE INDEX IF NOT EXISTS idx_votes_consultation_user ON votes(consultation_id, user_id);

-- Índices para permisos
CREATE INDEX IF NOT EXISTS idx_voting_permissions_consultation ON voting_permissions(consultation_id);
CREATE INDEX IF NOT EXISTS idx_voting_permissions_user ON voting_permissions(user_id);
CREATE INDEX IF NOT EXISTS idx_voting_permissions_can_vote ON voting_permissions(consultation_id, user_id, can_vote);

-- =====================================================
-- TRIGGERS Y FUNCIONES
-- =====================================================

-- Función para actualizar timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para popular_consultations
CREATE TRIGGER update_popular_consultations_updated_at 
    BEFORE UPDATE ON popular_consultations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger para voting_options
CREATE TRIGGER update_voting_options_updated_at 
    BEFORE UPDATE ON voting_options 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para actualizar contador de votos en opciones
CREATE OR REPLACE FUNCTION update_option_votes_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE voting_options 
        SET votes_count = votes_count + 1 
        WHERE id = NEW.option_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE voting_options 
        SET votes_count = votes_count - 1 
        WHERE id = OLD.option_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Trigger para actualizar contador de votos
CREATE TRIGGER trigger_update_option_votes_count
    AFTER INSERT OR DELETE ON votes
    FOR EACH ROW EXECUTE FUNCTION update_option_votes_count();

-- Función para actualizar totales de consulta
CREATE OR REPLACE FUNCTION update_consultation_totals()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar total de votos
    UPDATE popular_consultations 
    SET total_votes = (
        SELECT COUNT(*) 
        FROM votes 
        WHERE consultation_id = COALESCE(NEW.consultation_id, OLD.consultation_id)
    ),
    total_options = (
        SELECT COUNT(*) 
        FROM voting_options 
        WHERE consultation_id = COALESCE(NEW.consultation_id, OLD.consultation_id)
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ language 'plpgsql';

-- Triggers para actualizar totales
CREATE TRIGGER trigger_update_consultation_totals_votes
    AFTER INSERT OR DELETE ON votes
    FOR EACH ROW EXECUTE FUNCTION update_consultation_totals();

CREATE TRIGGER trigger_update_consultation_totals_options
    AFTER INSERT OR DELETE ON voting_options
    FOR EACH ROW EXECUTE FUNCTION update_consultation_totals();

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista para consultas activas con estadísticas
CREATE OR REPLACE VIEW active_consultations AS
SELECT 
    pc.*,
    COUNT(DISTINCT v.id) as vote_count,
    COUNT(DISTINCT vo.id) as option_count
FROM popular_consultations pc
LEFT JOIN votes v ON pc.id = v.consultation_id
LEFT JOIN voting_options vo ON pc.id = vo.consultation_id
WHERE pc.status = 'ACTIVE'
GROUP BY pc.id, pc.title, pc.description, pc.start_date, pc.end_date, pc.status, pc.min_votes, pc.created_by, pc.created_at, pc.updated_at;

-- Vista para usuarios que pueden votar
CREATE OR REPLACE VIEW eligible_voters AS
SELECT 
    vp.user_id,
    vp.consultation_id,
    vp.can_vote,
    pc.title as consultation_title,
    pc.start_date,
    pc.end_date
FROM voting_permissions vp
JOIN popular_consultations pc ON vp.consultation_id = pc.id
WHERE pc.status = 'ACTIVE' 
  AND vp.can_vote = true
  AND pc.start_date <= NOW() 
  AND pc.end_date >= NOW();

-- =====================================================
-- FUNCIONES ÚTILES
-- =====================================================

-- Función para verificar si un usuario puede votar
CREATE OR REPLACE FUNCTION can_user_vote(
    p_user_id UUID,
    p_consultation_id UUID
) RETURNS BOOLEAN AS $$
DECLARE
    has_permission BOOLEAN;
    already_voted BOOLEAN;
    consultation_active BOOLEAN;
BEGIN
    -- Verificar si tiene permiso
    SELECT EXISTS (
        SELECT 1 FROM voting_permissions 
        WHERE user_id = p_user_id 
          AND consultation_id = p_consultation_id 
          AND can_vote = true
    ) INTO has_permission;
    
    -- Verificar si ya votó
    SELECT EXISTS (
        SELECT 1 FROM votes 
        WHERE user_id = p_user_id 
          AND consultation_id = p_consultation_id
    ) INTO already_voted;
    
    -- Verificar si la consulta está activa
    SELECT EXISTS (
        SELECT 1 FROM popular_consultations 
        WHERE id = p_consultation_id 
          AND status = 'ACTIVE'
          AND start_date <= NOW() 
          AND end_date >= NOW()
    ) INTO consultation_active;
    
    RETURN has_permission AND NOT already_voted AND consultation_active;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener resultados de consulta
CREATE OR REPLACE FUNCTION get_consultation_results(
    p_consultation_id UUID
) RETURNS TABLE (
    option_id UUID,
    title VARCHAR,
    votes BIGINT,
    percentage NUMERIC
) AS $$
DECLARE
    total_votes BIGINT;
BEGIN
    -- Obtener total de votos
    SELECT COUNT(*) INTO total_votes
    FROM votes 
    WHERE consultation_id = p_consultation_id;
    
    -- Retornar resultados
    RETURN QUERY
    SELECT 
        vo.id,
        vo.title,
        COALESCE(v.vote_count, 0) as votes,
        CASE 
            WHEN total_votes > 0 THEN 
                ROUND((COALESCE(v.vote_count, 0) * 100.0 / total_votes), 2)
            ELSE 0 
        END as percentage
    FROM voting_options vo
    LEFT JOIN (
        SELECT option_id, COUNT(*) as vote_count
        FROM votes 
        WHERE consultation_id = p_consultation_id
        GROUP BY option_id
    ) v ON vo.id = v.option_id
    WHERE vo.consultation_id = p_consultation_id
    ORDER BY vo.order_index;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- POLÍTICAS DE SEGURIDAD (RLS - ROW LEVEL SECURITY)
-- =====================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE voting_options ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE voting_permissions ENABLE ROW LEVEL SECURITY;

-- Políticas RLS para popular_consultations (modo demo)
CREATE POLICY "Todos pueden ver consultas populares" ON popular_consultations
    FOR SELECT USING (true);

CREATE POLICY "Todos pueden crear consultas (modo demo)" ON popular_consultations
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Todos pueden actualizar consultas (modo demo)" ON popular_consultations
    FOR UPDATE USING (true);

CREATE POLICY "Todos pueden eliminar consultas (modo demo)" ON popular_consultations
    FOR DELETE USING (true);

-- Políticas para voting_options (modo demo)
CREATE POLICY "Todos pueden ver opciones de votación" ON voting_options
    FOR SELECT USING (true);

CREATE POLICY "Todos pueden agregar opciones (modo demo)" ON voting_options
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Todos pueden actualizar opciones (modo demo)" ON voting_options
    FOR UPDATE USING (true);

CREATE POLICY "Todos pueden eliminar opciones (modo demo)" ON voting_options
    FOR DELETE USING (true);

-- Políticas para votos (modo demo)
CREATE POLICY "Todos pueden ver votos" ON votes
    FOR SELECT USING (true);

CREATE POLICY "Todos pueden votar (modo demo)" ON votes
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Todos pueden actualizar votos (modo demo)" ON votes
    FOR UPDATE USING (true);

CREATE POLICY "Todos pueden eliminar votos (modo demo)" ON votes
    FOR DELETE USING (true);

-- Políticas para voting_permissions (modo demo)
CREATE POLICY "Todos pueden ver permisos" ON voting_permissions
    FOR SELECT USING (true);

CREATE POLICY "Todos pueden crear permisos (modo demo)" ON voting_permissions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Todos pueden actualizar permisos (modo demo)" ON voting_permissions
    FOR UPDATE USING (true);

CREATE POLICY "Todos pueden eliminar permisos (modo demo)" ON voting_permissions
    FOR DELETE USING (true);

-- =====================================================
-- DATOS DE EJEMPLO (opcional)
-- =====================================================

-- Insertar consulta de ejemplo (comentado para producción)
-- INSERT INTO popular_consultations (title, description, start_date, end_date, min_votes)
-- VALUES (
--     'Consulta Popular Ejemplo',
--     'Esta es una consulta de ejemplo para probar el sistema de votación',
--     NOW() + INTERVAL '1 day',
--     NOW() + INTERVAL '7 days',
--     10
-- );

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================

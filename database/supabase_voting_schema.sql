-- Schema de Supabase para Sistema de Votación de Consultas Populares
-- Creado: 2026-03-10

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
    created_by UUID, -- Removida referencia temporalmente para modo demo
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
    votes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA DE VOTOS
-- =====================================================
CREATE TABLE IF NOT EXISTS votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_id UUID NOT NULL REFERENCES voting_options(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    party_member_id UUID REFERENCES party_members(id) ON DELETE SET NULL,
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraint para asegurar que un usuario solo vote una vez por consulta
    UNIQUE(consultation_id, user_id)
);

-- =====================================================
-- TABLA DE PERMISOS DE VOTACIÓN
-- =====================================================
CREATE TABLE IF NOT EXISTS voting_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    consultation_id UUID REFERENCES popular_consultations(id) ON DELETE CASCADE,
    can_vote BOOLEAN DEFAULT false,
    granted_by UUID REFERENCES users(id) ON DELETE SET NULL,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraint para asegurar un solo registro por usuario y consulta
    UNIQUE(user_id, consultation_id)
);

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
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
CREATE INDEX IF NOT EXISTS idx_votes_party_member ON votes(party_member_id);

-- Índices para permisos de votación
CREATE INDEX IF NOT EXISTS idx_voting_permissions_user ON voting_permissions(user_id);
CREATE INDEX IF NOT EXISTS idx_voting_permissions_consultation ON voting_permissions(consultation_id);

-- =====================================================
-- POLÍTICAS DE SEGURIDAD (RLS - ROW LEVEL SECURITY)
-- =====================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE voting_options ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE voting_permissions ENABLE ROW LEVEL SECURITY;

-- Políticas RLS para popular_consultations
-- Modo demo: políticas más permisivas
CREATE POLICY "Todos pueden ver consultas populares" ON popular_consultations
    FOR SELECT USING (true);

CREATE POLICY "Todos pueden crear consultas (modo demo)" ON popular_consultations
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Todos pueden actualizar consultas (modo demo)" ON popular_consultations
    FOR UPDATE USING (true);

-- Políticas para voting_options
CREATE POLICY "Todos pueden ver opciones de votación" ON voting_options
    FOR SELECT USING (true);

CREATE POLICY "Todos pueden agregar opciones (modo demo)" ON voting_options
    FOR INSERT WITH CHECK (true);

-- Políticas para votos
CREATE POLICY "Usuarios pueden ver sus propios votos" ON votes
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Usuarios pueden votar si tienen permiso" ON votes
    FOR INSERT WITH CHECK (
        user_id = auth.uid() AND
        EXISTS (
            SELECT 1 FROM voting_permissions 
            WHERE user_id = auth.uid() 
            AND consultation_id = votes.consultation_id 
            AND can_vote = true
        )
    );

-- Políticas para voting_permissions
CREATE POLICY "Usuarios pueden ver sus permisos" ON voting_permissions
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Admins pueden gestionar permisos" ON voting_permissions
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM user_permissions 
            WHERE user_id = auth.uid() 
            AND permission = 'MANAGE_VOTING_PERMISSIONS'
        )
    );

-- =====================================================
-- TRIGGERS PARA ACTUALIZACIÓN DE CONTADORES
-- =====================================================

-- Trigger para actualizar el contador de votos en voting_options
CREATE OR REPLACE FUNCTION update_vote_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE voting_options 
    SET votes_count = votes_count + 1 
    WHERE id = NEW.option_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_vote_count
    AFTER INSERT ON votes
    FOR EACH ROW
    EXECUTE FUNCTION update_vote_count();

-- Trigger para actualizar updated_at en popular_consultations
CREATE OR REPLACE FUNCTION update_consultation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_consultation_timestamp
    BEFORE UPDATE ON popular_consultations
    FOR EACH ROW
    EXECUTE FUNCTION update_consultation_timestamp();

-- =====================================================
-- FUNCIONES ÚTILES
-- =====================================================

-- Función para verificar si un usuario puede votar en una consulta
CREATE OR REPLACE FUNCTION can_user_vote(
    p_user_id UUID,
    p_consultation_id UUID
) RETURNS BOOLEAN AS $$
DECLARE
    has_permission BOOLEAN;
    is_member BOOLEAN;
BEGIN
    -- Verificar si tiene permiso explícito
    SELECT (can_vote = true) INTO has_permission
    FROM voting_permissions
    WHERE user_id = p_user_id AND consultation_id = p_consultation_id;
    
    -- Verificar si es miembro de partido político
    SELECT COUNT(*) > 0 INTO is_member
    FROM party_members
    WHERE user_id = p_user_id AND is_active = true;
    
    -- Puede votar si tiene permiso Y es miembro de partido
    RETURN COALESCE(has_permission, false) AND COALESCE(is_member, false);
END;
$$ LANGUAGE plpgsql;

-- Función para obtener resultados de una consulta
CREATE OR REPLACE FUNCTION get_consultation_results(
    p_consultation_id UUID
) RETURNS TABLE (
    option_id UUID,
    option_title VARCHAR,
    votes_count BIGINT,
    percentage DECIMAL(5,2)
) AS $$
DECLARE
    total_votes BIGINT;
BEGIN
    -- Obtener total de votos
    SELECT COUNT(*) INTO total_votes
    FROM votes
    WHERE consultation_id = p_consultation_id;
    
    -- Retornar resultados con porcentajes
    RETURN QUERY
    SELECT 
        vo.id,
        vo.title,
        COALESCE(vo.votes_count, 0) as votes_count,
        CASE 
            WHEN total_votes > 0 THEN 
                ROUND((COALESCE(vo.votes_count, 0) * 100.0 / total_votes), 2)
            ELSE 0 
        END as percentage
    FROM voting_options vo
    WHERE vo.consultation_id = p_consultation_id
    ORDER BY vo.order_index;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista para consultas activas con información adicional
CREATE OR REPLACE VIEW active_consultations AS
SELECT 
    pc.*,
    COUNT(DISTINCT v.id) as total_votes,
    COUNT(DISTINCT vo.id) as total_options,
    CASE 
        WHEN pc.end_date < NOW() THEN 'FINISHED'
        WHEN pc.start_date > NOW() THEN 'PENDING'
        ELSE 'ACTIVE'
    END as current_status
FROM popular_consultations pc
LEFT JOIN votes v ON pc.id = v.consultation_id
LEFT JOIN voting_options vo ON pc.id = vo.consultation_id
WHERE pc.status = 'ACTIVE'
GROUP BY pc.id, pc.title, pc.description, pc.start_date, pc.end_date, pc.status, pc.min_votes, pc.created_by, pc.created_at, pc.updated_at;

-- Vista para usuarios que pueden votar
CREATE OR REPLACE VIEW eligible_voters AS
SELECT DISTINCT
    u.id as user_id,
    u.full_name,
    u.email,
    pm.id as party_member_id,
    pm.party_id,
    p.name as party_name,
    vp.consultation_id
FROM users u
INNER JOIN party_members pm ON u.id = pm.user_id AND pm.is_active = true
INNER JOIN political_parties p ON pm.party_id = p.id
INNER JOIN voting_permissions vp ON u.id = vp.user_id AND vp.can_vote = true
WHERE u.is_active = true;

-- =====================================================
-- DATOS DE EJEMPLO (opcional)
-- =====================================================

-- Insertar consulta de ejemplo (comentado para producción)
-- INSERT INTO popular_consultations (title, description, end_date, created_by)
-- VALUES (
--     'Consulta Popular Ejemplo',
--     'Esta es una consulta de ejemplo para probar el sistema de votación',
--     NOW() + INTERVAL '7 days',
--     (SELECT id FROM users LIMIT 1)
-- );

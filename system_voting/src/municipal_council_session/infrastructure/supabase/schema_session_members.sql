-- =====================================================
-- SCHEMA SUPABASE - SESSION MEMBERS Y SESSION BANCADAS
-- Sistema de Votación Municipal
-- =====================================================

-- =====================================================
-- TABLA: session_members
-- Miembros asociados a una sesión
-- =====================================================
CREATE TABLE IF NOT EXISTS session_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_session UUID NOT NULL,
    id_member UUID NOT NULL,
    is_present BOOLEAN DEFAULT FALSE,
    arrival_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_session_members_session ON session_members(id_session);
CREATE INDEX IF NOT EXISTS idx_session_members_member ON session_members(id_member);
CREATE INDEX IF NOT EXISTS idx_session_members_presence ON session_members(is_present);

-- Comentarios
COMMENT ON TABLE session_members IS 'Miembros del consejo asociados a una sesión';
COMMENT ON COLUMN session_members.id_session IS 'UUID de la sesión del consejo';
COMMENT ON COLUMN session_members.id_member IS 'UUID del miembro del consejo (party_members)';
COMMENT ON COLUMN session_members.is_present IS 'Si el miembro esta presente en la sesión';
COMMENT ON COLUMN session_members.arrival_time IS 'Hora de llegada del miembro';

-- RLS
ALTER TABLE session_members DISABLE ROW LEVEL SECURITY;

-- Grants
GRANT ALL ON session_members TO anon, authenticated, service_role;

-- =====================================================
-- TABLA: session_bancadas
-- Bancadas asociadas a una sesión
-- =====================================================
CREATE TABLE IF NOT EXISTS session_bancadas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_session UUID NOT NULL,
    id_bancada UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_session_bancadas_session ON session_bancadas(id_session);
CREATE INDEX IF NOT EXISTS idx_session_bancadas_bancada ON session_bancadas(id_bancada);

-- Comentarios
COMMENT ON TABLE session_bancadas IS 'Bancadas asociadas a una sesión del consejo';
COMMENT ON COLUMN session_bancadas.id_session IS 'UUID de la sesión del consejo';
COMMENT ON COLUMN session_bancadas.id_bancada IS 'UUID de la bancada';

-- RLS
ALTER TABLE session_bancadas DISABLE ROW LEVEL SECURITY;

-- Grants
GRANT ALL ON session_bancadas TO anon, authenticated, service_role;

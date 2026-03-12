-- Tabla de Votos para Consulta Popular
-- Nombre de la tabla: votes_consult

CREATE TABLE IF NOT EXISTS votes_consult (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_consult UUID NOT NULL,
    id_member UUID NOT NULL,
    id_party UUID NOT NULL,
    id_auth UUID NOT NULL,
    value_vote BOOLEAN NOT NULL,
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security
ALTER TABLE votes_consult ENABLE ROW LEVEL SECURITY;

-- Política pública para desarrollo (ajustar para producción)
CREATE POLICY "Allow all for votes_consult" ON votes_consult FOR ALL USING (true) WITH CHECK (true);

-- Índices para mejorar rendimiento
CREATE INDEX idx_votes_consult_id_consult ON votes_consult(id_consult);
CREATE INDEX idx_votes_consult_id_member ON votes_consult(id_member);
CREATE INDEX idx_votes_consult_id_party ON votes_consult(id_party);
CREATE INDEX idx_votes_consult_id_auth ON votes_consult(id_auth);
CREATE INDEX idx_votes_consult_created_at ON votes_consult(created_at DESC);

-- Índices únicos para evitar votos duplicados
CREATE UNIQUE INDEX idx_votes_consult_unique_member_consult ON votes_consult(id_member, id_consult);

-- Ejemplo de datos de prueba
-- INSERT INTO votes_consult (id_consult, id_member, id_party, id_auth, value_vote, comment)
-- VALUES (
--     'consult-uuid-1',
--     'member-uuid-1',
--     'party-uuid-1',
--     'auth-uuid-1',
--     true,
--     'Estoy de acuerdo con la propuesta'
-- );

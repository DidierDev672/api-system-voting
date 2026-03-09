-- Schema para Political Parties (Partidos Políticos)
-- Tabla para almacenar la información de partidos políticos y movimientos

CREATE TABLE IF NOT EXISTS political_parties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    acronym VARCHAR(20) NOT NULL,
    party_type VARCHAR(20) NOT NULL CHECK (party_type IN ('PARTY', 'MOVEMENT')),
    ideology TEXT,
    legal_representative VARCHAR(255) NOT NULL,
    representative_id VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    foundation_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_political_parties_name ON political_parties(name);
CREATE INDEX IF NOT EXISTS idx_political_parties_acronym ON political_parties(acronym);
CREATE INDEX IF NOT EXISTS idx_political_parties_party_type ON political_parties(party_type);
CREATE INDEX IF NOT EXISTS idx_political_parties_email ON political_parties(email);
CREATE INDEX IF NOT EXISTS idx_political_parties_is_active ON political_parties(is_active);
CREATE INDEX IF NOT EXISTS idx_political_parties_created_at ON political_parties(created_at);

-- Políticas de seguridad (Row Level Security)
ALTER TABLE political_parties ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserciones (registro de nuevos partidos)
CREATE POLICY "Allow insert operations" ON political_parties
    FOR INSERT WITH CHECK (true);

-- Política para permitir lecturas (consultas de partidos)
CREATE POLICY "Allow select operations" ON political_parties
    FOR SELECT USING (is_active = true);

-- Política para permitir actualizaciones
CREATE POLICY "Allow update operations" ON political_parties
    FOR UPDATE USING (true);

-- Trigger para actualizar updated_at
CREATE TRIGGER update_political_parties_updated_at 
    BEFORE UPDATE ON political_parties 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Restricción adicional: la sigla debe ser única y en mayúsculas
CREATE OR REPLACE FUNCTION normalize_acronym()
RETURNS TRIGGER AS $$
BEGIN
    NEW.acronym = UPPER(NEW.acronym);
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER normalize_political_party_acronym 
    BEFORE INSERT OR UPDATE ON political_parties 
    FOR EACH ROW EXECUTE FUNCTION normalize_acronym();

-- Comentarios para documentación
COMMENT ON TABLE political_parties IS 'Tabla para registrar partidos políticos y movimientos';
COMMENT ON COLUMN political_parties.id IS 'Identificador único del partido';
COMMENT ON COLUMN political_parties.name IS 'Nombre completo del partido';
COMMENT ON COLUMN political_parties.acronym IS 'Sigla del partido (automáticamente en mayúsculas)';
COMMENT ON COLUMN political_parties.party_type IS 'Tipo de organización: PARTY o MOVEMENT';
COMMENT ON COLUMN political_parties.ideology IS 'Descripción de la ideología política';
COMMENT ON COLUMN political_parties.legal_representative IS 'Nombre del representante legal';
COMMENT ON COLUMN political_parties.representative_id IS 'Identificación del representante legal';
COMMENT ON COLUMN political_parties.email IS 'Email de contacto del partido';
COMMENT ON COLUMN political_parties.foundation_date IS 'Fecha de fundación del partido';
COMMENT ON COLUMN political_parties.is_active IS 'Indica si el partido está activo';
COMMENT ON COLUMN political_parties.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN political_parties.updated_at IS 'Fecha de última actualización';

-- Vista para obtener estadísticas de partidos
CREATE OR REPLACE VIEW party_statistics AS
SELECT 
    pp.id,
    pp.name,
    pp.acronym,
    pp.party_type,
    COUNT(pm.id) as member_count,
    pp.foundation_date,
    pp.created_at
FROM political_parties pp
LEFT JOIN party_members pm ON pp.id = pm.political_party_id
WHERE pp.is_active = true
GROUP BY pp.id, pp.name, pp.acronym, pp.party_type, pp.foundation_date, pp.created_at
ORDER BY member_count DESC;

COMMENT ON VIEW party_statistics IS 'Vista que muestra estadísticas de miembros por partido';

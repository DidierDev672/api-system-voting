-- Schema para Party Members (Miembros de Partidos)
-- Tabla para almacenar la información de afiliados a partidos políticos

CREATE TABLE IF NOT EXISTS party_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(5) NOT NULL,
    document_number VARCHAR(30) NOT NULL UNIQUE,
    birth_date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    political_party_id UUID NOT NULL,
    consent BOOLEAN NOT NULL CHECK (consent = true),
    data_authorization BOOLEAN NOT NULL CHECK (data_authorization = true),
    affiliation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_party_members_political_party_id ON party_members(political_party_id);
CREATE INDEX IF NOT EXISTS idx_party_members_document_number ON party_members(document_number);
CREATE INDEX IF NOT EXISTS idx_party_members_created_at ON party_members(created_at);

-- Políticas de seguridad (Row Level Security)
ALTER TABLE party_members ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserciones (registro de nuevos miembros)
CREATE POLICY "Allow insert operations" ON party_members
    FOR INSERT WITH CHECK (true);

-- Política para permitir lecturas (consultas de miembros)
CREATE POLICY "Allow select operations" ON party_members
    FOR SELECT USING (true);

-- Política para permitir actualizaciones
CREATE POLICY "Allow update operations" ON party_members
    FOR UPDATE USING (true);

-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_party_members_updated_at 
    BEFORE UPDATE ON party_members 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE party_members IS 'Tabla para registrar miembros afiliados a partidos políticos';
COMMENT ON COLUMN party_members.id IS 'Identificador único del miembro';
COMMENT ON COLUMN party_members.full_name IS 'Nombre completo del miembro';
COMMENT ON COLUMN party_members.document_type IS 'Tipo de documento (CC, CE, PAS, etc.)';
COMMENT ON COLUMN party_members.document_number IS 'Número de documento único';
COMMENT ON COLUMN party_members.birth_date IS 'Fecha de nacimiento';
COMMENT ON COLUMN party_members.city IS 'Ciudad de residencia';
COMMENT ON COLUMN party_members.political_party_id IS 'ID del partido político al que está afiliado';
COMMENT ON COLUMN party_members.consent IS 'Consentimiento para afiliación política';
COMMENT ON COLUMN party_members.data_authorization IS 'Autorización para tratamiento de datos';
COMMENT ON COLUMN party_members.affiliation_date IS 'Fecha de afiliación al partido';
COMMENT ON COLUMN party_members.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN party_members.updated_at IS 'Fecha de última actualización';

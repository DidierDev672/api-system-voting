-- Schema para Secretario de Consejo Municipal
-- Tabla: municipal_council_secretaries

-- Crear tabla
CREATE TABLE IF NOT EXISTS municipal_council_secretaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    document_type TEXT NOT NULL CHECK (document_type IN ('CI', 'Pasaporte', 'Licencia', 'Otro')),
    document_id TEXT NOT NULL UNIQUE,
    exact_position TEXT NOT NULL CHECK (exact_position IN ('Secretario General', 'Secretario de comision')),
    administrative_act TEXT NOT NULL,
    possession_date TEXT NOT NULL,
    legal_period TEXT NOT NULL,
    professional_title TEXT,
    performance_type TEXT NOT NULL CHECK (performance_type IN ('ad-hoc', 'temporal')),
    institutional_email TEXT NOT NULL,
    digital_signature TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security (RLS)
ALTER TABLE municipal_council_secretaries ENABLE ROW LEVEL SECURITY;

-- Politica RLS: anyone can read
CREATE POLICY "Anyone can read municipal_council_secretaries" 
ON municipal_council_secretaries 
FOR SELECT USING (true);

-- Politica RLS: anyone can insert
CREATE POLICY "Anyone can insert municipal_council_secretaries" 
ON municipal_council_secretaries 
FOR INSERT WITH CHECK (true);

-- Politica RLS: anyone can update
CREATE POLICY "Anyone can update municipal_council_secretaries" 
ON municipal_council_secretaries 
FOR UPDATE USING (true);

-- Politica RLS: anyone can delete
CREATE POLICY "Anyone can delete municipal_council_secretaries" 
ON municipal_council_secretaries 
FOR DELETE USING (true);

-- Crear indice para busqueda por document_id
CREATE INDEX IF NOT EXISTS idx_municipal_council_secretaries_document_id 
ON municipal_council_secretaries(document_id);

-- Crear indice para busqueda por exact_position
CREATE INDEX IF NOT EXISTS idx_municipal_council_secretaries_position 
ON municipal_council_secretaries(exact_position);

-- Crear indice para busqueda por institutional_email
CREATE INDEX IF NOT EXISTS idx_municipal_council_secretaries_email 
ON municipal_council_secretaries(institutional_email);

-- Funcion para actualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar updated_at
CREATE TRIGGER update_municipal_council_secretaries_updated_at
    BEFORE UPDATE ON municipal_council_secretaries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentacion
COMMENT ON TABLE municipal_council_secretaries IS 'Tabla para almacenar los datos de los secretarios de consejo municipal';
COMMENT ON COLUMN municipal_council_secretaries.full_name IS 'Nombre completo del secretario';
COMMENT ON COLUMN municipal_council_secretaries.document_type IS 'Tipo de documento (CI, Pasaporte, Licencia, Otro)';
COMMENT ON COLUMN municipal_council_secretaries.document_id IS 'Numero de documento de identidad';
COMMENT ON COLUMN municipal_council_secretaries.exact_position IS 'Cargo exacto (Secretario General, Secretario de comision)';
COMMENT ON COLUMN municipal_council_secretaries.administrative_act IS 'Acto administrativo de eleccion';
COMMENT ON COLUMN municipal_council_secretaries.possession_date IS 'Fecha de posesion';
COMMENT ON COLUMN municipal_council_secretaries.legal_period IS 'Periodo legal';
COMMENT ON COLUMN municipal_council_secretaries.professional_title IS 'Titulo profesional';
COMMENT ON COLUMN municipal_council_secretaries.performance_type IS 'Calidad de actuacion (ad-hoc, temporal)';
COMMENT ON COLUMN municipal_council_secretaries.institutional_email IS 'Correo institucional';
COMMENT ON COLUMN municipal_council_secretaries.digital_signature IS 'Firma digital (base64)';

-- Schema para Presidente de Consejo Municipal
-- Tabla: municipal_council_presidents

-- Crear tabla
CREATE TABLE IF NOT EXISTS municipal_council_presidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    document_type TEXT NOT NULL CHECK (document_type IN ('CI', 'Pasaporte', 'Licencia', 'Otro')),
    document_id TEXT NOT NULL UNIQUE,
    board_position TEXT NOT NULL,
    political_party TEXT NOT NULL,
    election_period TEXT NOT NULL,
    presidency_type TEXT NOT NULL CHECK (presidency_type IN ('Propietario', 'Suplente', 'Interino')),
    position_time TEXT NOT NULL,
    institutional_email TEXT NOT NULL,
    digital_signature TEXT,
    fingerprint TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security (RLS)
ALTER TABLE municipal_council_presidents ENABLE ROW LEVEL SECURITY;

-- Politica RLS: anyone can read
CREATE POLICY "Anyone can read municipal_council_presidents" 
ON municipal_council_presidents 
FOR SELECT USING (true);

-- Politica RLS: anyone can insert
CREATE POLICY "Anyone can insert municipal_council_presidents" 
ON municipal_council_presidents 
FOR INSERT WITH CHECK (true);

-- Politica RLS: anyone can update
CREATE POLICY "Anyone can update municipal_council_presidents" 
ON municipal_council_presidents 
FOR UPDATE USING (true);

-- Politica RLS: anyone can delete
CREATE POLICY "Anyone can delete municipal_council_presidents" 
ON municipal_council_presidents 
FOR DELETE USING (true);

-- Crear indice para busqueda por document_id
CREATE INDEX IF NOT EXISTS idx_municipal_council_presidents_document_id 
ON municipal_council_presidents(document_id);

-- Crear indice para busqueda por political_party
CREATE INDEX IF NOT EXISTS idx_municipal_council_presidents_political_party 
ON municipal_council_presidents(political_party);

-- Crear indice para busqueda por election_period
CREATE INDEX IF NOT EXISTS idx_municipal_council_presidents_election_period 
ON municipal_council_presidents(election_period);

-- Crear indice para busqueda por institutional_email
CREATE INDEX IF NOT EXISTS idx_municipal_council_presidents_email 
ON municipal_council_presidents(institutional_email);

-- Funcion para actualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar updated_at
CREATE TRIGGER update_municipal_council_presidents_updated_at
    BEFORE UPDATE ON municipal_council_presidents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentacion
COMMENT ON TABLE municipal_council_presidents IS 'Tabla para almacenar los datos de los presidentes de consejo municipal';
COMMENT ON COLUMN municipal_council_presidents.full_name IS 'Nombre completo del presidente';
COMMENT ON COLUMN municipal_council_presidents.document_type IS 'Tipo de documento (CI, Pasaporte, Licencia, Otro)';
COMMENT ON COLUMN municipal_council_presidents.document_id IS 'Numero de documento de identidad';
COMMENT ON COLUMN municipal_council_presidents.board_position IS 'Cargo en la mesa de votacion';
COMMENT ON COLUMN municipal_council_presidents.political_party IS 'Partido politico al que pertenece';
COMMENT ON COLUMN municipal_council_presidents.election_period IS 'Periodo de eleccion';
COMMENT ON COLUMN municipal_council_presidents.presidency_type IS 'Calidad de presidencia (Propietario, Suplente, Interino)';
COMMENT ON COLUMN municipal_council_presidents.position_time IS 'Hora de toma de posicion';
COMMENT ON COLUMN municipal_council_presidents.institutional_email IS 'Correo institucional';
COMMENT ON COLUMN municipal_council_presidents.digital_signature IS 'Firma digital (base64)';
COMMENT ON COLUMN municipal_council_presidents.fingerprint IS 'Huella digital (base64)';

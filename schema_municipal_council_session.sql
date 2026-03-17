-- Schema para Sesion de Consejo Municipal
-- Tabla: municipal_council_sessions

-- Crear tabla
CREATE TABLE IF NOT EXISTS municipal_council_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title_session TEXT NOT NULL,
    type_session TEXT NOT NULL CHECK (type_session IN ('Ordinaria', 'Extraordinaria', 'Especial', 'Instalacion')),
    status_session TEXT NOT NULL CHECK (status_session IN ('Convocada', 'En progreso', 'Realizada', 'Cancelada', 'Postergada')),
    date_hour_start TIMESTAMP WITH TIME ZONE NOT NULL,
    date_hour_end TIMESTAMP WITH TIME ZONE NOT NULL,
    modality TEXT NOT NULL CHECK (modality IN ('presencial', 'virtual', 'hibrida')),
    place_enclosure TEXT NOT NULL,
    orden_day TEXT NOT NULL,
    quorum_required INTEGER NOT NULL CHECK (quorum_required >= 1),
    id_president UUID NOT NULL REFERENCES municipal_council_presidents(id),
    id_secretary UUID NOT NULL REFERENCES municipal_council_secretaries(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security (RLS)
ALTER TABLE municipal_council_sessions ENABLE ROW LEVEL SECURITY;

-- Politica RLS: anyone can read
CREATE POLICY "Anyone can read municipal_council_sessions" 
ON municipal_council_sessions 
FOR SELECT USING (true);

-- Politica RLS: anyone can insert
CREATE POLICY "Anyone can insert municipal_council_sessions" 
ON municipal_council_sessions 
FOR INSERT WITH CHECK (true);

-- Politica RLS: anyone can update
CREATE POLICY "Anyone can update municipal_council_sessions" 
ON municipal_council_sessions 
FOR UPDATE USING (true);

-- Politica RLS: anyone can delete
CREATE POLICY "Anyone can delete municipal_council_sessions" 
ON municipal_council_sessions 
FOR DELETE USING (true);

-- Crear indice para busqueda por title_session
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_title 
ON municipal_council_sessions(title_session);

-- Crear indice para busqueda por type_session
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_type 
ON municipal_council_sessions(type_session);

-- Crear indice para busqueda por status_session
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_status 
ON municipal_council_sessions(status_session);

-- Crear indice para busqueda por date_hour_start
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_date_start 
ON municipal_council_sessions(date_hour_start);

-- Crear indice para busqueda por modality
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_modality 
ON municipal_council_sessions(modality);

-- Crear indice para busqueda por id_president
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_president 
ON municipal_council_sessions(id_president);

-- Crear indice para busqueda por id_secretary
CREATE INDEX IF NOT EXISTS idx_municipal_council_sessions_secretary 
ON municipal_council_sessions(id_secretary);

-- Funcion para actualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar updated_at
CREATE TRIGGER update_municipal_council_sessions_updated_at
    BEFORE UPDATE ON municipal_council_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentacion
COMMENT ON TABLE municipal_council_sessions IS 'Tabla para almacenar las sesiones de consejo municipal';
COMMENT ON COLUMN municipal_council_sessions.title_session IS 'Titulo de la sesion';
COMMENT ON COLUMN municipal_council_sessions.type_session IS 'Tipo de sesion (Ordinaria, Extraordinaria, Especial, Instalacion)';
COMMENT ON COLUMN municipal_council_sessions.status_session IS 'Estado de la sesion (Convocada, En progreso, Realizada, Cancelada, Postergada)';
COMMENT ON COLUMN municipal_council_sessions.date_hour_start IS 'Fecha y hora de inicio de la sesion';
COMMENT ON COLUMN municipal_council_sessions.date_hour_end IS 'Fecha y hora de fin de la sesion';
COMMENT ON COLUMN municipal_council_sessions.modality IS 'Modalidad de la sesion (presencial, virtual, hibrida)';
COMMENT ON COLUMN municipal_council_sessions.place_enclosure IS 'Lugar de enclosure';
COMMENT ON COLUMN municipal_council_sessions.orden_day IS 'Orden del dia';
COMMENT ON COLUMN municipal_council_sessions.quorum_required IS 'Quorum requerido para iniciar la sesion';
COMMENT ON COLUMN municipal_council_sessions.id_president IS 'ID del presidente del consejo municipal';
COMMENT ON COLUMN municipal_council_sessions.id_secretary IS 'ID del secretario del consejo municipal';

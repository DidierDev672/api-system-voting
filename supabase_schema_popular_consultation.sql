-- Tabla de Consultas Populares
-- Nombre de la tabla: popular_consultations

CREATE TABLE IF NOT EXISTS popular_consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    questions JSONB NOT NULL DEFAULT '[]',
    proprietary_representation VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;

-- Política pública para desarrollo (ajustar para producción)
CREATE POLICY "Allow all for popular_consultations" ON popular_consultations FOR ALL USING (true) WITH CHECK (true);

-- Índices para mejorar rendimiento
CREATE INDEX idx_popular_consultations_status ON popular_consultations(status);
CREATE INDEX idx_popular_consultations_created_at ON popular_consultations(created_at DESC);

-- Ejemplo de datos de prueba
-- INSERT INTO popular_consultations (title, description, questions, proprietary_representation, status)
-- VALUES (
--     'Consulta sobre educación',
--     'Consulta popular sobre el sistema educativo',
--     '[
--         {"id": "1", "text": "¿Está de acuerdo con la educación gratuita?", "question_type": "single_choice", "options": ["Sí", "No"], "required": true},
--         {"id": "2", "text": "¿Qué nivel educativo considera más importante?", "question_type": "multiple_choice", "options": ["Primaria", "Secundaria", "Universidad"], "required": false}
--     ]'::jsonb,
--     'Representación Ciudadana',
--     'draft'
-- );

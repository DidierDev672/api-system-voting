-- =====================================================
-- SCHEMA SUPABASE - BANCADA
-- Sistema de Votación Municipal
-- =====================================================

-- Enum para tipo de curul
CREATE TYPE tipo_curul AS ENUM (
    'Ordinaria',
    'Estatuto de Oposición',
    'Reemplazo'
);

-- Enum para comisión permanente
CREATE TYPE comision_permanente AS ENUM (
    'Comisión de Presupuesto',
    'Comisión de Plan de Desarrollo',
    'Comisión de Gobierno',
    'Comisión de Hacienda',
    'Comisión de Educación',
    'Comisión de Salud',
    'Comisión de Infraestructura',
    'Comisión de Agricultura',
    'Comisión de Ambiente',
    'Comisión de Participación Ciudadana'
);

-- =====================================================
-- TABLA: bancada
-- =====================================================
CREATE TABLE bancada (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_miembro UUID NOT NULL,
    id_partido UUID NOT NULL,
    tipo_curul tipo_curul NOT NULL DEFAULT 'Ordinaria',
    fin_periodo DATE NOT NULL,
    declaraciones_bienes TEXT DEFAULT '',
    antecedentes_siri_sirus TEXT DEFAULT 'Sin antecedentes',
    comision_permanente comision_permanente DEFAULT 'Comisión de Gobierno',
    correo_institucional VARCHAR(255) NOT NULL,
    profesion VARCHAR(200) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =====================================================
-- ÍNDICES
-- =====================================================
CREATE INDEX idx_bancada_id_miembro ON bancada(id_miembro);
CREATE INDEX idx_bancada_id_partido ON bancada(id_partido);
CREATE INDEX idx_bancada_tipo_curul ON bancada(tipo_curul);
CREATE INDEX idx_bancada_comision ON bancada(comision_permanente);
CREATE INDEX idx_bancada_fin_periodo ON bancada(fin_periodo);
CREATE INDEX idx_bancada_created_at ON bancada(created_at DESC);

-- =====================================================
-- COMENTARIOS
-- =====================================================
COMMENT ON TABLE bancada IS 'Bancadas del Consejo Municipal';
COMMENT ON COLUMN bancada.id IS 'UUID único de la bancada';
COMMENT ON COLUMN bancada.id_miembro IS 'UUID del miembro del consejo';
COMMENT ON COLUMN bancada.id_partido IS 'UUID del partido político';
COMMENT ON COLUMN bancada.tipo_curul IS 'Tipo: Ordinaria, Estatuto de Oposición, Reemplazo';
COMMENT ON COLUMN bancada.fin_periodo IS 'Fecha fin del período';
COMMENT ON COLUMN bancada.declaraciones_bienes IS 'Declaración de bienes';
COMMENT ON COLUMN bancada.antecedentes_siri_sirus IS 'Verificación SIRI/SIRHUS';
COMMENT ON COLUMN bancada.comision_permanente IS 'Comisión permanente';
COMMENT ON COLUMN bancada.correo_institucional IS 'Correo institucional';
COMMENT ON COLUMN bancada.profesion IS 'Profesión del conmemral';

-- =====================================================
-- FUNCIÓN: updated_at automático
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_bancada_updated_at
    BEFORE UPDATE ON bancada
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- RLS (Desactivado para desarrollo)
-- =====================================================
ALTER TABLE bancada DISABLE ROW LEVEL SECURITY;

-- =====================================================
-- GRANT
-- =====================================================
GRANT ALL ON bancada TO anon, authenticated, service_role;

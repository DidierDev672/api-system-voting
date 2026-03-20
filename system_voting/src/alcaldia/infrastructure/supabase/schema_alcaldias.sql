-- =====================================================
-- SCHEMA SUPABASE - ALCALDIAS
-- Sistema de Votación Municipal
-- =====================================================

-- =====================================================
-- TABLA: alcaldias
-- Información básica de las alcaldías/municipios
-- =====================================================
CREATE TABLE IF NOT EXISTS public.alcaldias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre_entidad VARCHAR(255) NOT NULL,
    nit VARCHAR(50) NOT NULL UNIQUE,
    codigo_sigep VARCHAR(50) NOT NULL,
    orden_entidad VARCHAR(20) NOT NULL CHECK (orden_entidad IN ('Municipal', 'Distrital')),
    municipio VARCHAR(255) NOT NULL,
    direccion_fisica TEXT NOT NULL,
    dominio VARCHAR(255) NOT NULL,
    correo_institucional VARCHAR(255) NOT NULL,
    id_alcalde UUID NOT NULL,
    nombre_alcalde VARCHAR(255) NOT NULL,
    acto_posesion VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_alcaldias_nit ON public.alcaldias(nit);
CREATE INDEX IF NOT EXISTS idx_alcaldias_municipio ON public.alcaldias(municipio);
CREATE INDEX IF NOT EXISTS idx_alcaldias_alcalde ON public.alcaldias(id_alcalde);

-- Comentarios
COMMENT ON TABLE public.alcaldias IS 'Alcaldías y entidades territoriales del sistema de votación';
COMMENT ON COLUMN public.alcaldias.nombre_entidad IS 'Nombre completo de la entidad/alcaldía';
COMMENT ON COLUMN public.alcaldias.nit IS 'Número de Identificación Tributária';
COMMENT ON COLUMN public.alcaldias.codigo_sigep IS 'Código asignado por la Función Pública';
COMMENT ON COLUMN public.alcaldias.orden_entidad IS 'Clasificación: Municipal o Distrital';
COMMENT ON COLUMN public.alcaldias.municipio IS 'Nombre del municipio';
COMMENT ON COLUMN public.alcaldias.direccion_fisica IS 'Dirección física de la alcaldía';
COMMENT ON COLUMN public.alcaldias.dominio IS 'Dominio web de la entidad';
COMMENT ON COLUMN public.alcaldias.correo_institucional IS 'Correo electrónico institucional';
COMMENT ON COLUMN public.alcaldias.id_alcalde IS 'UUID del alcalde (FK a party_members)';
COMMENT ON COLUMN public.alcaldias.nombre_alcalde IS 'Nombre completo del alcalde';
COMMENT ON COLUMN public.alcaldias.acto_posesion IS 'Número de acta o decreto de posesión';

-- RLS (Row Level Security)
ALTER TABLE public.alcaldias DISABLE ROW LEVEL SECURITY;

-- Grants
GRANT ALL ON public.alcaldias TO anon, authenticated, service_role;

-- =====================================================
-- SCHEMA SUPABASE - ALCALDIAS
-- Sistema de Votación Municipal
-- Ejecute este SQL en el Dashboard de Supabase
-- =====================================================

-- TABLA: alcaldias
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

-- Deshabilitar RLS
ALTER TABLE public.alcaldias DISABLE ROW LEVEL SECURITY;

-- Grants
GRANT ALL ON public.alcaldias TO anon, authenticated, service_role;

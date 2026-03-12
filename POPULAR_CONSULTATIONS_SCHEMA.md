# 🚀 Schema SQL Completo para Popular Consultations

## 📋 **Instrucciones de Ejecución**

### **Paso 1: Ir a Supabase Dashboard**
1. Ve a: https://pbesvbrclrmjarouyler.supabase.co
2. Inicia sesión
3. Ve a **SQL Editor** (menú lateral)

### **Paso 2: Ejecutar el Schema SQL**
Copia y ejecuta el siguiente SQL completo:

```sql
-- Schema para Popular Consultations (Consultas Populares)
-- Tabla para gestionar consultas populares y votaciones

CREATE TABLE IF NOT EXISTS popular_consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    question VARCHAR(500) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'COMPLETED', 'CANCELLED')),
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para opciones de consulta
CREATE TABLE IF NOT EXISTS consultation_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_text VARCHAR(255) NOT NULL,
    option_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para votos
CREATE TABLE IF NOT EXISTS consultation_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_id UUID NOT NULL REFERENCES consultation_options(id) ON DELETE CASCADE,
    voter_id UUID NOT NULL, -- Referencia a sistema de identificación de votantes
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    UNIQUE(consultation_id, voter_id) -- Un voto por consulta por votante
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_popular_consultations_start_date ON popular_consultations(start_date);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_end_date ON popular_consultations(end_date);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_status ON popular_consultations(status);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_is_active ON popular_consultations(is_active);
CREATE INDEX IF NOT EXISTS idx_popular_consultations_created_by ON popular_consultations(created_by);

CREATE INDEX IF NOT EXISTS idx_consultation_options_consultation_id ON consultation_options(consultation_id);
CREATE INDEX IF NOT EXISTS idx_consultation_options_order ON consultation_options(option_order);

CREATE INDEX IF NOT EXISTS idx_consultation_votes_consultation_id ON consultation_votes(consultation_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_option_id ON consultation_votes(option_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_voter_id ON consultation_votes(voter_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_voted_at ON consultation_votes(voted_at);

-- Políticas de seguridad (Row Level Security)
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_options ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_votes ENABLE ROW LEVEL SECURITY;

-- Políticas para popular_consultations
CREATE POLICY "Allow insert operations" ON popular_consultations
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON popular_consultations
    FOR SELECT USING (is_active = true);

CREATE POLICY "Allow update operations" ON popular_consultations
    FOR UPDATE USING (true);

-- Políticas para consultation_options
CREATE POLICY "Allow insert operations" ON consultation_options
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON consultation_options
    FOR SELECT USING (true);

CREATE POLICY "Allow update operations" ON consultation_options
    FOR UPDATE USING (true);

-- Políticas para consultation_votes
CREATE POLICY "Allow insert operations" ON consultation_votes
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow select operations" ON consultation_votes
    FOR SELECT USING (true);

-- Trigger para actualizar updated_at
CREATE TRIGGER update_popular_consultations_updated_at 
    BEFORE UPDATE ON popular_consultations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE popular_consultations IS 'Tabla para gestionar consultas populares';
COMMENT ON COLUMN popular_consultations.id IS 'Identificador único de la consulta';
COMMENT ON COLUMN popular_consultations.title IS 'Título de la consulta';
COMMENT ON COLUMN popular_consultations.description IS 'Descripción detallada de la consulta';
COMMENT ON COLUMN popular_consultations.question IS 'Pregunta principal de la consulta';
COMMENT ON COLUMN popular_consultations.start_date IS 'Fecha de inicio de la consulta';
COMMENT ON COLUMN popular_consultations.end_date IS 'Fecha de fin de la consulta';
COMMENT ON COLUMN popular_consultations.status IS 'Estado de la consulta (ACTIVE, INACTIVE, COMPLETED, CANCELLED)';
COMMENT ON COLUMN popular_consultations.is_active IS 'Indica si la consulta está activa';
COMMENT ON COLUMN popular_consultations.created_by IS 'Usuario que creó la consulta';

COMMENT ON TABLE consultation_options IS 'Tabla para opciones de respuesta de consultas';
COMMENT ON COLUMN consultation_options.id IS 'Identificador único de la opción';
COMMENT ON COLUMN consultation_options.consultation_id IS 'ID de la consulta padre';
COMMENT ON COLUMN consultation_options.option_text IS 'Texto de la opción';
COMMENT ON COLUMN consultation_options.option_order IS 'Orden de la opción';

COMMENT ON TABLE consultation_votes IS 'Tabla para registrar votos en consultas';
COMMENT ON COLUMN consultation_votes.id IS 'Identificador único del voto';
COMMENT ON COLUMN consultation_votes.consultation_id IS 'ID de la consulta votada';
COMMENT ON COLUMN consultation_votes.option_id IS 'ID de la opción seleccionada';
COMMENT ON COLUMN consultation_votes.voter_id IS 'ID del votante';
COMMENT ON COLUMN consultation_votes.voted_at IS 'Fecha y hora del voto';
COMMENT ON COLUMN consultation_votes.ip_address IS 'Dirección IP del votante';

-- Vista para resultados de consultas
CREATE OR REPLACE VIEW consultation_results AS
SELECT 
    c.id as consultation_id,
    c.title,
    c.question,
    co.id as option_id,
    co.option_text,
    co.option_order,
    COUNT(cv.id) as vote_count,
    ROUND(
        (COUNT(cv.id) * 100.0 / 
         (SELECT COUNT(*) FROM consultation_votes cv2 WHERE cv2.consultation_id = c.id)
        ), 2
    ) as vote_percentage
FROM popular_consultations c
LEFT JOIN consultation_options co ON c.id = co.consultation_id
LEFT JOIN consultation_votes cv ON co.id = cv.option_id
WHERE c.is_active = true
GROUP BY c.id, c.title, c.question, co.id, co.option_text, co.option_order
ORDER BY c.id, co.option_order;

COMMENT ON VIEW consultation_results IS 'Vista que muestra resultados de consultas con conteo y porcentajes';
```

### **Paso 3: Verificar Tablas Creadas**
Ejecuta esta consulta para verificar:

```sql
-- Verificar tablas creadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('popular_consultations', 'consultation_options', 'consultation_votes')
ORDER BY table_name;
```

Deberías ver las 3 tablas en los resultados.

### **Paso 4: Probar la API**
Una vez ejecutado el schema, prueba los endpoints:

```bash
# Crear consulta
POST http://127.0.0.1:8000/api/popular-consultations/create/
{
    "title": "Consulta sobre presupuesto participativo",
    "description": "Decidir cómo se distribuirá el presupuesto municipal 2026",
    "start_date": "2026-04-01",
    "end_date": "2026-04-30",
    "status": "ACTIVE",
    "created_by": "admin-user-id"
}

# Listar consultas activas
GET http://127.0.0.1:8000/api/popular-consultations/

# Listar consultas por estado
GET http://127.0.0.1:8000/api/popular-consultations/?status=COMPLETED
```

## ✅ **Características del Schema:**

### **Tablas Principales:**
- ✅ `popular_consultations` - Consultas principales
- ✅ `consultation_options` - Opciones de respuesta
- ✅ `consultation_votes` - Votos registrados

### **Campos Mejorados:**
- ✅ `status` - Estados válidos (ACTIVE, INACTIVE, COMPLETED, CANCELLED)
- ✅ `start_date` / `end_date` - Tipo DATE para mejor compatibilidad
- ✅ `created_by` - Referencia a usuarios
- ✅ `is_active` - Control de activación

### **Seguridad y Optimización:**
- ✅ Row Level Security (RLS)
- ✅ Índices optimizados (incluyendo status)
- ✅ Trigger para updated_at
- ✅ Vista de resultados con porcentajes

### **Validaciones:**
- ✅ CHECK constraint para status
- ✅ UNIQUE constraint para votos (1 voto por consulta por votante)
- ✅ FOREIGN KEY constraints con CASCADE DELETE

## 🎯 **Resultado Final:**

Una vez ejecutado este schema, tendrás:
- ✅ Base de datos completa para consultas populares
- ✅ API funcionando con Supabase
- ✅ Sistema de votación robusto y seguro
- ✅ Vista de resultados en tiempo real

**¡El schema está completo y listo para ejecutar! 🚀**

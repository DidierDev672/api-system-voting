# 🚀 Ejecución Ordenada de Schemas Supabase

## 📋 **Orden Correcto de Ejecución**

Para evitar errores de dependencia, ejecuta los schemas en este orden:

### **Paso 1: Ejecutar Schema de Users (Primero)**
```sql
-- Copiar desde: supabase_integration/schemas/03_users.sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(10),
    document_number VARCHAR(30),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices y políticas
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow insert operations" ON users FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON users FOR SELECT USING (true);
```

### **Paso 2: Ejecutar Schema de Popular Consultations (Segundo)**
```sql
-- Ahora sí funcionará porque la tabla users existe
CREATE TABLE IF NOT EXISTS popular_consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    question VARCHAR(500) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'COMPLETED', 'CANCELLED')),
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id), -- Ahora funciona
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Resto del schema de popular_consultations...
CREATE TABLE IF NOT EXISTS consultation_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_text VARCHAR(255) NOT NULL,
    option_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultation_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultation_id UUID NOT NULL REFERENCES popular_consultations(id) ON DELETE CASCADE,
    option_id UUID NOT NULL REFERENCES consultation_options(id) ON DELETE CASCADE,
    voter_id UUID NOT NULL,
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    UNIQUE(consultation_id, voter_id)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_popular_consultations_status ON popular_consultations(status);
CREATE INDEX IF NOT EXISTS idx_consultation_options_consultation_id ON consultation_options(consultation_id);
CREATE INDEX IF NOT EXISTS idx_consultation_votes_consultation_id ON consultation_votes(consultation_id);

-- RLS
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_options ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_votes ENABLE ROW LEVEL SECURITY;

-- Políticas
CREATE POLICY "Allow insert operations" ON popular_consultations FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON popular_consultations FOR SELECT USING (true);
CREATE POLICY "Allow update operations" ON popular_consultations FOR UPDATE USING (true);

CREATE POLICY "Allow insert operations" ON consultation_options FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON consultation_options FOR SELECT USING (true);

CREATE POLICY "Allow insert operations" ON consultation_votes FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON consultation_votes FOR SELECT USING (true);
```

### **Paso 3: Ejecutar Schema de Functions and Triggers (Tercero)**
```sql
-- Copiar desde: supabase_integration/schemas/05_functions_and_triggers.sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_popular_consultations_updated_at 
    BEFORE UPDATE ON popular_consultations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 🔧 **Solución Inmediata**

Si ya ejecutaste el schema de popular_consultations con el error, haz esto:

### **Opción A: Eliminar y recrear**
```sql
-- Eliminar tablas existentes
DROP TABLE IF EXISTS consultation_votes CASCADE;
DROP TABLE IF EXISTS consultation_options CASCADE;
DROP TABLE IF EXISTS popular_consultations CASCADE;

-- Ahora ejecuta el schema completo en orden correcto
```

### **Opción B: Agregar referencia después**
```sql
-- Si la tabla users ya existe, agrega la referencia
ALTER TABLE popular_consultations 
ADD CONSTRAINT fk_popular_consultations_created_by 
FOREIGN KEY (created_by) REFERENCES users(id);
```

## ✅ **Verificación Final**

Después de ejecutar todo, verifica con:

```sql
-- Verificar todas las tablas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'popular_consultations', 'consultation_options', 'consultation_votes')
ORDER BY table_name;

-- Verificar foreign keys
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY';
```

## 🎯 **Resumen**

1. **Ejecuta users.sql primero**
2. **Luego popular_consultations.sql**
3. **Finalmente functions_and_triggers.sql**
4. **Verifica que todo esté creado correctamente**

**¡Ahora el schema funcionará sin errores! 🚀**

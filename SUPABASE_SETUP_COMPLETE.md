# 🚀 CONFIGURACIÓN COMPLETA DE SUPABASE PARA PARTY MEMBERS

## 📋 **Estado Actual:**
✅ Servidor Django funcionando en http://127.0.0.1:8000/
✅ Variables de entorno configuradas correctamente
✅ Código de API listo para usar Supabase
❌ Tablas de Supabase no existen aún

## 🔧 **PASOS PARA CONFIGURAR:**

### **Paso 1: Ir a Supabase Dashboard**
1. Abre: https://pbesvbrclrmjarouyler.supabase.co
2. Inicia sesión
3. Ve a **SQL Editor** (en el menú lateral)

### **Paso 2: Ejecutar Schema de Party Members**
Copia y pega este SQL en el editor y haz clic en **Run**:

```sql
-- Schema para Party Members
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

-- Índices
CREATE INDEX IF NOT EXISTS idx_party_members_political_party_id ON party_members(political_party_id);
CREATE INDEX IF NOT EXISTS idx_party_members_document_number ON party_members(document_number);

-- Row Level Security
ALTER TABLE party_members ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad
CREATE POLICY "Allow insert operations" ON party_members FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON party_members FOR SELECT USING (true);
CREATE POLICY "Allow update operations" ON party_members FOR UPDATE USING (true);

-- Trigger para updated_at
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
```

### **Paso 3: Ejecutar Schema de Political Parties**
```sql
-- Schema para Political Parties
CREATE TABLE IF NOT EXISTS political_parties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    acronym VARCHAR(10) NOT NULL,
    party_type VARCHAR(20) NOT NULL CHECK (party_type IN ('PARTY', 'MOVEMENT')),
    ideology VARCHAR(255),
    legal_representative VARCHAR(255),
    representative_id VARCHAR(50),
    email VARCHAR(255) UNIQUE,
    foundation_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_political_parties_name ON political_parties(name);
CREATE INDEX IF NOT EXISTS idx_political_parties_email ON political_parties(email);

-- Row Level Security
ALTER TABLE political_parties ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad
CREATE POLICY "Allow insert operations" ON political_parties FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON political_parties FOR SELECT USING (true);
CREATE POLICY "Allow update operations" ON political_parties FOR UPDATE USING (true);

-- Trigger para updated_at
CREATE TRIGGER update_political_parties_updated_at 
    BEFORE UPDATE ON political_parties 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### **Paso 4: Verificar Tablas Creadas**
En el SQL Editor, ejecuta:
```sql
-- Verificar tablas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('party_members', 'political_parties');
```

Deberías ver ambas tablas en los resultados.

## 🧪 **PASO 5: PROBAR LA API**

Una vez que las tablas existan, prueba los endpoints:

### **Registrar Miembro de Partido:**
```bash
curl -X POST http://127.0.0.1:8000/api/party-members/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Pérez García",
    "document_type": "CC",
    "document_number": "12345678",
    "birth_date": "1990-05-15",
    "city": "Bogotá",
    "political_party_id": "00000000-0000-0000-0000-000000000000",
    "consent": true,
    "data_authorization": true,
    "affiliation_date": "2026-03-09"
  }'
```

### **Listar Miembros:**
```bash
curl -X GET http://127.0.0.1:8000/api/party-members/
```

### **Registrar Partido Político:**
```bash
curl -X POST http://127.0.0.1:8000/api/political-parties/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Partido de Ejemplo",
    "acronym": "PDEJ",
    "party_type": "PARTY",
    "ideology": "Ideología de centro",
    "legal_representative": "Juan Pérez",
    "representative_id": "12345678",
    "email": "contacto@partido.com",
    "foundation_date": "2020-01-15"
  }'
```

### **Listar Partidos:**
```bash
curl -X GET http://127.0.0.1:8000/api/political-parties/
```

## ✅ **RESULTADO ESPERADO:**

Después de ejecutar los schemas SQL, deberías obtener:

- ✅ `201 Created` al registrar miembros/partidos
- ✅ `200 OK` al listar miembros/partidos
- ✅ Datos guardados en Supabase
- ✅ Respuestas JSON con los datos creados

## 🎯 **RESUMEN:**

1. **Ejecuta los 2 schemas SQL** en Supabase Dashboard
2. **Verifica que las tablas existan**
3. **Prueba los endpoints** con curl o Postman
4. **¡Listo!** Tu API estará funcionando con Supabase

🚀 **La configuración está completa y lista para usar!**

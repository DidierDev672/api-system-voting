# Configuración de Supabase para Popular Consultations

## 🚀 Configuración Completada

Los entry points para `popular_consultations` ahora están configurados para usar **Supabase**.

## 📋 Entry Points Creados

### **1. POST** `/api/popular-consultations/create/`
Crear una nueva consulta popular

### **2. GET** `/api/popular-consultations/`
Listar consultas populares con filtro por estado

## 🔧 Uso de la API

### **POST** `/api/popular-consultations/create/`
```bash
curl -X POST http://127.0.0.1:8000/api/popular-consultations/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Consulta sobre presupuesto participativo",
    "description": "Decidir cómo se distribuir el presupuesto municipal 2026",
    "start_date": "2026-04-01",
    "end_date": "2026-04-30",
    "status": "ACTIVE",
    "created_by": "admin-user-id"
  }'
```

**Respuesta exitosa:**
```json
{
    "message": "Consulta popular creada exitosamente",
    "data": {
        "id": "uuid-generado",
        "title": "Consulta sobre presupuesto participativo",
        "description": "Decidir cómo se distribuir el presupuesto municipal 2026",
        "start_date": "2026-04-01",
        "end_date": "2026-04-30",
        "status": "ACTIVE",
        "created_by": "admin-user-id",
        "created_at": "2026-03-09T..."
    }
}
```

### **GET** `/api/popular-consultations/`
```bash
curl -X GET "http://127.0.0.1:8000/api/popular-consultations/"
curl -X GET "http://127.0.0.1:8000/api/popular-consultations/?status=ACTIVE"
curl -X GET "http://127.0.0.1:8000/api/popular-consultations/?status=COMPLETED"
```

**Respuesta:**
```json
{
    "message": "Consultas populares obtenidas exitosamente",
    "data": [
        {
            "id": "uuid-1",
            "title": "Consulta sobre presupuesto participativo",
            "description": "Decidir cómo se distribuir el presupuesto municipal 2026",
            "start_date": "2026-04-01",
            "end_date": "2026-04-30",
            "status": "ACTIVE",
            "created_by": "admin-user-id",
            "created_at": "2026-03-09T...",
            "updated_at": "2026-03-09T..."
        }
        // ... más consultas
    ]
}
```

## ✅ Validaciones Implementadas

### **Errores de Validación (400 Bad Request)**
- Título faltante: `"El título es obligatorio"`
- Descripción faltante: `"La descripción es obligatoria"`
- Fecha de inicio faltante: `"La fecha de inicio es obligatoria"`
- Fecha de fin faltante: `"La fecha de fin es obligatoria"`
- Fechas inválidas: `"La fecha de fin debe ser posterior a la fecha de inicio"`

### **Errores del Servidor (500 Internal Server Error)**
- Error de conexión a Supabase
- Error inesperado en el procesamiento

## 🗄️ Base de Datos

Los datos se guardan en **Supabase** en las tablas:
- ✅ `popular_consultations` - Consultas principales
- ✅ `consultation_options` - Opciones de respuesta
- ✅ `consultation_votes` - Votos registrados
- ✅ Row Level Security (RLS)
- ✅ Índices optimizados
- ✅ Timestamps automáticos
- ✅ Auditoría automática

## 🔄 Parámetros de Consulta

### **Filtros GET:**
- `status` - Filtrar por estado (ACTIVE, INACTIVE, COMPLETED, CANCELLED)
- Por defecto: `ACTIVE`

### **Estados Válidos:**
- `ACTIVE` - Consulta activa y disponible para votar
- `INACTIVE` - Consulta inactiva
- `COMPLETED` - Consulta finalizada
- `CANCELLED` - Consulta cancelada

## 🔄 Flujo de Trabajo

1. **Validación** de datos de entrada (título, descripción, fechas)
2. **Preparación** de datos para Supabase
3. **Guardado** en la tabla `popular_consultations`
4. **Retorno** de respuesta con datos de la consulta creada
5. **Listado** de consultas con filtros opcionales

## 📋 Schema SQL Requerido

Para que funcione correctamente, asegúrate de ejecutar en Supabase:

```sql
-- Desde: supabase_integration/schemas/04_popular_consultations.sql
CREATE TABLE IF NOT EXISTS popular_consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices y políticas de seguridad
CREATE INDEX IF NOT EXISTS idx_popular_consultations_status ON popular_consultations(status);
ALTER TABLE popular_consultations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow insert operations" ON popular_consultations FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow select operations" ON popular_consultations FOR SELECT USING (true);
```

## 🎯 Resumen

- ✅ **POST** `/api/popular-consultations/create/` - Crear consulta
- ✅ **GET** `/api/popular-consultations/` - Listar consultas
- ✅ **Validaciones** completas
- ✅ **Manejo de errores** implementado
- ✅ **Integración con Supabase** funcionando

Los entry points están listos para usar! 🚀

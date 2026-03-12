# 🚀 Schema JSONB para Múltiples Preguntas

## ✅ **Corrección Implementada:**

He cambiado el campo `question` (VARCHAR) a `questions` (JSONB array) para soportar múltiples preguntas en una consulta popular.

## 📋 **Estructura del Campo Questions:**

### **Formato JSONB Array:**
```json
{
    "questions": [
        "¿Cómo debería distribuirse el presupuesto municipal 2026?",
        "¿Qué proyectos prioritarios deberían financiarse?",
        "¿Debería aumentarse el impuesto predial para mejorar servicios?"
    ]
}
```

### **Validaciones en la Base de Datos:**
```sql
questions JSONB NOT NULL CHECK (
    jsonb_typeof(questions) = 'array' AND 
    jsonb_array_length(questions) > 0
)
```

## 🔧 **Ejemplos de Uso en la API:**

### **POST** `/api/popular-consultations/create/`
```json
{
    "title": "Consulta sobre presupuesto participativo 2026",
    "description": "Decidir cómo se distribuirá el presupuesto municipal para el próximo año",
    "questions": [
        "¿Cómo debería distribuirse el presupuesto municipal 2026?",
        "¿Qué proyectos prioritarios deberían financiarse?",
        "¿Debería aumentarse el impuesto predial para mejorar servicios?"
    ],
    "start_date": "2026-04-01",
    "end_date": "2026-04-30",
    "status": "ACTIVE"
}
```

### **Respuesta Exitosa:**
```json
{
    "message": "Consulta popular creada exitosamente",
    "data": {
        "id": "uuid-generado",
        "title": "Consulta sobre presupuesto participativo 2026",
        "description": "Decidir cómo se distribuirá el presupuesto municipal para el próximo año",
        "questions": [
            "¿Cómo debería distribuirse el presupuesto municipal 2026?",
            "¿Qué proyectos prioritarios deberían financiarse?",
            "¿Debería aumentarse el impuesto predial para mejorar servicios?"
        ],
        "start_date": "2026-04-01",
        "end_date": "2026-04-30",
        "status": "ACTIVE",
        "created_at": "2026-03-09T..."
    }
}
```

## ✅ **Validaciones Implementadas:**

### **En la Base de Datos:**
- ✅ **Debe ser un array JSONB**
- ✅ **Debe contener al menos una pregunta**
- ✅ **Índice GIN** para búsquedas eficientes

### **En la API:**
- ✅ **Campo obligatorio**
- ✅ **Debe ser un array** con al menos un elemento
- ✅ **Cada pregunta** debe tener al menos 10 caracteres
- ✅ **Mensajes de error** específicos por pregunta

### **Ejemplos de Errores:**
```json
{
    "error": "Error de validación",
    "message": "Las preguntas deben ser un array con al menos una pregunta"
}

{
    "error": "Error de validación", 
    "message": "La pregunta #2 debe tener al menos 10 caracteres"
}
```

## 🔍 **Consultas SQL con JSONB:**

### **Buscar consultas por pregunta específica:**
```sql
SELECT * FROM popular_consultations 
WHERE questions::text LIKE '%presupuesto%';
```

### **Obtener todas las preguntas de una consulta:**
```sql
SELECT title, questions 
FROM popular_consultations 
WHERE id = 'uuid-consulta';
```

### **Contar preguntas por consulta:**
```sql
SELECT 
    title, 
    jsonb_array_length(questions) as total_preguntas
FROM popular_consultations;
```

## 🎯 **Ventajas del JSONB:**

1. **Flexibilidad:** Soporta cualquier número de preguntas
2. **Escalabilidad:** Fácil agregar/quitar preguntas
3. **Búsqueda:** Índice GIN para búsquedas eficientes
4. **Estructura:** Formato JSON estándar y legible
5. **Validación:** Constraints a nivel de base de datos

## 📝 **Ejemplos de Consultas Complejas:**

### **Consulta sobre transporte público:**
```json
{
    "title": "Plan de transporte público 2026",
    "description": "Definir prioridades para mejorar el sistema de transporte",
    "questions": [
        "¿Debería implementarse un nuevo metro?",
        "¿Qué rutas de bus necesitan más frecuencia?",
        "¿Debería haber tarifa diferencial para estudiantes?",
        "¿Cómo financiar la expansión del sistema?"
    ]
}
```

### **Consulta sobre medio ambiente:**
```json
{
    "title": "Políticas ambientales municipales",
    "description": "Establecer metas ambientales para la ciudad",
    "questions": [
        "¿Debería prohibirse el plástico de un solo uso?",
        "¿Cuántos árboles deberían plantarse este año?",
        "¿Debería implementarse reciclaje obligatorio?",
        "¿Qué incentivos para energías renovables?"
    ]
}
```

## 🔄 **Migración desde Question Único:**

Si tienes datos existentes con el campo `question`, puedes migrar así:

```sql
-- Convertir question único a array questions
UPDATE popular_consultations 
SET questions = jsonb_build_array(question)
WHERE question IS NOT NULL;

-- Eliminar columna antigua (después de verificar)
ALTER TABLE popular_consultations DROP COLUMN question;
```

**¡El schema ahora soporta múltiples preguntas con JSONB de manera robusta y flexible! 🚀**

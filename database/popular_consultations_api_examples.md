# Ejemplos de Consultas Populares - API REST

## 📋 **Ejemplos de Payloads para la API**

### **1. Crear Consulta Popular**

```bash
POST /api/popular-consultations/create/
Content-Type: application/json

{
    "title": "Presupuesto Participativo Municipal 2026",
    "description": "Decida cómo se distribuirán los fondos del presupuesto municipal para el año 2026. Su opinión es fundamental para priorizar las necesidades de nuestra comunidad.",
    "questions": [
        "¿En qué área debería invertirse la mayor parte del presupuesto municipal?",
        "¿Qué proyecto comunitario considera más urgente?",
        "¿Cómo deberíamos priorizar el gasto en infraestructura vs servicios sociales?"
    ],
    "start_date": "2026-04-01",
    "end_date": "2026-04-30",
    "created_by": "550e8400-e29b-41d4-a716-446655440000",
    "status": "ACTIVE"
}
```

**Response:**
```json
{
    "consultation": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Presupuesto Participativo Municipal 2026",
        "description": "Decida cómo se distribuirán los fondos del presupuesto municipal...",
        "questions": [
            "¿En qué área debería invertirse la mayor parte del presupuesto municipal?",
            "¿Qué proyecto comunitario considera más urgente?",
            "¿Cómo deberíamos priorizar el gasto en infraestructura vs servicios sociales?"
        ],
        "start_date": "2026-04-01",
        "end_date": "2026-04-30",
        "status": "ACTIVE",
        "is_active": true,
        "created_by": "550e8400-e29b-41d4-a716-446655440000",
        "created_at": "2026-03-11T22:00:00Z",
        "updated_at": "2026-03-11T22:00:00Z"
    },
    "options": []
}
```

---

### **2. Listar Consultas (con filtros)**

```bash
# Todas las consultas
GET /api/popular-consultations/

# Consultas activas
GET /api/popular-consultations/?is_active=true

# Consultas por estado
GET /api/popular-consultations/?status=ACTIVE

# Consultas activas para votación
GET /api/popular-consultations/active/
```

**Response:**
```json
{
    "consultations": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Presupuesto Participativo Municipal 2026",
            "description": "Decida cómo se distribuirán los fondos del presupuesto municipal...",
            "questions": [
                "¿En qué área debería invertirse la mayor parte del presupuesto municipal?",
                "¿Qué proyecto comunitario considera más urgente?",
                "¿Cómo deberíamos priorizar el gasto en infraestructura vs servicios sociales?"
            ],
            "start_date": "2026-04-01",
            "end_date": "2026-04-30",
            "status": "ACTIVE",
            "is_active": true,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2026-03-11T22:00:00Z",
            "updated_at": "2026-03-11T22:00:00Z"
        }
    ],
    "total": 1
}
```

---

### **3. Votar en Consulta**

```bash
POST /api/popular-consultations/vote/
Content-Type: application/json

{
    "consultation_id": "550e8400-e29b-41d4-a716-446655440000",
    "option_id": "660f9500-f29c-41d4-a716-446655440001",
    "voter_id": "770g0600-g39d-41d4-a716-446655440002",
    "ip_address": "192.168.1.100"
}
```

**Response:**
```json
{
    "vote": {
        "id": "880h1700-h49e-41d4-a716-446655440003",
        "consultation_id": "550e8400-e29b-41d4-a716-446655440000",
        "option_id": "660f9500-f29c-41d4-a716-446655440001",
        "voter_id": "770g0600-g39d-41d4-a716-446655440002",
        "voted_at": "2026-03-11T22:15:00Z"
    },
    "consultation": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Presupuesto Participativo Municipal 2026",
        "status": "ACTIVE",
        "is_active": true,
        "start_date": "2026-04-01",
        "end_date": "2026-04-30"
    }
}
```

---

### **4. Ver Resultados de Consulta**

```bash
GET /api/popular-consultations/550e8400-e29b-41d4-a716-446655440000/results/
```

**Response:**
```json
{
    "consultation_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_votes": 125,
    "results": {
        "660f9500-f29c-41d4-a716-446655440001": {
            "vote_count": 45,
            "vote_percentage": 36.0,
            "option_text": "Educación y escuelas",
            "option_order": 1
        },
        "660f9500-f29c-41d4-a716-446655440002": {
            "vote_count": 30,
            "vote_percentage": 24.0,
            "option_text": "Salud y hospitales",
            "option_order": 2
        },
        "660f9500-f29c-41d4-a716-446655440003": {
            "vote_count": 25,
            "vote_percentage": 20.0,
            "option_text": "Seguridad y policía",
            "option_order": 3
        },
        "660f9500-f29c-41d4-a716-446655440004": {
            "vote_count": 15,
            "vote_percentage": 12.0,
            "option_text": "Infraestructura vial",
            "option_order": 4
        },
        "660f9500-f29c-41d4-a716-446655440005": {
            "vote_count": 10,
            "vote_percentage": 8.0,
            "option_text": "Parques y recreación",
            "option_order": 5
        }
    }
}
```

---

## 🎯 **Casos de Error Comunes**

### **Error: Validación de fechas**
```json
{
    "error": "La fecha de fin debe ser posterior a la fecha de inicio"
}
```

### **Error: Ya votó**
```json
{
    "error": "El votante ya ha participado en esta consulta"
}
```

### **Error: Consulta no activa**
```json
{
    "error": "No se puede votar en esta consulta"
}
```

### **Error: Sin preguntas**
```json
{
    "questions": ["Debe incluir al menos una pregunta"]
}
```

---

## 🚀 **Flujo Completo de Uso**

1. **Crear consulta** → `POST /api/popular-consultations/create/`
2. **Agregar opciones** → (necesitaría endpoint adicional)
3. **Listar consultas activas** → `GET /api/popular-consultations/active/`
4. **Votar** → `POST /api/popular-consultations/vote/`
5. **Ver resultados** → `GET /api/popular-consultations/{id}/results/`

---

## 📝 **Notas Importantes**

- Los **UUIDs** deben ser válidos y únicos
- Las **fechas** deben estar en formato `YYYY-MM-DD`
- Un **votante** solo puede votar una vez por consulta
- Las consultas deben estar **ACTIVAS** y dentro del período de votación
- Los **questions** es un array JSON con al menos un elemento

# API Popular Consultation - Ejemplos de Uso con Supabase

## 📋 Descripción
La API de `popular_consultation` está completamente integrada con Supabase usando la tabla `popular_consultations`. Todos los datos se almacenan y recuperan directamente desde Supabase.

## 🔗 Endpoints Disponibles

### 1. Crear Consulta Popular
```http
POST /api/popular-consultation/create/
Content-Type: application/json
```

#### Ejemplo 1: Consulta Básica
```json
{
    "title": "¿Debería implementarse más transporte público?",
    "description": "Consulta sobre la expansión del transporte público en la ciudad",
    "questions": [
        {
            "text": "¿Apoyas la expansión del transporte público?",
            "type": "yes_no"
        }
    ],
    "status": "ACTIVE",
    "proprietary_representation": "Consejo Municipal"
}
```

#### Ejemplo 2: Consulta con Fechas
```json
{
    "title": "Presupuesto Participativo 2024",
    "description": "Votación sobre la distribución del presupuesto municipal",
    "questions": [
        {
            "text": "¿En qué área debería invertirse más presupuesto?",
            "type": "multiple_choice",
            "options": ["Educación", "Salud", "Seguridad", "Infraestructura"]
        }
    ],
    "status": "ACTIVE",
    "proprietary_representation": "Secretaría de Hacienda"
}
```

#### Ejemplo 3: Consulta Compleja
```json
{
    "title": "Plan de Desarrollo Urbano",
    "description": "Consulta sobre el futuro desarrollo urbano de la ciudad",
    "questions": [
        {
            "text": "¿Qué tipo de desarrollo prefieres para la ciudad?",
            "type": "multiple_choice",
            "options": [
                "Residencial",
                "Comercial", 
                "Industrial",
                "Mixto"
            ]
        },
        {
            "text": "¿Priorizas espacios verdes?",
            "type": "yes_no"
        }
    ],
    "status": "ACTIVE",
    "proprietary_representation": "Departamento de Urbanismo"
}
```

#### Respuesta Exitosa:
```json
{
    "message": "created"
}
```

---

### 2. Listar Todas las Consultas
```http
GET /api/popular-consultation/
```

#### Ejemplo de Respuesta:
```json
{
    "consultations": [
        {
            "id": "8116c5be-91e8-46dd-8f95-0994dd3a07ef",
            "title": "¿Debería implementarse más transporte público?",
            "description": "Consulta sobre la expansión del transporte público en la ciudad",
            "questions": [
                {
                    "text": "¿Apoyas la expansión del transporte público?",
                    "type": "yes_no"
                }
            ],
            "status": "ACTIVE",
            "proprietary_representation": "Consejo Municipal",
            "is_active": true,
            "created_by": null,
            "start_date": null,
            "end_date": null
        }
    ],
    "total": 1
}
```

---

### 3. Obtener Consulta Específica
```http
GET /api/popular-consultation/{consultation_id}/
```

#### Ejemplo:
```http
GET /api/popular-consultation/8116c5be-91e8-46dd-8f95-0994dd3a07ef/
```

#### Respuesta:
```json
{
    "id": "8116c5be-91e8-46dd-8f95-0994dd3a07ef",
    "title": "¿Debería implementarse más transporte público?",
    "description": "Consulta sobre la expansión del transporte público en la ciudad",
    "questions": [
        {
            "text": "¿Apoyas la expansión del transporte público?",
            "type": "yes_no"
        }
    ],
    "status": "ACTIVE",
    "proprietary_representation": "Consejo Municipal"
}
```

---

### 4. Actualizar Consulta
```http
PUT /api/popular-consultation/{consultation_id}/update/
Content-Type: application/json
```

#### Ejemplo:
```json
{
    "title": "¿Debería implementarse más transporte público? (Actualizada)",
    "description": "Consulta actualizada sobre la expansión del transporte público",
    "status": "INACTIVE"
}
```

---

### 5. Votar en Consulta
```http
POST /api/popular-consultation/{consultation_id}/vote/
Content-Type: application/json
```

#### Ejemplo:
```json
{
    "vote_data": {
        "question_index": 0,
        "answer": "yes",
        "voter_info": {
            "ip": "192.168.1.1"
        }
    }
}
```

#### Respuesta:
```json
{
    "message": "Voto registrado exitosamente",
    "consultation_id": "8116c5be-91e8-46dd-8f95-0994dd3a07ef",
    "vote_data": {
        "question_index": 0,
        "answer": "yes",
        "voter_info": {
            "ip": "192.168.1.1"
        }
    }
}
```

---

### 6. Ver Resultados
```http
GET /api/popular-consultation/{consultation_id}/results/
```

#### Respuesta:
```json
{
    "consultation_id": "8116c5be-91e8-46dd-8f95-0994dd3a07ef",
    "results": [
        {
            "question": "¿Apoyas la expansión del transporte público?",
            "votes": {
                "yes": 150,
                "no": 45
            },
            "total_votes": 195
        }
    ]
}
```

---

## 🛠️ Ejemplos con cURL

### Crear Consulta:
```bash
curl -X POST http://localhost:8000/api/popular-consultation/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Consulta de Prueba",
    "description": "Esta es una consulta de ejemplo",
    "questions": [
      {
        "text": "¿Te gusta esta API?",
        "type": "yes_no"
      }
    ],
    "status": "ACTIVE",
    "proprietary_representation": "Ejemplo"
  }'
```

### Listar Consultas:
```bash
curl -X GET http://localhost:8000/api/popular-consultation/
```

### Obtener Consulta Específica:
```bash
curl -X GET http://localhost:8000/api/popular-consultation/8116c5be-91e8-46dd-8f95-0994dd3a07ef/
```

---

## 📊 Campos Disponibles

### Campos Obligatorios:
- `title`: Título de la consulta (string, max 255)
- `description`: Descripción detallada (text)
- `questions`: Array de preguntas (JSON)
- `status`: Estado de la consulta (ACTIVE, INACTIVE, COMPLETED, CANCELLED)

### Campos Opcionales:
- `proprietary_representation`: Representante propietario (string)
- `start_date`: Fecha de inicio (date)
- `end_date`: Fecha de fin (date)
- `created_by`: ID del creador (UUID)

### Estructura de Questions:
```json
{
    "text": "Texto de la pregunta",
    "type": "yes_no|multiple_choice|open_text",
    "options": ["Opción 1", "Opción 2"] // Solo para multiple_choice
}
```

---

## 🔧 Configuración Técnica

### Base de Datos:
- **Tabla**: `popular_consultations` en Supabase
- **Conexión**: Automática vía variables de entorno
- **Almacenamiento**: Persistente en Supabase

### Arquitectura:
```
API Request → View → Use Case → Repository → Supabase
```

### Estados de Consulta:
- `ACTIVE`: Consulta activa y disponible para votar
- `INACTIVE`: Consulta inactiva temporalmente
- `COMPLETED`: Consulta finalizada
- `CANCELLED`: Consulta cancelada

---

## 🚀 Uso con JavaScript

### Ejemplo con Fetch API:
```javascript
// Crear consulta
const createConsultation = async () => {
    const response = await fetch('http://localhost:8000/api/popular-consultation/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: 'Consulta JavaScript',
            description: 'Creada desde JavaScript',
            questions: [
                {
                    text: '¿Funciona bien?',
                    type: 'yes_no'
                }
            ],
            status: 'ACTIVE',
            proprietary_representation: 'Frontend'
        })
    });
    
    const result = await response.json();
    console.log(result);
};

// Listar consultas
const getConsultations = async () => {
    const response = await fetch('http://localhost:8000/api/popular-consultation/');
    const data = await response.json();
    console.log(data.consultations);
};
```

---

## ✅ Verificación de Funcionamiento

Para verificar que todo funciona correctamente:

1. **Crear una consulta** → Debe retornar `{"message": "created"}`
2. **Listar consultas** → Debe mostrar la consulta creada
3. **Verificar en Supabase** → Los datos deben aparecer en la tabla `popular_consultations`

🎯 **La API está completamente operativa con Supabase!**

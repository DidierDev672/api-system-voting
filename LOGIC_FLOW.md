# 📋 Lógica para Registrar Consulta Popular - Flujo Completo

## 🔄 Flujo de Arquitectura Hexagonal

```
HTTP Request → View → Use Case → Repository → Supabase Service → Supabase DB
```

## 1️⃣ **Punto de Entrada: View (Capa de Presentación)**

### Archivo: `views.py`
```python
class CreateConsultationView(APIView):
    """View para crear una nueva consulta."""
    
    def __init__(self):
        super().__init__()
        self.repository = SupabasePopularConsultationRepository()
    
    def post(self, request):
        """Crear una nueva consulta."""
        # 1. Recibir la petición HTTP con datos JSON
        # 2. Crear instancia del caso de uso con el repositorio
        usecase = CreateConsultationUseCase(self.repository)
        
        # 3. Ejecutar el caso de uso con los datos de la petición
        usecase.execute(request.data)
        
        # 4. Retornar respuesta de éxito
        return Response({"message": "created"})
```

**¿Qué sucede aquí?**
- ✅ Recibe petición `POST /api/popular-consultation/create/`
- ✅ Extrae datos del cuerpo JSON (`request.data`)
- ✅ Inicializa el caso de uso con el repositorio inyectado
- ✅ Delega la lógica de negocio al caso de uso

---

## 2️⃣ **Lógica de Negocio: Use Case (Capa de Aplicación)**

### Archivo: `create_consultation.py`
```python
class CreateConsultationUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, consultation_data):
        # 1. Crear la entidad de dominio desde el diccionario
        consultation = PopularConsultation(
            id=uuid4(),  # Generar UUID único
            title=consultation_data.get('title', ''),
            description=consultation_data.get('description', ''),
            questions=consultation_data.get('questions', []),
            status=consultation_data.get('status', 'ACTIVE'),
            proprietary_representation=consultation_data.get('proprietary_representation', '')
        )
        
        # 2. Delegar el almacenamiento al repositorio
        return self.repository.save(consultation)
```

**¿Qué sucede aquí?**
- ✅ Recibe el diccionario de datos de la View
- ✅ Crea una entidad de dominio `PopularConsultation` con validación
- ✅ Genera UUID único para la nueva consulta
- ✅ Aplica valores por defecto si faltan campos
- ✅ Delega la persistencia al repositorio

---

## 3️⃣ **Persistencia: Repository (Capa de Infraestructura)**

### Archivo: `supabase_repository.py`
```python
class SupabasePopularConsultationRepository(PopularConsultationRepository):
    def save(self, consultation: PopularConsultation) -> PopularConsultation:
        """Guardar una consulta en Supabase"""
        try:
            # 1. Convertir entidad a diccionario para Supabase
            consultation_data = {
                'title': consultation.title,
                'description': consultation.description,
                'questions': consultation.questions,
                'status': consultation.status,
                'proprietary_representation': consultation.proprietary_representation
            }
            
            # 2. Campos opcionales
            if consultation.start_date:
                consultation_data['start_date'] = consultation.start_date
            if consultation.end_date:
                consultation_data['end_date'] = consultation.end_date
            if consultation.created_by:
                consultation_data['created_by'] = str(consultation.created_by)
            
            # 3. Usar el servicio de Supabase para guardar
            result = consultations_service.create_consultation(consultation_data)
            
            # 4. Convertir resultado a entidad y retornar
            return self._map_to_entity(result)
            
        except Exception as e:
            logger.error(f"Error saving consultation: {e}")
            raise
```

**¿Qué sucede aquí?**
- ✅ Recibe la entidad de dominio del caso de uso
- ✅ Convierte la entidad a formato compatible con Supabase
- ✅ Filtra solo los campos que existen en la tabla
- ✅ Maneja campos opcionales (fechas, created_by)
- ✅ Llama al servicio de Supabase para persistencia
- ✅ Convierte el resultado de vuelta a entidad de dominio

---

## 4️⃣ **Servicio de Base de Datos: Supabase Service**

### Archivo: `services.py`
```python
class ConsultationsService(SupabaseService):
    """Servicio para consultas populares"""
    
    def create_consultation(self, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear una nueva consulta"""
        return self.insert_record("popular_consultations", consultation_data)

class SupabaseService:
    def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insertar un registro en una tabla"""
        try:
            # 1. Ejecutar inserción en Supabase
            result = self.client.table(table).insert(data).execute()
            
            # 2. Retornar el primer registro insertado
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error insertando en {table}: {str(e)}")
            raise
```

**¿Qué sucede aquí?**
- ✅ Recibe el diccionario de datos del repositorio
- ✅ Usa el cliente de Supabase para insertar en la tabla específica
- ✅ Ejecuta la operación SQL: `INSERT INTO popular_consultations (...)`
- ✅ Maneja errores de base de datos
- ✅ Retorna el registro insertado con ID generado por Supabase

---

## 🗄️ **Entidad de Dominio**

### Archivo: `entities.py`
```python
@dataclass
class PopularConsultation:
    id: Optional[UUID] = None
    title: str = ""
    description: str = ""
    questions: List[Dict] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "ACTIVE"
    is_active: bool = True
    created_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    proprietary_representation: str = ""
    
    def __post_init__(self):
        if self.questions is None:
            self.questions = []
```

**¿Qué representa?**
- ✅ El modelo de negocio principal
- ✅ Reglas de negocio y validaciones
- ✅ Estructura de datos centralizada
- ✅ Independiente de la infraestructura

---

## 🔄 **Fluo Completo Paso a Paso**

### Petición HTTP:
```http
POST /api/popular-consultation/create/
Content-Type: application/json

{
    "title": "Consulta de Ejemplo",
    "description": "Descripción de prueba",
    "questions": [{"text": "¿Te gusta?"}],
    "status": "ACTIVE",
    "proprietary_representation": "Test"
}
```

### 1. View recibe la petición:
```python
# CreateConsultationView.post()
request.data = {
    "title": "Consulta de Ejemplo",
    "description": "Descripción de prueba",
    "questions": [{"text": "¿Te gusta?"}],
    "status": "ACTIVE",
    "proprietary_representation": "Test"
}
```

### 2. Use Case procesa:
```python
# CreateConsultationUseCase.execute()
consultation = PopularConsultation(
    id=UUID('12345678-...'),  # Nuevo UUID
    title="Consulta de Ejemplo",
    description="Descripción de prueba",
    questions=[{"text": "¿Te gusta?"}],
    status="ACTIVE",
    proprietary_representation="Test"
)
```

### 3. Repository transforma:
```python
# SupabasePopularConsultationRepository.save()
consultation_data = {
    "title": "Consulta de Ejemplo",
    "description": "Descripción de prueba", 
    "questions": [{"text": "¿Te gusta?"}],
    "status": "ACTIVE",
    "proprietary_representation": "Test"
}
```

### 4. Supabase Service ejecuta:
```sql
-- SQL generado automáticamente por Supabase
INSERT INTO popular_consultations (
    id, title, description, questions, status, proprietary_representation, created_at
) VALUES (
    gen_random_uuid(), 
    'Consulta de Ejemplo', 
    'Descripción de prueba',
    '[{"text": "¿Te gusta?"}]',
    'ACTIVE',
    'Test',
    NOW()
);
```

### 5. Respuesta HTTP:
```json
{
    "message": "created"
}
```

---

## 🎯 **Puntos Clave de la Arquitectura**

### ✅ **Separación de Responsabilidades:**
- **View**: Solo maneja HTTP y respuestas
- **Use Case**: Lógica de negocio pura
- **Repository**: Abstracción de persistencia
- **Service**: Conexión específica a Supabase

### ✅ **Inyección de Dependencias:**
```python
# View inyecta repository en use case
usecase = CreateConsultationUseCase(self.repository)

# Repository inyecta service de Supabase
result = consultations_service.create_consultation(consultation_data)
```

### ✅ **Transformación de Datos:**
- **HTTP JSON** → **Diccionario Python** (View)
- **Diccionario** → **Entidad Dominio** (Use Case)
- **Entidad** → **Diccionario Supabase** (Repository)
- **Diccionario** → **SQL** (Supabase Service)

---

## 🔧 **Manejo de Errores**

### Cada capa maneja errores apropiadamente:

```python
# View: Error HTTP 500
except Exception as e:
    return Response({'error': str(e)}, status=500)

# Use Case: Validación de datos
if not consultation_data.get('title'):
    raise ValueError("Title is required")

# Repository: Error de base de datos
except Exception as e:
    logger.error(f"Error saving consultation: {e}")
    raise

# Service: Error de Supabase
except Exception as e:
    logger.error(f"Error insertando en {table}: {str(e)}")
    raise
```

---

## 🚀 **Ventajas de este Flujo**

### ✅ **Mantenibilidad:**
- Cada capa tiene una responsabilidad única
- Fácil de modificar una capa sin afectar otras

### ✅ **Testeabilidad:**
- Se pueden mockear las dependencias
- Cada capa se puede probar independientemente

### ✅ **Flexibilidad:**
- Se puede cambiar de Supabase a otra BD fácilmente
- Se pueden agregar nuevas reglas de negocio sin tocar la infraestructura

### ✅ **Escalabilidad:**
- La arquitectura soporta crecimiento del sistema
- Separación clara permite desarrollo paralelo

---

## 📊 **Resumen del Flujo**

```
🌐 HTTP Request
    ↓
🎨 View (CreateConsultationView)
    ↓ request.data
⚙️ Use Case (CreateConsultationUseCase)
    ↓ PopularConsultation entity
💾 Repository (SupabasePopularConsultationRepository)
    ↓ consultation_data dict
🗄️ Supabase Service (ConsultationsService)
    ↓ SQL INSERT
🗃️ Supabase Database (popular_consultations table)
    ↓
📄 Response {"message": "created"}
```

**¡Este es el flujo completo para registrar una consulta popular en Supabase!** 🎯

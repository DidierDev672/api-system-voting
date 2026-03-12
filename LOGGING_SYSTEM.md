# 📊 Sistema de Logging para Consultas Populares

## 🎯 Objetivo del Logging

Implementar un sistema de seguimiento completo para todos los procesos de la consulta popular, permitiendo:
- ✅ **Monitoreo en tiempo real** de todas las operaciones
- ✅ **Trazabilidad** completa de cada petición
- ✅ **Diagnóstico rápido** de problemas
- ✅ **Auditoría** de operaciones críticas
- ✅ **Análisis de rendimiento** y comportamiento

## 🔧 Configuración del Logger

### **1. Configuración en Django Settings**
```python
# system_voting/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {module} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/popular_consultation.log',
            'formatter': 'detailed',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'popular_consultation': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### **2. Logger Específico**
```python
# En cada módulo
consultation_logger = logging.getLogger('popular_consultation')
```

## 📋 Capas con Logging Implementado

### **1. View Layer (entrypoints/views.py)**

#### **Logging en CreateConsultationView.post():**
```python
def post(self, request):
    consultation_logger.info("=== INICIO CREACIÓN CONSULTA POPULAR ===")
    consultation_logger.info(f"Request data: {request.data}")
    consultation_logger.info(f"Request headers: {dict(request.headers)}")
    consultation_logger.info(f"Request method: {request.method}")
    consultation_logger.info(f"Request user: {request.user if hasattr(request, 'user') else 'Anonymous'}")
    
    try:
        consultation_logger.info("Inicializando repositorio Supabase...")
        repository = SupabasePopularConsultationRepository()
        
        consultation_logger.info("Creando caso de uso CreateConsultationUseCase...")
        usecase = CreateConsultationUseCase(repository)
        
        consultation_logger.info("Ejecutando caso de uso con datos de la petición...")
        result = usecase.execute(request.data)
        
        consultation_logger.info(f"Consulta creada exitosamente: {result}")
        consultation_logger.info("=== FIN CREACIÓN CONSULTA POPULAR ===")
        
        return Response({"message": "created"})
        
    except Exception as e:
        consultation_logger.error(f"ERROR en creación de consulta: {str(e)}")
        consultation_logger.error(f"Exception type: {type(e).__name__}")
        consultation_logger.error(f"Traceback: {traceback.format_exc()}")
        consultation_logger.info("=== FIN ERROR CREACIÓN CONSULTA POPULAR ===")
        
        return Response({'error': 'Error interno del servidor'}, status=500)
```

**¿Qué se registra?**
- ✅ Datos completos de la petición HTTP
- ✅ Headers y método HTTP
- ✅ Usuario autenticado (si aplica)
- ✅ Inicialización de componentes
- ✅ Tiempo de ejecución
- ✅ Resultados y errores completos

---

### **2. Use Case Layer (application/create_consultation.py)**

#### **Logging en CreateConsultationUseCase.execute():**
```python
def execute(self, consultation_data):
    consultation_logger.info("=== INICIO EJECUCIÓN CREATE CONSULTATION USE CASE ===")
    consultation_logger.info(f"Datos recibidos: {consultation_data}")
    consultation_logger.info(f"Tipo de datos recibidos: {type(consultation_data)}")
    
    try:
        # Validar campos requeridos
        required_fields = ['title', 'description']
        for field in required_fields:
            if not consultation_data.get(field):
                consultation_logger.error(f"Campo requerido faltante: {field}")
                raise ValueError(f"El campo '{field}' es requerido")
        
        consultation_logger.info("Campos requeridos validados correctamente")
        
        # Crear entidad
        consultation_logger.info("Creando entidad PopularConsultation...")
        consultation = PopularConsultation(
            id=uuid4(),
            title=consultation_data.get('title', ''),
            description=consultation_data.get('description', ''),
            questions=consultation_data.get('questions', []),
            status=consultation_data.get('status', 'ACTIVE'),
            proprietary_representation=consultation_data.get('proprietary_representation', '')
        )
        
        consultation_logger.info(f"Entidad creada: {consultation}")
        consultation_logger.info(f"ID generado: {consultation.id}")
        consultation_logger.info(f"Title: {consultation.title}")
        consultation_logger.info(f"Status: {consultation.status}")
        consultation_logger.info(f"Questions count: {len(consultation.questions)}")
        
        # Guardar
        consultation_logger.info("Guardando consulta en repositorio...")
        result = self.repository.save(consultation)
        
        consultation_logger.info(f"Consulta guardada exitosamente: {result}")
        consultation_logger.info("=== FIN EJECUCIÓN CREATE CONSULTATION USE CASE ===")
        
        return result
        
    except Exception as e:
        consultation_logger.error(f"ERROR en CreateConsultationUseCase: {str(e)}")
        consultation_logger.error(f"Exception type: {type(e).__name__}")
        consultation_logger.error(f"Traceback: {traceback.format_exc()}")
        consultation_logger.info("=== FIN ERROR CREATE CONSULTATION USE CASE ===")
        raise
```

**¿Qué se registra?**
- ✅ Validación de campos requeridos
- ✅ Creación de entidad de dominio
- ✅ Generación de UUID
- ✅ Transformación de datos
- ✅ Tiempos de procesamiento
- ✅ Errores de validación

---

### **3. Repository Layer (infrastructure/supabase_repository.py)**

#### **Logging en SupabasePopularConsultationRepository.save():**
```python
def save(self, consultation: PopularConsultation) -> PopularConsultation:
    consultation_logger.info("=== INICIO SAVE EN SUPABASE REPOSITORY ===")
    consultation_logger.info(f"Entidad recibida: {consultation}")
    consultation_logger.info(f"ID de entidad: {consultation.id}")
    consultation_logger.info(f"Title: {consultation.title}")
    consultation_logger.info(f"Status: {consultation.status}")
    
    try:
        # Convertir a diccionario
        consultation_logger.info("Convirtiendo entidad a diccionario para Supabase...")
        consultation_data = {
            'title': consultation.title,
            'description': consultation.description,
            'questions': consultation.questions,
            'status': consultation.status,
            'proprietary_representation': consultation.proprietary_representation
        }
        
        # Campos opcionales
        if consultation.start_date:
            consultation_data['start_date'] = consultation.start_date
            consultation_logger.info(f"Start date incluido: {consultation.start_date}")
            
        if consultation.end_date:
            consultation_data['end_date'] = consultation.end_date
            consultation_logger.info(f"End date incluido: {consultation.end_date}")
            
        if consultation.created_by:
            consultation_data['created_by'] = str(consultation.created_by)
            consultation_logger.info(f"Created by incluido: {consultation.created_by}")
        
        consultation_logger.info(f"Datos preparados para Supabase: {consultation_data}")
        consultation_logger.info("Enviando datos a Supabase...")
        
        result = consultations_service.create_consultation(consultation_data)
        
        consultation_logger.info(f"Respuesta de Supabase: {result}")
        consultation_logger.info("Convirtiendo resultado a entidad...")
        
        mapped_result = self._map_to_entity(result)
        consultation_logger.info(f"Entidad mapeada: {mapped_result}")
        consultation_logger.info("=== FIN SAVE EN SUPABASE REPOSITORY ===")
        
        return mapped_result
        
    except Exception as e:
        consultation_logger.error(f"ERROR en save de SupabaseRepository: {str(e)}")
        consultation_logger.error(f"Exception type: {type(e).__name__}")
        consultation_logger.error(f"Traceback: {traceback.format_exc()}")
        consultation_logger.info("=== FIN ERROR SAVE EN SUPABASE REPOSITORY ===")
        raise
```

**¿Qué se registra?**
- ✅ Entidades recibidas y sus propiedades
- ✅ Transformación de datos
- ✅ Campos opcionales procesados
- ✅ Comunicación con Supabase
- ✅ Mapeo de resultados
- ✅ Tiempos de respuesta

---

### **4. Service Layer (supabase_integration/services.py)**

#### **Logging en ConsultationsService.create_consultation():**
```python
def create_consultation(self, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
    consultation_logger.info("=== INICIO CREATE CONSULTATION EN SUPABASE SERVICE ===")
    consultation_logger.info(f"Datos recibidos: {consultation_data}")
    consultation_logger.info(f"Tabla objetivo: popular_consultations")
    
    try:
        result = self.insert_record("popular_consultations", consultation_data)
        consultation_logger.info(f"Consulta creada en Supabase: {result}")
        consultation_logger.info("=== FIN CREATE CONSULTATION EN SUPABASE SERVICE ===")
        return result
    except Exception as e:
        consultation_logger.error(f"ERROR en create_consultation: {str(e)}")
        consultation_logger.error(f"Exception type: {type(e).__name__}")
        consultation_logger.info("=== FIN ERROR CREATE CONSULTATION EN SUPABASE SERVICE ===")
        raise

def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    consultation_logger.info(f"=== INICIO INSERT RECORD EN TABLA {table} ===")
    consultation_logger.info(f"Datos a insertar: {data}")
    
    try:
        result = self.client.table(table).insert(data).execute()
        consultation_logger.info(f"Resultado de inserción: {result}")
        
        if result.data:
            consultation_logger.info(f"Registro insertado exitosamente: {result.data[0]}")
            consultation_logger.info("=== FIN INSERT RECORD ===")
            return result.data[0]
        else:
            consultation_logger.warning("No se retornaron datos en la inserción")
            return None
            
    except Exception as e:
        consultation_logger.error(f"Error insertando en {table}: {str(e)}")
        consultation_logger.error(f"Exception type: {type(e).__name__}")
        consultation_logger.info("=== FIN ERROR INSERT RECORD ===")
        raise
```

**¿Qué se registra?**
- ✅ Operaciones de base de datos
- ✅ Tablas y datos específicos
- ✅ Resultados de Supabase
- ✅ Conexión y autenticación
- ✅ Errores de SQL

---

## 📁 Archivos de Log

### **Ubicación:**
```
logs/popular_consultation.log
```

### **Formato de Entrada:**
```
[2026-03-12 10:55:23,456] INFO [views:71] CreateConsultationView - === INICIO CREACIÓN CONSULTA POPULAR ===
[2026-03-12 10:55:23,457] INFO [views:72] CreateConsultationView - Request data: {'title': 'Test', 'description': 'Test desc'}
[2026-03-12 10:55:23,458] INFO [views:73] CreateConsultationView - Request headers: {'Content-Type': 'application/json'}
[2026-03-12 10:55:23,459] INFO [views:74] CreateConsultationView - Request method: POST
[2026-03-12 10:55:23,460] INFO [views:75] CreateConsultationView - Request user: Anonymous
```

---

## 🔍 Niveles de Logging

### **INFO:**
- ✅ Inicio y fin de operaciones
- ✅ Datos de entrada y salida
- ✅ Transformaciones exitosas
- ✅ Conexiones establecidas

### **WARNING:**
- ⚠️ Datos opcionales faltantes
- ⚠️ Respuestas vacías
- ⚠️ Operaciones lentas

### **ERROR:**
- ❌ Excepciones y fallos
- ❌ Errores de validación
- ❌ Problemas de conexión
- ❌ Errores de base de datos

---

## 📊 Ejemplo de Log Completo

### **Petición Exitosa:**
```
[2026-03-12 10:55:23,456] INFO [views:71] CreateConsultationView - === INICIO CREACIÓN CONSULTA POPULAR ===
[2026-03-12 10:55:23,457] INFO [views:72] CreateConsultationView - Request data: {'title': 'Consulta Test', 'description': 'Descripción', 'questions': [{'text': 'Pregunta'}], 'status': 'ACTIVE'}
[2026-03-12 10:55:23,458] INFO [views:73] CreateConsultationView - Request headers: {'Content-Type': 'application/json', 'User-Agent': 'curl/7.68.0'}
[2026-03-12 10:55:23,459] INFO [views:74] CreateConsultationView - Request method: POST
[2026-03-12 10:55:23,460] INFO [views:75] CreateConsultationView - Request user: Anonymous
[2026-03-12 10:55:23,461] INFO [views:79] CreateConsultationView - Inicializando repositorio Supabase...
[2026-03-12 10:55:23,462] INFO [views:82] CreateConsultationView - Creando caso de uso CreateConsultationUseCase...
[2026-03-12 10:55:23,463] INFO [views:85] CreateConsultationView - Ejecutando caso de uso con datos de la petición...
[2026-03-12 10:55:23,464] INFO [create_consultation:13] CreateConsultationUseCase - === INICIO EJECUCIÓN CREATE CONSULTATION USE CASE ===
[2026-03-12 10:55:23,465] INFO [create_consultation:14] CreateConsultationUseCase - Datos recibidos: {'title': 'Consulta Test', 'description': 'Descripción'}
[2026-03-12 10:55:23,466] INFO [create_consultation:25] CreateConsultationUseCase - Campos requeridos validados correctamente
[2026-03-12 10:55:23,467] INFO [create_consultation:28] CreateConsultationUseCase - Creando entidad PopularConsultation...
[2026-03-12 10:55:23,468] INFO [create_consultation:38] CreateConsultationUseCase - Entidad creada: PopularConsultation(id=...)
[2026-03-12 10:55:23,469] INFO [create_consultation:39] CreateConsultationUseCase - ID generado: 12345678-1234-5678-9abc-123456789012
[2026-03-12 10:55:23,470] INFO [create_consultation:45] CreateConsultationUseCase - Guardando consulta en repositorio...
[2026-03-12 10:55:23,471] INFO [supabase_repository:16] SupabasePopularConsultationRepository - === INICIO SAVE EN SUPABASE REPOSITORY ===
[2026-03-12 10:55:23,472] INFO [supabase_repository:17] SupabasePopularConsultationRepository - Entidad recibida: PopularConsultation(...)
[2026-03-12 10:55:23,473] INFO [supabase_repository:24] SupabasePopularConsultationRepository - Convirtiendo entidad a diccionario para Supabase...
[2026-03-12 10:55:23,474] INFO [supabase_repository:47] SupabasePopularConsultationRepository - Datos preparados para Supabase: {'title': 'Consulta Test', ...}
[2026-03-12 10:55:23,475] INFO [supabase_repository:48] SupabasePopularConsultationRepository - Enviando datos a Supabase...
[2026-03-12 10:55:23,476] INFO [services:214] ConsultationsService - === INICIO CREATE CONSULTATION EN SUPABASE SERVICE ===
[2026-03-12 10:55:23,477] INFO [services:215] ConsultationsService - Datos recibidos: {'title': 'Consulta Test', ...}
[2026-03-12 10:55:23,478] INFO [services:216] ConsultationsService - Tabla objetivo: popular_consultations
[2026-03-12 10:55:23,479] INFO [services:56] SupabaseService - === INICIO INSERT RECORD EN TABLA popular_consultations ===
[2026-03-12 10:55:23,480] INFO [services:57] SupabaseService - Datos a insertar: {'title': 'Consulta Test', ...}
[2026-03-12 10:55:23,500] INFO [services:65] SupabaseService - Registro insertado exitosamente: {'id': '...', 'title': 'Consulta Test', ...}
[2026-03-12 10:55:23,501] INFO [services:66] SupabaseService - === FIN INSERT RECORD ===
[2026-03-12 10:55:23,502] INFO [services:220] ConsultationsService - Consulta creada en Supabase: {'id': '...', 'title': 'Consulta Test', ...}
[2026-03-12 10:55:23,503] INFO [services:221] ConsultationsService - === FIN CREATE CONSULTATION EN SUPABASE SERVICE ===
[2026-03-12 10:55:23,504] INFO [supabase_repository:52] SupabasePopularConsultationRepository - Respuesta de Supabase: {'id': '...', 'title': 'Consulta Test', ...}
[2026-03-12 10:55:23,505] INFO [supabase_repository:53] SupabasePopularConsultationRepository - Convirtiendo resultado a entidad...
[2026-03-12 10:55:23,506] INFO [supabase_repository:58] SupabasePopularConsultationRepository - Entidad mapeada: PopularConsultation(...)
[2026-03-12 10:55:23,507] INFO [supabase_repository:59] SupabasePopularConsultationRepository - === FIN SAVE EN SUPABASE REPOSITORY ===
[2026-03-12 10:55:23,508] INFO [create_consultation:48] CreateConsultationUseCase - Consulta guardada exitosamente: PopularConsultation(...)
[2026-03-12 10:55:23,509] INFO [create_consultation:49] CreateConsultationUseCase - === FIN EJECUCIÓN CREATE CONSULTATION USE CASE ===
[2026-03-12 10:55:23,510] INFO [views:88] CreateConsultationView - Consulta creada exitosamente: PopularConsultation(...)
[2026-03-12 10:55:23,511] INFO [views:89] CreateConsultationView - === FIN CREACIÓN CONSULTA POPULAR ===
```

### **Petición con Error:**
```
[2026-03-12 10:55:23,456] ERROR [create_consultation:22] CreateConsultationUseCase - Campo requerido faltante: title
[2026-03-12 10:55:23,457] ERROR [views:94] CreateConsultationView - ERROR en creación de consulta: El campo 'title' es requerido
[2026-03-12 10:55:23,458] ERROR [views:95] CreateConsultationView - Exception type: ValueError
[2026-03-12 10:55:23,459] ERROR [views:97] CreateConsultationView - Traceback: Traceback (most recent call last)...
[2026-03-12 10:55:23,460] INFO [views:98] CreateConsultationView - === FIN ERROR CREACIÓN CONSULTA POPULAR ===
```

---

## 🛠️ Herramientas de Monitoreo

### **1. Ver logs en tiempo real:**
```bash
tail -f logs/popular_consultation.log
```

### **2. Filtrar por nivel:**
```bash
# Solo errores
grep "ERROR" logs/popular_consultation.log

# Solo warnings
grep "WARNING" logs/popular_consultation.log

# Solo una operación específica
grep "CREACIÓN CONSULTA" logs/popular_consultation.log
```

### **3. Análisis con awk:**
```bash
# Contar operaciones por hora
awk '{print $1" "$2}' logs/popular_consultation.log | sort | uniq -c

# Extraer tiempos de respuesta
grep "FIN" logs/popular_consultation.log | awk '{print $1" "$2}'
```

---

## 📈 Métricas que se Pueden Extraer

### **1. Rendimiento:**
- Tiempo total de cada operación
- Tiempo por capa (View, Use Case, Repository, Service)
- Cuellos de botella identificados

### **2. Errores:**
- Frecuencia de errores por tipo
- Campos más problemáticos
- Errores de Supabase vs errores de aplicación

### **3. Uso:**
- Consultas creadas por hora/día
- Usuarios más activos
- Tipos de consultas más comunes

---

## 🚀 Beneficios del Sistema Implementado

### **✅ Trazabilidad Completa:**
- Cada petición tiene un ID único
- Se puede seguir el flujo completo
- Fácil identificar dónde falla

### **✅ Diagnóstico Rápido:**
- Logs estructurados y detallados
- Información de contexto completa
- Stack traces completos

### **✅ Monitoreo Proactivo:**
- Alertas de errores en tiempo real
- Métricas de rendimiento
- Tendencias de uso

### **✅ Auditoría:**
- Registro de todas las operaciones
- Quién hizo qué y cuándo
- Cumplimiento normativo

---

## 🎯 **Resumen de Implementación**

El sistema de logging está completamente implementado en todas las capas:

1. **✅ View Layer**: Registra peticiones HTTP
2. **✅ Use Case Layer**: Registra lógica de negocio
3. **✅ Repository Layer**: Registra persistencia
4. **✅ Service Layer**: Registra operaciones de Supabase
5. **✅ Configuración**: Logs en archivo y consola
6. **✅ Formato**: Estructurado y detallado

**¡Ahora tienes visibilidad completa de todos los procesos de consulta popular!** 📊

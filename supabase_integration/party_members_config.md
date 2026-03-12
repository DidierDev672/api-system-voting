# Configuración de Supabase para Party Members

## 🚀 Configuración Completada

El entry point `/api/party-members/register/` ahora está configurado para usar **Supabase** en lugar de la base de datos local.

## 📋 Cambios Realizados

### 1. **Vista Actualizada** (`views.py`)
- ✅ Se eliminaron dependencias de Django Repository
- ✅ Se agregó importación de `PartyMemberValidator`
- ✅ Se agregó importación de `PartyMember` entidad
- ✅ Se agregó importación de `party_members_service` (Supabase)

### 2. **Método POST** - Registrar Miembro de Partido
```python
def post(self, request):
    try:
        # Validar datos de entrada
        PartyMemberValidator.validate(request.data)
        
        # Crear entidad PartyMember
        member = PartyMember(**request.data)
        
        # Preparar datos para Supabase
        member_data = {
            "full_name": member.full_name,
            "document_type": member.document_type,
            "document_number": member.document_number,
            "birth_date": member.birth_date,
            "city": member.city,
            "political_party_id": member.political_party_id,
            "consent": member.consent,
            "data_authorization": member.data_authorization,
            "affiliation_date": member.affiliation_date
        }
        
        # Guardar en Supabase
        result = party_members_service.create_member(member_data)
        
        return Response({ 
            "message": "Afiliación registrada exitosamente",
            "data": result
        }, status=status.HTTP_201_CREATED)
```

### 3. **Método GET** - Listar Miembros de Partido
```python
def get(self, request):
    try:
        # Obtener miembros activos desde Supabase
        members = party_members_service.get_all_active_members()
        
        return Response({
            "message": "Miembros de partido obtenidos exitosamente",
            "data": members
        }, status=status.HTTP_200_OK)
```

## 🔧 Uso de la API

### **POST** `/api/party-members/register/`
```bash
curl -X POST http://127.0.0.1:8000/api/party-members/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Pérez García",
    "document_type": "CC",
    "document_number": "12345678",
    "birth_date": "1990-05-15",
    "city": "Bogotá",
    "political_party_id": "uuid-del-partido",
    "consent": true,
    "data_authorization": true,
    "affiliation_date": "2026-03-09"
  }'
```

**Respuesta exitosa:**
```json
{
    "message": "Afiliación registrada exitosamente",
    "data": {
        "id": "uuid-generado",
        "full_name": "Juan Pérez García",
        "document_type": "CC",
        "document_number": "12345678",
        "birth_date": "1990-05-15",
        "city": "Bogotá",
        "political_party_id": "uuid-del-partido",
        "consent": true,
        "data_authorization": true,
        "affiliation_date": "2026-03-09",
        "created_at": "2026-03-09T..."
    }
}
```

### **GET** `/api/party-members/`
```bash
curl -X GET http://127.0.0.1:8000/api/party-members/
```

**Respuesta:**
```json
{
    "message": "Miembros de partido obtenidos exitosamente",
    "data": [
        {
            "id": "uuid-1",
            "full_name": "Juan Pérez García",
            "document_type": "CC",
            "document_number": "12345678",
            "birth_date": "1990-05-15",
            "city": "Bogotá",
            "political_party_id": "uuid-partido",
            "consent": true,
            "data_authorization": true,
            "affiliation_date": "2026-03-09",
            "created_at": "2026-03-09T..."
        }
        // ... más miembros
    ]
}
```

## ✅ Validaciones Implementadas

### **Errores de Validación (400 Bad Request)**
- Documento duplicado: `"Ya existe un miembro con este número de documento"`
- Partido político inválido: `"El partido político especificado no existe"`
- Tipo de documento inválido: `"Tipo de documento no válido"`
- Consentimiento falso: `"El consentimiento es obligatorio"`
- Autorización de datos falso: `"La autorización de datos es obligatoria"`

### **Errores del Servidor (500 Internal Server Error)**
- Error de conexión a Supabase
- Error inesperado en el procesamiento

## 🗄️ Base de Datos

Los datos ahora se guardan en **Supabase** en la tabla `party_members` con:
- ✅ Row Level Security (RLS)
- ✅ Índices optimizados
- ✅ Auditoría automática
- ✅ Timestamps automáticos
- ✅ Validaciones de integridad
- ✅ Relación con `political_parties`

## 🔄 Flujo de Trabajo

1. **Validación** de datos de entrada usando `PartyMemberValidator`
2. **Creación** de entidad `PartyMember`
3. **Preparación** de datos para Supabase
4. **Guardado** en la tabla `party_members`
5. **Retorno** de respuesta con datos del miembro creado

## 🔄 Próximos Pasos

1. **Ejecutar schemas SQL** en Supabase
2. **Probar endpoints** con diferentes datos
3. **Implementar autenticación** con Supabase Auth
4. **Agregar endpoints** para actualizar/eliminar miembros
5. **Configurar webhooks** para sincronización

La API está lista para usar con Supabase! 🎉

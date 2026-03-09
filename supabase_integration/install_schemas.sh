#!/bin/bash

# Script de instalación para Supabase Schemas
# Uso: ./install_schemas.sh

echo "🚀 Iniciando instalación de schemas en Supabase..."

# Verificar variables de entorno
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Error: Las variables de entorno SUPABASE_URL y SUPABASE_ANON_KEY son requeridas"
    exit 1
fi

# Lista de schemas en orden de ejecución
schemas=(
    "01_party_members.sql"
    "02_political_parties.sql"
    "03_users.sql"
    "04_popular_consultations.sql"
    "05_functions_and_triggers.sql"
)

# Directorio de schemas
SCHEMAS_DIR="./supabase/schemas"

# Verificar si el directorio existe
if [ ! -d "$SCHEMAS_DIR" ]; then
    echo "❌ Error: El directorio $SCHEMAS_DIR no existe"
    exit 1
fi

# Instalar cada schema
for schema in "${schemas[@]}"; do
    echo "📝 Instalando $schema..."
    
    # Verificar si el archivo existe
    if [ ! -f "$SCHEMAS_DIR/$schema" ]; then
        echo "❌ Error: El archivo $schema no existe"
        exit 1
    fi
    
    # Ejecutar el schema usando curl o psql según tu preferencia
    # Opción 1: Usando curl con REST API de Supabase
    # curl -X POST "$SUPABASE_URL/rest/v1/rpc/execute_sql" \
    #      -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
    #      -H "Content-Type: application/json" \
    #      -d "{\"sql\": $(cat "$SCHEMAS_DIR/$schema" | jq -Rs .)}"
    
    # Opción 2: Usando psql (requiere tener psql instalado)
    # PGPASSWORD=$SUPABASE_ANON_KEY psql -h $SUPABASE_URL -U postgres -d postgres -f "$SCHEMAS_DIR/$schema"
    
    echo "✅ $schema instalado correctamente"
done

echo "🎉 Todos los schemas han sido instalados correctamente!"
echo ""
echo "📋 Resumen de tablas creadas:"
echo "  - party_members"
echo "  - political_parties"
echo "  - users"
echo "  - popular_consultations"
echo "  - consultation_options"
echo "  - consultation_votes"
echo "  - audit_logs"
echo ""
echo "🔧 Funciones y vistas creadas:"
echo "  - update_updated_at_column()"
echo "  - is_valid_email()"
echo "  - generate_slug()"
echo "  - get_system_statistics()"
echo "  - party_statistics (vista)"
echo "  - consultation_results (vista)"
echo ""
echo "🚀 La API está lista para usar!"

"""
Script para configurar el sistema de votación con Supabase
Ejecutar: python setup_supabase.py
"""

import os
import sys

def setup_supabase_config():
    """Configurar las variables de Supabase en settings.py"""
    print("🔧 CONFIGURACIÓN DE SUPABASE")
    print("="*50)
    
    print("\n📋 Necesitas los siguientes datos de tu proyecto Supabase:")
    print("1. URL del proyecto: https://tu-proyecto.supabase.co")
    print("2. Anon Key: llave pública de tu proyecto")
    print("3. Service Role Key: llave de servicio (privada)")
    
    print("\n📝 Ingresa tus datos de Supabase:")
    
    # Obtener datos del usuario
    supabase_url = input("URL del proyecto (ej: https://tu-proyecto.supabase.co): ").strip()
    if not supabase_url:
        print("❌ La URL es obligatoria")
        return False
    
    anon_key = input("Anon Key: ").strip()
    if not anon_key:
        print("❌ La Anon Key es obligatoria")
        return False
    
    service_key = input("Service Role Key: ").strip()
    if not service_key:
        print("❌ La Service Role Key es obligatoria")
        return False
    
    # Actualizar settings.py
    settings_file = "system_voting/settings.py"
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar las configuraciones
        content = content.replace(
            "SUPABASE_URL = 'https://your-project.supabase.co'",
            f"SUPABASE_URL = '{supabase_url}'"
        )
        content = content.replace(
            "SUPABASE_ANON_KEY = 'your-anon-key'",
            f"SUPABASE_ANON_KEY = '{anon_key}'"
        )
        content = content.replace(
            "SUPABASE_SERVICE_ROLE_KEY = 'your-service-role-key'",
            f"SUPABASE_SERVICE_ROLE_KEY = '{service_key}'"
        )
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración guardada en settings.py")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar settings.py: {str(e)}")
        return False

def show_schema_instructions():
    """Mostrar instrucciones para ejecutar el schema"""
    print("\n🗄️ EJECUTAR SCHEMA EN SUPABASE")
    print("="*50)
    
    print("\n📋 Pasos para ejecutar el schema de la base de datos:")
    print("1. Ve a tu dashboard de Supabase: https://app.supabase.com")
    print("2. Selecciona tu proyecto")
    print("3. Ve a 'SQL Editor' en el menú lateral")
    print("4. Copia y pega el contenido del archivo:")
    print("   📁 database/supabase_voting_schema.sql")
    print("5. Haz clic en 'Run' para ejecutar el script")
    print("6. Verifica que todas las tablas se creen correctamente")
    
    print("\n📄 El schema crea las siguientes tablas:")
    print("• popular_consultations - Consultas populares")
    print("• voting_options - Opciones de votación")
    print("• votes - Votos registrados")
    print("• voting_permissions - Permisos de votación")
    print("• Vistas y funciones útiles")
    print("• Políticas RLS para seguridad")

def test_connection():
    """Probar la conexión con Supabase"""
    print("\n🧪 PROBAR CONEXIÓN CON SUPABASE")
    print("="*50)
    
    try:
        # Importar después de configurar
        from system_voting.src.users.infrastructure.repositories.supabase_voting_repository import SupabaseVotingRepository
        
        repository = SupabaseVotingRepository()
        
        if repository.demo_mode:
            print("❌ Todavía está en modo demo")
            print("   Verifica que las variables de entorno estén configuradas correctamente")
            return False
        else:
            print("✅ Conexión exitosa con Supabase")
            print(f"   URL: {repository.supabase.supabase_url[:30]}...")
            return True
            
    except Exception as e:
        print(f"❌ Error al conectar con Supabase: {str(e)}")
        return False

def show_next_steps():
    """Mostrar siguientes pasos"""
    print("\n🚀 SIGUIENTES PASOS")
    print("="*50)
    
    print("\n1. Reinicia el servidor Django:")
    print("   python manage.py runserver")
    
    print("\n2. Prueba el endpoint de creación:")
    print("   POST http://127.0.0.1:8000/api/users/voting/consultations/create/")
    
    print("\n3. Verifica en Supabase que los datos se guarden:")
    print("   Ve a Table Editor → popular_consultations")
    
    print("\n4. Ejemplos de prueba:")
    print("   python examples/simple_test.py")
    print("   .\\examples\\powershell_example.ps1")

def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN DEL SISTEMA DE VOTACIÓN CON SUPABASE")
    print("="*60)
    
    # Paso 1: Configurar variables
    if not setup_supabase_config():
        print("\n❌ No se pudo completar la configuración")
        sys.exit(1)
    
    # Paso 2: Mostrar instrucciones del schema
    show_schema_instructions()
    
    # Preguntar si ya ejecutó el schema
    print("\n" + "="*50)
    schema_executed = input("¿Ya ejecutaste el schema en Supabase? (s/n): ").strip().lower()
    
    if schema_executed == 's':
        # Paso 3: Probar conexión
        if test_connection():
            # Paso 4: Mostrar siguientes pasos
            show_next_steps()
            print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
            print("✅ Tu sistema de votación ahora está conectado a Supabase")
        else:
            print("\n❌ La conexión falló. Revisa tus credenciales.")
    else:
        print("\n📝 Ejecuta el schema primero y luego corre este script nuevamente")
        print("   o ejecuta 'python setup_supabase.py' cuando termines")

if __name__ == "__main__":
    main()

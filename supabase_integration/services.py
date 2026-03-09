"""
Configuración de Supabase para la API REST
Este módulo proporciona utilidades y configuración para interactuar con Supabase
"""

import os
from supabase import create_client
from django.conf import settings
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Clase de configuración para Supabase"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self._client = None
    
    @property
    def client(self):
        """Obtener cliente de Supabase (lazy initialization)"""
        if self._client is None:
            if not self.url or not self.anon_key:
                raise ValueError("SUPABASE_URL y SUPABASE_ANON_KEY son requeridos")
            self._client = create_client(self.url, self.anon_key)
        return self._client
    
    @property
    def admin_client(self):
        """Obtener cliente con permisos de administrador"""
        if not self.service_role_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY es requerido para operaciones de administrador")
        return create_client(self.url, self.service_role_key)

# Instancia global de configuración
supabase_config = SupabaseConfig()

class SupabaseService:
    """Servicio para operaciones comunes con Supabase"""
    
    def __init__(self, client=None):
        self.client = client or supabase_config.client
    
    def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insertar un registro en una tabla"""
        try:
            result = self.client.table(table).insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error insertando en {table}: {str(e)}")
            raise
    
    def get_all_records(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Obtener todos los registros de una tabla con filtros opcionales"""
        try:
            query = self.client.table(table).select("*")
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo registros de {table}: {str(e)}")
            raise
    
    def get_record_by_id(self, table: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Obtener un registro por ID"""
        try:
            result = self.client.table(table).select("*").eq("id", record_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error obteniendo registro {record_id} de {table}: {str(e)}")
            raise
    
    def update_record(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar un registro"""
        try:
            result = self.client.table(table).update(data).eq("id", record_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error actualizando registro {record_id} en {table}: {str(e)}")
            raise
    
    def delete_record(self, table: str, record_id: str) -> bool:
        """Eliminar un registro"""
        try:
            result = self.client.table(table).delete().eq("id", record_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error eliminando registro {record_id} de {table}: {str(e)}")
            raise
    
    def execute_rpc(self, function_name: str, params: Dict[str, Any] = None) -> Any:
        """Ejecutar una función RPC de Supabase"""
        try:
            result = self.client.rpc(function_name, params or {}).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error ejecutando RPC {function_name}: {str(e)}")
            raise

# Servicios específicos para cada entidad
class PartyMembersService(SupabaseService):
    """Servicio para miembros de partidos"""
    
    def create_member(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo miembro de partido"""
        return self.insert_record("party_members", member_data)
    
    def get_members_by_party(self, party_id: str) -> List[Dict[str, Any]]:
        """Obtener miembros por partido político"""
        return self.get_all_records("party_members", {"political_party_id": party_id})
    
    def get_member_by_document(self, document_number: str) -> Optional[Dict[str, Any]]:
        """Obtener miembro por número de documento"""
        records = self.get_all_records("party_members", {"document_number": document_number})
        return records[0] if records else None

class PoliticalPartiesService(SupabaseService):
    """Servicio para partidos políticos"""
    
    def create_party(self, party_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo partido político"""
        return self.insert_record("political_parties", party_data)
    
    def get_all_active_parties(self) -> List[Dict[str, Any]]:
        """Obtener todos los partidos activos"""
        return self.get_all_records("political_parties", {"is_active": True})
    
    def get_party_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtener partido por nombre"""
        records = self.get_all_records("political_parties", {"name": name})
        return records[0] if records else None
    
    def get_party_statistics(self) -> List[Dict[str, Any]]:
        """Obtener estadísticas de partidos"""
        try:
            result = self.client.table("party_statistics").select("*").execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de partidos: {str(e)}")
            raise

class UsersService(SupabaseService):
    """Servicio para usuarios"""
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo usuario"""
        return self.insert_record("users", user_data)
    
    def get_active_users(self) -> List[Dict[str, Any]]:
        """Obtener usuarios activos"""
        return self.get_all_records("users", {"is_active": True})
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por email"""
        records = self.get_all_records("users", {"email": email})
        return records[0] if records else None

class ConsultationsService(SupabaseService):
    """Servicio para consultas populares"""
    
    def create_consultation(self, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear una nueva consulta"""
        return self.insert_record("popular_consultations", consultation_data)
    
    def add_consultation_option(self, option_data: Dict[str, Any]) -> Dict[str, Any]:
        """Agregar una opción a una consulta"""
        return self.insert_record("consultation_options", option_data)
    
    def vote_in_consultation(self, vote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registrar un voto en una consulta"""
        return self.insert_record("consultation_votes", vote_data)
    
    def get_consultation_results(self, consultation_id: str) -> List[Dict[str, Any]]:
        """Obtener resultados de una consulta"""
        return self.get_all_records("consultation_results", {"consultation_id": consultation_id})
    
    def get_active_consultations(self) -> List[Dict[str, Any]]:
        """Obtener consultas activas"""
        # Obtener consultas donde la fecha actual está entre start_date y end_date
        try:
            result = self.client.table("popular_consultations").select("*")\
                .eq("is_active", True)\
                .lte("start_date", "now()")\
                .gte("end_date", "now()")\
                .execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo consultas activas: {str(e)}")
            raise

# Instancias globales de servicios
party_members_service = PartyMembersService()
political_parties_service = PoliticalPartiesService()
users_service = UsersService()
consultations_service = ConsultationsService()

def get_system_statistics() -> Dict[str, Any]:
    """Obtener estadísticas generales del sistema"""
    try:
        return supabase_config.client.rpc("get_system_statistics").execute().data
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas del sistema: {str(e)}")
        raise

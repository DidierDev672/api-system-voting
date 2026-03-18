"""
Configuración de Supabase para la API REST
Este módulo proporciona utilidades y configuración para interactuar con Supabase
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from django.conf import settings
from typing import Dict, Any, Optional, List
import logging

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)
consultation_logger = logging.getLogger("popular_consultation")


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
            raise ValueError(
                "SUPABASE_SERVICE_ROLE_KEY es requerido para operaciones de administrador"
            )
        return create_client(self.url, self.service_role_key)


# Instancia global de configuración
supabase_config = SupabaseConfig()


class SupabaseService:
    """Servicio para operaciones comunes con Supabase"""

    def __init__(self, client=None):
        self.client = client or supabase_config.client
        consultation_logger = logging.getLogger("popular_consultation")
        consultation_logger.info("SupabaseService inicializado")

    def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insertar un registro en una tabla"""
        consultation_logger = logging.getLogger("popular_consultation")
        consultation_logger.info(f"=== INICIO INSERT RECORD EN TABLA {table} ===")
        consultation_logger.info(f"Datos a insertar: {data}")

        try:
            result = self.client.table(table).insert(data).execute()
            consultation_logger.info(f"Resultado de inserción: {result}")

            if result.data:
                consultation_logger.info(
                    f"Registro insertado exitosamente: {result.data[0]}"
                )
                consultation_logger.info("=== FIN INSERT RECORD ===")
                return result.data[0]
            else:
                consultation_logger.warning("No se retornaron datos en la inserción")
                consultation_logger.info("=== FIN INSERT RECORD SIN DATOS ===")
                return None

        except Exception as e:
            consultation_logger.error(f"Error insertando en {table}: {str(e)}")
            consultation_logger.error(f"Exception type: {type(e).__name__}")
            consultation_logger.info("=== FIN ERROR INSERT RECORD ===")
            raise

    def get_all_records(
        self, table: str, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
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

    def update_record(
        self, table: str, record_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Actualizar un registro"""
        try:
            result = self.client.table(table).update(data).eq("id", record_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(
                f"Error actualizando registro {record_id} en {table}: {str(e)}"
            )
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

    def get_all_members(self) -> List[Dict[str, Any]]:
        """Obtener todos los miembros de partido"""
        return self.get_all_records("party_members", {})

    def get_all_active_members(self) -> List[Dict[str, Any]]:
        """Obtener todos los miembros activos"""
        try:
            return self.get_all_records("party_members", {"is_active": True})
        except Exception:
            # Si la columna is_active no existe, devolver todos
            return self.get_all_records("party_members", {})

    def get_members_by_party(self, party_id: str) -> List[Dict[str, Any]]:
        """Obtener miembros por partido político"""
        return self.get_all_records("party_members", {"political_party_id": party_id})

    def get_member_by_document(self, document_number: str) -> Optional[Dict[str, Any]]:
        """Obtener miembro por número de documento"""
        records = self.get_all_records(
            "party_members", {"document_number": document_number}
        )
        return records[0] if records else None


class PoliticalPartiesService(SupabaseService):
    """Servicio para partidos políticos"""

    def create_party(self, party_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo partido político"""
        return self.insert_record("political_parties", party_data)

    def get_all_active_parties(self) -> List[Dict[str, Any]]:
        """Obtener todos los partidos activos"""
        try:
            return self.get_all_records("political_parties", {"is_active": True})
        except Exception:
            # Si la columna is_active no existe, devolver todos
            return self.get_all_records("political_parties", {})

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

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por ID"""
        records = self.get_all_records("users", {"id": user_id})
        return records[0] if records else None

    def get_user_by_auth_id(self, auth_id: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por auth_id de Supabase"""
        records = self.get_all_records("users", {"auth_id": auth_id})
        return records[0] if records else None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por email"""
        records = self.get_all_records("users", {"email": email})
        return records[0] if records else None

    def get_user_by_document(
        self, document_type: str, document_number: str
    ) -> Optional[Dict[str, Any]]:
        """Obtener usuario por documento"""
        records = self.get_all_records(
            "users",
            {"document_type": document_type, "document_number": document_number},
        )
        return records[0] if records else None

    def get_all_users(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios"""
        filters = {"is_active": True} if active_only else {}
        return self.get_all_records("users", filters)

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar un usuario"""
        return self.update_record("users", user_id, user_data)

    def update_user_by_auth_id(
        self, auth_id: str, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Actualizar usuario por auth_id"""
        user = self.get_user_by_auth_id(auth_id)
        if not user:
            raise ValueError(f"Usuario con auth_id {auth_id} no encontrado")
        return self.update_record("users", user["id"], user_data)

    def delete_user(self, user_id: str) -> bool:
        """Eliminar usuario (soft delete)"""
        return self.update_record("users", user_id, {"is_active": False})

    def search_users(
        self, search_term: str = None, role_filter: str = None, active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Buscar usuarios con filtros"""
        try:
            # Usar la función de búsqueda personalizada
            query = self.client.rpc(
                "search_users",
                {
                    "search_term": search_term,
                    "role_filter": role_filter,
                    "active_only": active_only,
                },
            )
            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Error searching users: {e}")
            return []


class ConsultationsService(SupabaseService):
    """Servicio para consultas populares usando tabla popular_consultations"""

    def __init__(self, client=None):
        super().__init__(client)
        consultation_logger.info(
            "ConsultationsService inicializado para tabla popular_consultations"
        )

    def create_consultation(self, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear una nueva consulta en tabla popular_consultations"""
        consultation_logger.info(
            "=== INICIO CREATE CONSULTATION EN TABLA POPULAR_CONSULTATIONS ==="
        )
        consultation_logger.info(f"Datos recibidos: {consultation_data}")
        consultation_logger.info(f"Tabla objetivo: popular_consultations")

        try:
            result = self.insert_record("popular_consultations", consultation_data)
            consultation_logger.info(f"Consulta creada en Supabase: {result}")
            consultation_logger.info(
                "=== FIN CREATE CONSULTATION EN TABLA POPULAR_CONSULTATIONS ==="
            )
            return result
        except Exception as e:
            consultation_logger.error(f"ERROR en create_consultation: {str(e)}")
            consultation_logger.error(f"Exception type: {type(e).__name__}")
            consultation_logger.info(
                "=== FIN ERROR CREATE CONSULTATION EN TABLA POPULAR_CONSULTATIONS ==="
            )
            raise

    def get_all_consultations(self) -> List[Dict[str, Any]]:
        """Obtener todas las consultas de popular_consultations"""
        consultation_logger.info(
            "=== INICIO GET ALL CONSULTATIONS DE POPULAR_CONSULTATIONS ==="
        )

        try:
            result = self.get_all_records("popular_consultations")
            consultation_logger.info(
                f"Consultas obtenidas: {len(result) if result else 0}"
            )
            consultation_logger.info(
                "=== FIN GET ALL CONSULTATIONS DE POPULAR_CONSULTATIONS ==="
            )
            return result or []
        except Exception as e:
            consultation_logger.error(f"ERROR en get_all_consultations: {str(e)}")
            consultation_logger.info(
                "=== FIN ERROR GET ALL CONSULTATIONS DE POPULAR_CONSULTATIONS ==="
            )
            return []

    def get_consultation_by_id(self, consultation_id: str) -> Optional[Dict[str, Any]]:
        """Obtener consulta por ID de popular_consultations"""
        consultation_logger.info(
            f"=== INICIO GET BY ID DE POPULAR_CONSULTATIONS: {consultation_id} ==="
        )

        try:
            result = self.get_record_by_id("popular_consultations", consultation_id)
            consultation_logger.info(f"Consulta encontrada: {result}")
            consultation_logger.info("=== FIN GET BY ID DE POPULAR_CONSULTATIONS ===")
            return result
        except Exception as e:
            consultation_logger.error(f"ERROR en get_consultation_by_id: {str(e)}")
            consultation_logger.info(
                "=== FIN ERROR GET BY ID DE POPULAR_CONSULTATIONS ==="
            )
            return None

    def update_consultation(
        self, consultation_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Actualizar consulta en popular_consultations"""
        consultation_logger.info(
            f"=== INICIO UPDATE DE POPULAR_CONSULTATIONS: {consultation_id} ==="
        )
        consultation_logger.info(f"Datos de actualización: {data}")

        try:
            result = self.update_record("popular_consultations", consultation_id, data)
            consultation_logger.info(f"Consulta actualizada: {result}")
            consultation_logger.info("=== FIN UPDATE DE POPULAR_CONSULTATIONS ===")
            return result
        except Exception as e:
            consultation_logger.error(f"ERROR en update_consultation: {str(e)}")
            consultation_logger.info(
                "=== FIN ERROR UPDATE DE POPULAR_CONSULTATIONS ==="
            )
            return None

    def delete_consultation(self, consultation_id: str) -> bool:
        """Eliminar consulta de popular_consultations"""
        consultation_logger.info(
            f"=== INICIO DELETE DE POPULAR_CONSULTATIONS: {consultation_id} ==="
        )

        try:
            result = self.delete_record("popular_consultations", consultation_id)
            consultation_logger.info(f"Resultado eliminación: {result}")
            consultation_logger.info("=== FIN DELETE DE POPULAR_CONSULTATIONS ===")
            return result
        except Exception as e:
            consultation_logger.error(f"ERROR en delete_consultation: {str(e)}")
            consultation_logger.info(
                "=== FIN ERROR DELETE DE POPULAR_CONSULTATIONS ==="
            )
            return False


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

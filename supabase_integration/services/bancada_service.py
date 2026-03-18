from supabase import create_client, Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BancadaSupabaseService:
    """Servicio para interactuar con la tabla bancada en Supabase"""

    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_SERVICE_ROLE_KEY
        self.client: Client = None

    def get_client(self) -> Client:
        """Obtener cliente de Supabase (lazy initialization)"""
        if self.client is None:
            self.client = create_client(self.url, self.key)
        return self.client

    def create_record(self, data: dict) -> dict:
        """Crear un nuevo registro de bancada"""
        try:
            client = self.get_client()
            response = client.table("bancada").insert(data).execute()
            if response.data:
                return response.data[0]
            raise Exception("No se recibió respuesta al insertar")
        except Exception as e:
            logger.error(f"Error creando bancada en Supabase: {str(e)}")
            raise

    def get_all_records(self) -> list:
        """Obtener todos los registros de bancada"""
        try:
            client = self.get_client()
            response = client.table("bancada").select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error obteniendo bancadas de Supabase: {str(e)}")
            raise

    def get_record_by_id(self, record_id: str) -> dict:
        """Obtener un registro de bancada por ID"""
        try:
            client = self.get_client()
            response = client.table("bancada").select("*").eq("id", record_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error obteniendo bancada {record_id}: {str(e)}")
            raise

    def get_by_miembro(self, id_miembro: str) -> list:
        """Obtener bancadas por ID de miembro"""
        try:
            client = self.get_client()
            response = (
                client.table("bancada")
                .select("*")
                .eq("id_miembro", id_miembro)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(
                f"Error obteniendo bancadas por miembro {id_miembro}: {str(e)}"
            )
            raise

    def get_by_partido(self, id_partido: str) -> list:
        """Obtener bancadas por ID de partido"""
        try:
            client = self.get_client()
            response = (
                client.table("bancada")
                .select("*")
                .eq("id_partido", id_partido)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(
                f"Error obteniendo bancadas por partido {id_partido}: {str(e)}"
            )
            raise

    def update_record(self, record_id: str, data: dict) -> dict:
        """Actualizar un registro de bancada"""
        try:
            client = self.get_client()
            response = (
                client.table("bancada").update(data).eq("id", record_id).execute()
            )
            if response.data:
                return response.data[0]
            raise Exception(f"Bancada {record_id} no encontrada")
        except Exception as e:
            logger.error(f"Error actualizando bancada {record_id}: {str(e)}")
            raise

    def delete_record(self, record_id: str) -> bool:
        """Eliminar un registro de bancada"""
        try:
            client = self.get_client()
            client.table("bancada").delete().eq("id", record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error eliminando bancada {record_id}: {str(e)}")
            raise


_bancada_service = None


def get_bancada_service() -> BancadaSupabaseService:
    """Obtener instancia singleton del servicio"""
    global _bancada_service
    if _bancada_service is None:
        _bancada_service = BancadaSupabaseService()
    return _bancada_service

"""
Puerto del Repositorio para Consulta Popular
Arquitectura Hexagonal - Define la interfaz que debe implementar el adapter
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.popular_consultation.domain.entities.consultation import (
    PopularConsultation,
)


class ConsultationRepositoryPort(ABC):
    """Puerto abstracto para el repositorio de consultas populares"""

    @abstractmethod
    def save(self, consultation: PopularConsultation) -> PopularConsultation:
        """Crear una nueva consulta popular"""
        pass

    @abstractmethod
    def get_by_id(self, consultation_id: str) -> Optional[PopularConsultation]:
        """Obtener consulta por ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[PopularConsultation]:
        """Obtener todas las consultas"""
        pass

    @abstractmethod
    def update(self, consultation: PopularConsultation) -> PopularConsultation:
        """Actualizar una consulta"""
        pass

    @abstractmethod
    def delete(self, consultation_id: str) -> bool:
        """Eliminar una consulta"""
        pass

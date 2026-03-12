"""
Caso de Uso para Registrar Voto - Aplicación
Vertical Slicing + Hexagonal Architecture
"""

import logging
from typing import Dict, Any
from system_voting.src.voting.domain.entities.vote import Vote, CreateVoteCommand
from system_voting.src.voting.domain.ports.vote_repository import VoteRepositoryPort

logger = logging.getLogger(__name__)


class RegisterVoteUseCase:
    """Caso de uso para registrar un voto en una consulta popular"""

    def __init__(self, vote_repository: VoteRepositoryPort):
        self.vote_repository = vote_repository

    def execute(self, command: CreateVoteCommand) -> Dict[str, Any]:
        """Ejecutar el caso de uso de registrar voto"""
        logger.info(
            f"=== USECASE: Registrando voto para consulta {command.id_consult} ==="
        )

        # Validar que el miembro no haya votado previamente
        if self.vote_repository.exists_by_member_and_consult(
            command.id_member, command.id_consult
        ):
            logger.warning(
                f"=== USECASE: Miembro {command.id_member} ya votó en consulta {command.id_consult} ==="
            )
            raise ValueError("El miembro ya ha emitido su voto en esta consulta")

        # Crear la entidad de voto
        vote = Vote(
            id_consult=command.id_consult,
            id_member=command.id_member,
            id_party=command.id_party,
            id_auth=command.id_auth,
            value_vote=command.value_vote,
            comment=command.comment,
        )

        # Persistir el voto
        saved_vote = self.vote_repository.save(vote)

        logger.info(f"=== USECASE: Voto registrado exitosamente: {saved_vote.id} ===")

        return {
            "success": True,
            "vote": saved_vote,
            "message": "Voto registrado exitosamente",
        }


class GetVotesByConsultationUseCase:
    """Caso de uso para obtener votos de una consulta"""

    def __init__(self, vote_repository: VoteRepositoryPort):
        self.vote_repository = vote_repository

    def execute(self, id_consult: str) -> Dict[str, Any]:
        """Obtener todos los votos de una consulta"""
        logger.info(f"=== USECASE: Obteniendo votos para consulta {id_consult} ===")

        votes = self.vote_repository.find_by_consultation(id_consult)

        logger.info(f"=== USECASE: {len(votes)} votos encontrados ===")

        return {"success": True, "votes": votes, "count": len(votes)}


class GetVotesByMemberUseCase:
    """Caso de uso para obtener votos de un miembro"""

    def __init__(self, vote_repository: VoteRepositoryPort):
        self.vote_repository = vote_repository

    def execute(self, id_member: str) -> Dict[str, Any]:
        """Obtener todos los votos de un miembro"""
        logger.info(f"=== USECASE: Obteniendo votos para miembro {id_member} ===")

        votes = self.vote_repository.find_by_member(id_member)

        logger.info(f"=== USECASE: {len(votes)} votos encontrados ===")

        return {"success": True, "votes": votes, "count": len(votes)}

from typing import Optional, List
from system_voting.src.users.domain.entities.user import User, CreateUserCommand, UpdateUserCommand
from system_voting.src.users.domain.repositories.user_repository import UserRepository
import bcrypt


class UserService:
    """Servicio de Aplicación - Casos de Uso (Hexagonal)"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, command: CreateUserCommand) -> User:
        """Caso de uso: Crear nuevo usuario"""
        # Validaciones de negocio
        if self.user_repository.get_by_email(command.email):
            raise ValueError("El correo electrónico ya está registrado")
        
        if self.user_repository.get_by_document(command.document_type, command.document_number):
            raise ValueError("El número de documento ya está registrado")
        
        # Crear entidad de dominio
        user = User(
            full_name=command.full_name,
            document_type=command.document_type,
            document_number=command.document_number,
            email=command.email,
            password=self._hash_password(command.password) if command.password else None,
            phone=command.phone,
            role=command.role
        )
        
        # Guardar mediante el puerto
        return self.user_repository.save(user)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Caso de uso: Obtener usuario por ID"""
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Caso de uso: Obtener usuario por email"""
        return self.user_repository.get_by_email(email)
    
    def get_users(self, active_only: bool = True) -> List[User]:
        """Caso de uso: Obtener todos los usuarios"""
        return self.user_repository.get_all(active_only)
    
    def update_user(self, command: UpdateUserCommand) -> User:
        """Caso de uso: Actualizar usuario"""
        user = self.user_repository.get_by_id(command.id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Actualizar campos si se proporcionan
        if command.full_name:
            user.full_name = command.full_name
        if command.phone:
            user.phone = command.phone
        if command.email:
            # Verificar que el nuevo email no exista
            existing_user = self.user_repository.get_by_email(command.email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("El correo electrónico ya está registrado")
            user.email = command.email
        
        return self.user_repository.update(user)
    
    def delete_user(self, user_id: str) -> bool:
        """Caso de uso: Eliminar usuario (soft delete)"""
        return self.user_repository.delete(user_id)
    
    def _hash_password(self, password: str) -> str:
        """Método privado para hashear contraseñas"""
        if not password:
            return ""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, user: User, password: str) -> bool:
        """Verificar contraseña"""
        if not user.password or not password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

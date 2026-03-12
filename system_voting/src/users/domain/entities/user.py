from typing import Optional
from dataclasses import dataclass


@dataclass
class User:
    """Entidad de Usuario - Dominio Puro (Vertical Slicing + Hexagonal)"""

    id: Optional[str] = None
    auth_id: Optional[str] = None  # ID de Supabase Auth
    full_name: str = ""
    document_type: str = ""
    document_number: str = ""
    email: str = ""
    password: Optional[str] = None
    phone: Optional[str] = None
    role: str = "CITIZEN"
    is_active: bool = True

    def __post_init__(self):
        """Validaciones de dominio - Lógica de negocio pura"""
        if not self.full_name or len(self.full_name.strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")

        if not self.document_type:
            raise ValueError("El tipo de documento es obligatorio")

        if not self.document_number or len(self.document_number.strip()) < 5:
            raise ValueError("El número de documento debe tener al menos 5 caracteres")

        # if not self.email or "@" not in self.email:
        #     raise ValueError("El correo electrónico no es válido")

        if self.phone and len(self.phone.strip()) < 7:
            raise ValueError("El teléfono debe tener al menos 7 dígitos")


@dataclass
class CreateUserCommand:
    """Comando para crear un usuario - Application Layer (Hexagonal)"""

    full_name: str
    document_type: str
    document_number: str
    email: str
    password: Optional[str] = None
    phone: Optional[str] = None
    role: str = "CITIZEN"


@dataclass
class CompleteUserProfileCommand:
    """Comando para completar perfil de usuario después de registro en Supabase Auth"""

    auth_id: str
    full_name: str
    document_type: str
    document_number: str
    phone: str


@dataclass
class UpdateUserCommand:
    """Comando para actualizar un usuario - Application Layer"""

    id: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

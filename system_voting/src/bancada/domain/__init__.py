# Domain Layer - Expose entities and ports
from .entities import Bancada
from .ports import BancadaRepositoryInterface
from .value_objects import TipoCurul, ComisionPermanente

__all__ = [
    "Bancada",
    "BancadaRepositoryInterface",
    "TipoCurul",
    "ComisionPermanente",
]

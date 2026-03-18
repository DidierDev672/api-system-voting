"""
Supabase integration services package
"""

from supabase_integration.services.bancada_service import (
    BancadaSupabaseService,
    get_bancada_service,
)

__all__ = [
    "BancadaSupabaseService",
    "get_bancada_service",
]

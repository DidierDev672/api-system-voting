"""
Domain Entities - Screening
Vertical Slicing + SOLID Principles
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ScreeningOption:
    id: str
    text: str
    value: int  # 1 = correct, 0 = incorrect


@dataclass
class ScreeningQuestion:
    sound: str  # Sound ID or URL
    optionsAnswer: List[ScreeningOption]


@dataclass
class Screening:
    id: str
    title: str
    description: str
    questions: List[ScreeningQuestion]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateScreeningDTO:
    title: str
    description: str
    questions: List[dict]  # List of {sound, optionsAnswer: [{id, text, value}]}

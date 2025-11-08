from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Provider(SQLModel, table=True):
    """Database model for NGO providers."""
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_name: str = Field(index=True)
    provider_identifier_abn: Optional[str] = None
    delivery_area: Optional[str] = None
    local_government_area: Optional[str] = None
    local_health_district: Optional[str] = Field(index=True)
    target_group: Optional[str] = None
    classification: Optional[str] = None
    gender: Optional[str] = None
    indigenous_status: Optional[str] = None
    commissioning_agency: Optional[str] = Field(index=True)
    program_name: Optional[str] = None
    agreement_identifier: Optional[str] = None
    agreement_start_date: Optional[str] = None
    agreement_end_date: Optional[str] = None


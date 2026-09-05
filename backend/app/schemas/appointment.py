from datetime import datetime

from pydantic import BaseModel, Field


class AvailabilityRequest(BaseModel):
    start: datetime
    end: datetime


class AvailabilityResponse(BaseModel):
    available: bool


class BookingRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=7, max_length=30)
    start: datetime
    end: datetime
    call_id: str = Field(min_length=1, max_length=200)


class BookingResponse(BaseModel):
    success: bool
    appointment_id: str | None = None
    message: str
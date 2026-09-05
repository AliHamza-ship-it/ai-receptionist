from fastapi import APIRouter, HTTPException

from app.schemas.appointment import (
    AvailabilityRequest,
    AvailabilityResponse,
    BookingRequest,
    BookingResponse,
)
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/api/v1")
service = AppointmentService()


@router.post(
    "/availability",
    response_model=AvailabilityResponse,
)
async def check_availability(request: AvailabilityRequest):
    try:
        available = service.check_availability(
            request.start,
            request.end,
        )
        return {"available": available}

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/appointments",
    response_model=BookingResponse,
)
async def book_appointment(request: BookingRequest):
    try:
        appointment = service.book(
            request.name,
            request.phone,
            request.start,
            request.end,
            request.call_id,
        )

        if not appointment:
            return BookingResponse(
                success=False,
                message="The requested time is no longer available.",
            )

        return BookingResponse(
            success=True,
            appointment_id=appointment["id"],
            message="Appointment booked successfully.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
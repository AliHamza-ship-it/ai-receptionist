import json

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.security import verify_retell_request
from app.schemas.appointment import (
    AvailabilityRequest,
    BookingRequest,
)
from app.services.appointment_service import AppointmentService


router = APIRouter(prefix="/api/v1")

appointment_service = AppointmentService()


@router.post("/tools/check_availability")
async def check_availability(
    request: Request,
    _: bytes = Depends(verify_retell_request),
):
    try:
        payload = json.loads((await request.body()).decode("utf-8"))
        args = payload.get("args", payload)

        request_data = AvailabilityRequest.model_validate(args)

        available = appointment_service.is_available(
            request_data.start,
            request_data.end,
        )

        return {
            "available": available,
            "message": (
                "The requested appointment time is available."
                if available
                else "The requested appointment time is not available."
            ),
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/tools/book_appointment")
async def book_appointment(
    request: Request,
    _: bytes = Depends(verify_retell_request),
):
    try:
        payload = json.loads((await request.body()).decode("utf-8"))

        args = payload.get("args", payload)
        call = payload.get("call", {})

        call_id = call.get("call_id")

        if not call_id:
            raise HTTPException(
                status_code=400,
                detail="Missing Retell call ID.",
            )

        booking_data = BookingRequest(
            name=args["name"],
            phone=args["phone"],
            start=args["start"],
            end=args["end"],
            call_id=call_id,
        )

        result = appointment_service.book(
            booking_data
        )

        return result

    except KeyError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field: {exc.args[0]}",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
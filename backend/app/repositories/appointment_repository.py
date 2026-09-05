from datetime import datetime

from app.integrations.supabase import get_supabase


class AppointmentRepository:

    def has_conflict(
        self,
        start: datetime,
        end: datetime,
    ) -> bool:
        db = get_supabase()

        result = (
            db.table("appointments")
            .select("id")
            .eq("status", "booked")
            .lt("appointment_start", end.isoformat())
            .gt("appointment_end", start.isoformat())
            .limit(1)
            .execute()
        )

        return bool(result.data)

    def create(
        self,
        customer_id: str,
        start: datetime,
        end: datetime,
        call_id: str,
    ):
        db = get_supabase()

        return (
            db.table("appointments")
            .insert({
                "customer_id": customer_id,
                "appointment_start": start.isoformat(),
                "appointment_end": end.isoformat(),
                "status": "booked",
                "call_id": call_id,
            })
            .execute()
        )
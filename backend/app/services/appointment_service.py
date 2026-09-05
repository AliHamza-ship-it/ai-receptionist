from datetime import datetime, timezone

from app.integrations.supabase import get_supabase
from app.repositories.appointment_repository import AppointmentRepository


class AppointmentService:

    def __init__(self):
        self.repository = AppointmentRepository()

    def check_availability(
        self,
        start: datetime,
        end: datetime,
    ) -> bool:
        self._validate_time(start, end)
        return not self.repository.has_conflict(start, end)

    def book(
        self,
        name: str,
        phone: str,
        start: datetime,
        end: datetime,
        call_id: str,
    ):
        self._validate_time(start, end)

        if self.repository.has_conflict(start, end):
            return None

        db = get_supabase()

        customer = (
            db.table("customers")
            .select("id")
            .eq("phone", phone)
            .limit(1)
            .execute()
        )

        if customer.data:
            customer_id = customer.data[0]["id"]
        else:
            result = (
                db.table("customers")
                .insert({
                    "name": name,
                    "phone": phone,
                })
                .execute()
            )
            customer_id = result.data[0]["id"]

        result = self.repository.create(
            customer_id,
            start,
            end,
            call_id,
        )

        return result.data[0] if result.data else None

    @staticmethod
    def _validate_time(start: datetime, end: datetime):
        if end <= start:
            raise ValueError("Appointment end must be after start.")

        now = datetime.now(timezone.utc)

        if start.astimezone(timezone.utc) <= now:
            raise ValueError("Appointment must be in the future.")
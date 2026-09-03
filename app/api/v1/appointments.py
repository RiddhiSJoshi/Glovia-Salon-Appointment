from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies import (
    get_current_user,
    get_salon_owner,
)

from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentReschedule,
)

from app.services.appointment_service import AppointmentService


router = APIRouter(
    tags=["Appointments"],
)


# ============================================================
# CREATE APPOINTMENT
# ============================================================

@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    data: AppointmentCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Customer creates an appointment.

    Backend MUST re-check availability before creating
    the appointment.
    """

    try:
        service = AppointmentService(db)

        appointment = await service.create_appointment(
            customer_id=current_user.id,
            data=data,
        )

        return appointment

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create this appointment.",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create appointment.",
        )


# ============================================================
# CUSTOMER APPOINTMENTS
# ============================================================

@router.get(
    "/my",
    response_model=list[AppointmentResponse],
    status_code=status.HTTP_200_OK,
)
async def get_my_appointments(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        return await service.get_customer_appointments(
            customer_id=current_user.id
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to retrieve appointments.",
    )

# ============================================================
# GET APPOINTMENT
# ============================================================

@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_appointment(
    appointment_id: int = Path(..., gt=0),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        appointment = await service.get_appointment(
            appointment_id=appointment_id,
            user_id=current_user.id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found.",
            )

        return appointment

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this appointment.",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve appointment.",
        )


# ============================================================
# CANCEL APPOINTMENT
# ============================================================

@router.put(
    "/{appointment_id}/cancel",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def cancel_appointment(
    appointment_id: int = Path(..., gt=0),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        appointment = await service.cancel_appointment(
            appointment_id=appointment_id,
            user_id=current_user.id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found.",
            )

        return appointment

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to cancel this appointment.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel appointment.",
        )


# ============================================================
# RESCHEDULE APPOINTMENT
# ============================================================

@router.patch(
    "/{appointment_id}/reschedule",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def reschedule_appointment(
    data: AppointmentReschedule,
    appointment_id: int = Path(..., gt=0),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        appointment = await service.reschedule_appointment(
            appointment_id=appointment_id,
            user_id=current_user.id,
            data=data,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found.",
            )

        return appointment

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to reschedule this appointment.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reschedule appointment.",
        )

# ============================================================
# SALON APPOINTMENTS
# ============================================================

@router.get(
    "/salons/{salon_id}/appointments",
    response_model=list[AppointmentResponse],
    status_code=status.HTTP_200_OK,
)
async def get_salon_appointments(
    salon_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        return await service.get_salon_appointments(
            salon_id=salon_id,
            owner_id=current_user.id,
        )

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view these appointments.",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve salon appointments.",
        )


# ============================================================
# CONFIRM APPOINTMENT
# ============================================================

@router.patch(
    "/salons/{salon_id}/appointments/{appointment_id}/confirm",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def confirm_appointment(
    salon_id: int = Path(..., gt=0),
    appointment_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        appointment = await service.confirm_appointment(
            salon_id=salon_id,
            appointment_id=appointment_id,
            owner_id=current_user.id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found.",
            )

        return appointment

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to confirm this appointment.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to confirm appointment.",
        )


# ============================================================
# REJECT APPOINTMENT
# ============================================================

@router.patch(
    "/salons/{salon_id}/appointments/{appointment_id}/reject",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def reject_appointment(
    salon_id: int = Path(..., gt=0),
    appointment_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        appointment = await service.reject_appointment(
            salon_id=salon_id,
            appointment_id=appointment_id,
            owner_id=current_user.id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found.",
            )

        return appointment

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to reject this appointment.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject appointment.",
        )


# ============================================================
# COMPLETE APPOINTMENT
# ============================================================

@router.put(
    "/salons/{salon_id}/appointments/{appointment_id}/complete",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def complete_appointment(
    salon_id: int = Path(..., gt=0),
    appointment_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AppointmentService(db)

        appointment = await service.complete_appointment(
            salon_id=salon_id,
            appointment_id=appointment_id,
            owner_id=current_user.id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found.",
            )

        return appointment

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to complete this appointment.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete appointment.",
        )
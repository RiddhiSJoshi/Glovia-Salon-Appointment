from datetime import datetime, time, date
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint

)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Salon(Base):
    __tablename__ = "salons"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    address: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    pincode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    categories = relationship(
        "Category",
        back_populates="salon",
        cascade="all, delete-orphan",
    )

    services = relationship(
        "Service",
        back_populates="salon",
        cascade="all, delete-orphan",
    )

    staff = relationship(
        "Staff",
        back_populates="salon",
        cascade="all, delete-orphan",
    )

    working_hours = relationship(
        "WorkingHour",
        back_populates="salon",
        cascade="all, delete-orphan",
    )

    appointments = relationship(
        "Appointment",
        back_populates="salon",
        cascade="all, delete-orphan",
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    salon = relationship(
        "Salon",
        back_populates="categories",
    )

    services = relationship(
        "Service",
        back_populates="category",
    )


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    salon = relationship(
        "Salon",
        back_populates="services",
    )

    category = relationship(
        "Category",
        back_populates="services",
    )

    appointments = relationship(
        "Appointment",
        back_populates="service",
    )


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    specialization: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    salon = relationship(
        "Salon",
        back_populates="staff",
    )

    appointments = relationship(
        "Appointment",
        back_populates="staff",
    )


class WorkingHour(Base):
    __tablename__ = "working_hours"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(
        nullable=False,
    )

    opening_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    closing_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_closed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    salon = relationship(
        "Salon",
        back_populates="working_hours",
    )


class StaffLeave(Base):
    __tablename__ = "staff_leaves"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    leave_date: Mapped[date] = mapped_column(
        DateTime,
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )


class Appointment(Base):
    __tablename__ = "appointments"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "salon_id",
            name="uq_review_customer_salon",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.id"),
        nullable=False,
        index=True,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        default=AppointmentStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="appointments",
    )

    salon = relationship(
        "Salon",
        foreign_keys=[salon_id],
        back_populates="appointments",
    )

    staff = relationship(
        "Staff",
        foreign_keys=[staff_id],
        back_populates="appointments",
    )

    service = relationship(
        "Service",
        foreign_keys=[service_id],
        back_populates="appointments",
    )

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )
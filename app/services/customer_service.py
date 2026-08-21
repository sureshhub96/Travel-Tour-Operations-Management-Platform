from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import (
    CustomerRepository
)


class CustomerService:

    @staticmethod
    def create(
        db: Session,
        data
    ):

        existing = CustomerRepository.get_by_email(
            db,
            data.email
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Customer email already exists"
            )

        customer = Customer(
            **data.model_dump()
        )

        return CustomerRepository.create(
            db,
            customer
        )

    @staticmethod
    def get(
        db: Session,
        customer_id: int
    ):

        customer = CustomerRepository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return customer

    @staticmethod
    def get_all(
        db: Session
    ):

        return CustomerRepository.get_all(db)

    @staticmethod
    def update(
        db: Session,
        customer_id: int,
        data
    ):

        customer = CustomerService.get(
            db,
            customer_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:

            existing = CustomerRepository.get_by_email(
                db,
                update_data["email"]
            )

            if existing and existing.id != customer_id:
                raise HTTPException(
                    status_code=400,
                    detail="Email already belongs to another customer"
                )

        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def delete(
        db: Session,
        customer_id: int
    ):

        customer = CustomerService.get(
            db,
            customer_id
        )

        CustomerRepository.delete(
            db,
            customer
        )
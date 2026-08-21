from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.customer import Customer
from app.models.user import User

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate
)

from app.services.customer_service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# ==================================================
# CREATE CUSTOMER
# ==================================================

@router.post(
    "",
    response_model=CustomerResponse,
    status_code=201
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return CustomerService.create(
        db,
        customer
    )


# ==================================================
# GET CUSTOMERS
# Search + Filtering + Sorting + Pagination
# ==================================================

@router.get(
    "",
    response_model=list[CustomerResponse]
)
def get_customers(
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,

    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    sort_by: str = "id",
    sort_order: str = "asc",

    db: Session = Depends(get_db),
):

    query = db.query(Customer)

    # ------------------------------
    # Name
    # ------------------------------

    if name:

        query = query.filter(
            Customer.name.ilike(
                f"%{name}%"
            )
        )

    # ------------------------------
    # Email
    # ------------------------------

    if email:

        query = query.filter(
            Customer.email.ilike(
                f"%{email}%"
            )
        )

    # ------------------------------
    # Phone
    # ------------------------------

    if phone:

        query = query.filter(
            Customer.phone.ilike(
                f"%{phone}%"
            )
        )

    # ------------------------------
    # Sorting
    # ------------------------------

    allowed_sort_fields = {
        "id": Customer.id,
        "name": Customer.name,
        "email": Customer.email,
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        Customer.id
    )

    if sort_order.lower() == "desc":

        query = query.order_by(
            sort_column.desc()
        )

    else:

        query = query.order_by(
            sort_column.asc()
        )

    # ------------------------------
    # Pagination
    # ------------------------------

    return (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


# ==================================================
# GET CUSTOMER
# ==================================================

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    return CustomerService.get(
        db,
        customer_id
    )


# ==================================================
# UPDATE CUSTOMER
# ==================================================

@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return CustomerService.update(
        db,
        customer_id,
        customer
    )
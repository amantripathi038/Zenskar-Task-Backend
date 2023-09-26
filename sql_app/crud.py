from sqlalchemy.orm import Session

from . import models, schemas


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.ID == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.Customer):
    new_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def update_customer(db: Session, customer_id: int, customer: schemas.Customer):
    db_customer = (
        db.query(models.Customer).filter(models.Customer.ID == customer_id).first()
    )
    if db_customer:
        for key, value in customer.dict().items():
            setattr(db_customer, key, value)
            db.commit()
            db.refresh(db_customer)
    return db_customer

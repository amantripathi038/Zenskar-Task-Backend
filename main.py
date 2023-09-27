from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from kafka import send_to_kafka

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    return "Server is working."


@app.get("/customers/{customer_id}/")
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    required_customer = crud.get_customer(db, customer_id)
    return required_customer


@app.get("/customers/")
async def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    required_customers = crud.get_customers(db, skip, limit)
    return required_customers


@app.post("/customers/")
async def create_customer(customer: schemas.Customer, db: Session = Depends(get_db)):
    new_customer = crud.create_customer(db, customer)
    if customer.forward_message:
        new_customer_data = {
            "ID": new_customer.ID,
            "name": new_customer.name,
            "email": new_customer.email,
        }
        send_to_kafka(
            "customer-events",
            {"event_type": "customer_created", "customer": new_customer_data},
        )
    return new_customer


@app.put("/customers/{customer_id}/")
async def update_customer(
    customer_id: int,
    customer: schemas.Customer,
    db: Session = Depends(get_db),
):
    updated_customer = crud.update_customer(db, customer_id, customer)
    if customer.forward_message:
        updated_customer_data = {
            "ID": updated_customer.ID,
            "name": updated_customer.name,
            "email": updated_customer.email,
        }
        send_to_kafka(
            "customer-events",
            {"event_type": "customer_updated", "customer": updated_customer_data},
        )
    return updated_customer

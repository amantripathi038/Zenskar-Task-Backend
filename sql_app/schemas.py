from pydantic import BaseModel


# Pydantic model for the response data
class Customer(BaseModel):
    name: str
    email: str
    forward_message: bool

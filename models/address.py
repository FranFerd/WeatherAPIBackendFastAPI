from pydantic import BaseModel

class AddressResponse(BaseModel):
    address: str
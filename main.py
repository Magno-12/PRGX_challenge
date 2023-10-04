from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()

class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class AddressModel(BaseModel):
    street: str
    city: str
    country: str

class UserWithAddressesModel(BaseModel):
    user: UserModel
    addresses: List[AddressModel]

db = []

@app.post("/users/", response_model=UserModel)
async def create_user(user_with_addresses: UserWithAddressesModel):
    email_exists = any(user['email'] == user_with_addresses.user.email for user in db)
    if email_exists:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user_data = user_with_addresses.user.model_dump()
    user_data["addresses"] = [addr.model_dump() for addr in user_with_addresses.addresses]
    db.append(user_data)
    user_dict = user_with_addresses.user.model_dump()
    response_data = {
        "message": "User created successfully",
        "user": user_dict
    }
    return JSONResponse(content=response_data)

@app.get("/users/", response_model=List[UserModel])
async def get_users_by_country(country: str = Query(..., title="Country", min_length=3)):
    users_in_country = []
    for user in db:
        if any(addr['country'] == country for addr in user['addresses']):
            user_copy = user.copy()
            user_copy.pop("password")
            users_in_country.append(UserModel(**user))
    if not users_in_country:
        raise HTTPException(status_code=404, detail="No users found in the specified country")
    return users_in_country

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

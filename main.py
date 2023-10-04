from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from pydantic import BaseModel, EmailStr
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: Optional[str]

class AddressModel(BaseModel):
    street: str
    city: str
    country: str

class UserWithAddressesModel(BaseModel):
    user: UserModel
    addresses: List[AddressModel]

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModelDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class AddressModelDB(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    city = Column(String)
    country = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=UserModel)
async def create_user(user_with_addresses: UserWithAddressesModel):
    db = SessionLocal()
    email_exists = db.query(UserModelDB).\
        filter(UserModelDB.email == user_with_addresses.user.email).\
                first()
    db.close()
    if email_exists:
        raise HTTPException(
            status_code=400, detail="Email is already registered"
        )

    user_data = user_with_addresses.user.model_dump()
    addresses_data = [
        addr.model_dump() for addr in user_with_addresses.addresses
        ]

    db = SessionLocal()
    db_user = UserModelDB(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    for address_data in addresses_data:
        address_data["user_id"] = db_user.id
        db_address = AddressModelDB(**address_data)
        db.add(db_address)

    db.commit()
    db.close()

    response_data = {
        "message": "User created successfully",
        "user": user_with_addresses.user.\
                model_dump(exclude={"password"}
                )
    }
    return JSONResponse(content=response_data)

@app.get("/users/", response_model=List[UserModel])
async def get_users_by_country(
    country: str = Query(..., title="Country", min_length=3)):
    db = SessionLocal()
    addresses = db.query(AddressModelDB).\
        filter(AddressModelDB.country == country).all()
    user_ids = [address.user_id for address in addresses]
    users_in_country = db.query(UserModelDB).\
        filter(UserModelDB.id.in_(user_ids)).all()
    db.close()
    if not users_in_country:
        raise HTTPException(
            status_code=404, detail="No users found in the specified country")
    users_data = [{"first_name": user.first_name,
                   "last_name": user.last_name,
                   "email": user.email, "password": None}
                   for user in users_in_country
                ]
    return users_data

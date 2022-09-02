from pydantic import BaseModel, PositiveInt, constr
from typing import Optional


class Customer(BaseModel):
    CustomerID: Optional[str]
    CompanyName: Optional[str]
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    Region: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]
    Fax: Optional[str]

    class Config:
        orm_mode = True


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Suppliers(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True


class Category(BaseModel):
    CategoryID: int
    CategoryName: str
    Description: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    ProductID: int
    ProductName: str
    Category: Optional[Category]
    Discontinued: int

    class Config:
        orm_mode = True


class CategoryUpdater(BaseModel):
    CategoryID: int
    CategoryName: Optional[str]
    Description: Optional[str]

    class Config:
        orm_mode = True


class CategoryCreator(BaseModel):
    CategoryName: Optional[str]
    Description: Optional[str]

    class Config:
        orm_mode = True

class SupplierCreator(BaseModel):
    CompanyName: str
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]


class SupplierUpdater(BaseModel):
    CompanyName: Optional[str]
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]
    Fax: Optional[str]
    HomePage: Optional[str]

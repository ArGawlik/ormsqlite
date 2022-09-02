from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from typing import Optional

from . import crud, schemas, models
from .database import get_db

router = APIRouter()


@router.get("/")
async def main_page():
    return "Hello world"


@router.get("/categories")
async def categories(db: Session = Depends(get_db)):
    categories = crud.get_all_categories(db)
    print(type(categories))
    return list(map(lambda x: {"id": x.CategoryID, "name": x.CategoryName}, categories))


@router.get("/categories/{id}")
async def category(id: PositiveInt, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, id)
    return category


@router.put("/categories/{id}")
async def put_category(id: PositiveInt, cat: schemas.CategoryUpdater, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, id)
    if category is None:
        raise HTTPException(status_code=404)
    return crud.update_category(db, id, cat)


@router.post("/categories", status_code=201)
async def create_category(cat: schemas.CategoryCreator, db: Session = Depends(get_db)):
    new_cat_id = crud.get_last_cat_id(db).CategoryID + 1
    return crud.create_category(db = db, cat = cat, id = new_cat_id)


@router.delete("/categories/{id}")
async def delete_category(id: PositiveInt, db: Session = Depends(get_db)):
    return crud.delete_category(db=db, id=id)


@router.get("/customers")
async def customers(db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return {"customers": list(map(lambda x: {"id": x.CustomerID, "name": x.CompanyName,
                                             "full_address": " ".join(list(
                                                 map(lambda y: "" if y is None else y,
                                                     [x.Address, x.PostalCode, x.City, x.Country])))},
                                  customers))}


@router.get("/products")
async def products(db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return {"products": list(map(lambda x: x.ProductName, products)),
            "products_counter": len(products)}


@router.get("/products/{product_id}")
async def get_specific_product(product_id: PositiveInt, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.ProductID, "name": product.ProductName}


@router.get("/customers_details", response_model=List[schemas.Customer])
async def get_all_customers(db: Session = Depends(get_db)):
    return crud.get_all_customers(db)


@router.get("/employees")
async def get_employees(limit: Optional[int] = 0,
                        offset: Optional[int] = 0, order: Optional[str] = "id", db: Session = Depends(get_db)):
    """Available orders: id, last_name, first_name, city"""
    order_dict = {"id": models.Employee.EmployeeID,
                  "last_name": models.Employee.LastName,
                  "first_name": models.Employee.FirstName,
                  "city": models.Employee.City}
    if order not in order_dict.keys() or limit < 0 or offset < 0:
        raise HTTPException(status_code=400, detail="Bad request")
    employees = crud.get_employees_with_params(db, limit, offset, order_dict[order.lower()])
    return employees


@router.get("/products/{id}/orders")
async def products_orders(id: PositiveInt, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, id)
    if product is None:
        raise HTTPException(status_code=404)
    product_orders = crud.get_product_orders(db, id)
    return list(map(lambda x: {"id": x.OrderID, "customer": x.CompanyName, "quantity": x.Quantity,
                               "total_price": x.Quantity * x.UnitPrice * (1 - x.Discount)}, product_orders))


@router.get("/products_extended")
async def products_extended(db: Session = Depends((get_db))):
    return crud.get_extended_products(db)


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


@router.get("/suppliers", response_model=List[schemas.Suppliers])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{supp_id}")
async def get_supp(supp_id: PositiveInt, db: Session = Depends(get_db)):
    db_supp = crud.get_supplier(db, supp_id)
    if db_supp is None:
        raise HTTPException(status_code=404)
    return db_supp


@router.get("/suppliers/{supp_id}/products", response_model=List[schemas.Product])
async def get_products_by_supp(supp_id: PositiveInt, db: Session = Depends(get_db)):
    db_supp = crud.get_products_by_supp(db, supp_id)
    if db_supp is None or not db_supp:
        raise HTTPException(status_code=404)
    return [{'ProductID': product.ProductID, 'ProductName': product.ProductName,
             'Category': {"CategoryID": product.CategoryID, 'CategoryName': product.CategoryName, 'Description': product.Description},
             'Discontinued': product.Discontinued, } for product in db_supp]


@router.post("/suppliers", status_code=201)
async def create_supplier(supp: schemas.SupplierCreator, db: Session = Depends(get_db)):
    new_supp_id = crud.get_last_supp_id(db).SupplierID + 1
    return crud.add_supplier(supp_id=new_supp_id, db=db, supp=supp)


@router.put("/suppliers/{supp_id}", status_code=200)
async def update_supplier(supp_id: PositiveInt, supp: schemas.SupplierUpdater, db: Session = Depends(get_db)):
    db_supp = crud.get_suppliers(db)
    if supp_id not in [db_supplier.SupplierID for db_supplier in db_supp]:
        raise HTTPException(status_code=404)
    return crud.update_supplier(supp_id=supp_id, db=db, supp=supp)


@router.delete("/suppliers/{supp_id}", status_code=204)
async def delete_supplier(supp_id: PositiveInt, db: Session = Depends(get_db)):
    db_supp = crud.get_suppliers(db)
    if supp_id not in [db_supplier.SupplierID for db_supplier in db_supp]:
        raise HTTPException(status_code=404)
    return crud.delete_supplier(supp_id=supp_id, db=db)

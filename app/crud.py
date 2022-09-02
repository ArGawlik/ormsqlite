from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_all_customers(db: Session):
    return db.query(models.Customer).all()


def get_all_categories(db: Session):
    return db.query(models.Category).all()


def get_category_by_id(db: Session, id: int):
    return db.query(models.Category).filter(models.Category.CategoryID == id).first()


def update_category(db: Session, id: int, category):
    changes = [change for change in category]
    changes_dict = {}
    for change in changes:
        if change[1] is not None:
            changes_dict[change[0]] = change[1]
    dbb = db.query(models.Category).filter(models.Category.CategoryID == id).first()

    if "CategoryID" in changes_dict.keys(): dbb.CategoryID = changes_dict["CategoryID"]
    if "CategoryName" in changes_dict.keys(): dbb.CategoryName = changes_dict["CategoryName"]
    if "Description" in changes_dict.keys(): dbb.Description = changes_dict["Description"]
    db.commit()
    db.refresh(dbb)
    return dbb


def create_category(db: Session, cat: schemas.CategoryCreator, id: int):
    db_cat = models.Category(CategoryID = id ,CategoryName=cat.CategoryName, Description=cat.Description)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def get_all_products(db: Session):
    return db.query(models.Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.ProductID == product_id).first()


def get_employees_with_params(db: Session, limit: int, offset: int, order: str):
    if limit == 0:
        return db.query(models.Employee.EmployeeID,
                        models.Employee.LastName,
                        models.Employee.FirstName,
                        models.Employee.City).order_by(order).offset(offset).all()
    else:
        return db.query(models.Employee.EmployeeID,
                        models.Employee.LastName,
                        models.Employee.FirstName,
                        models.Employee.City).order_by(order).limit(limit).offset(offset).all()


def get_extended_products(db: Session):
    return db.query(models.Product.ProductID, models.Product.ProductName,
                    models.Category.CategoryName, models.Supplier.CompanyName) \
        .join(models.Category, models.Category.CategoryID == models.Product.CategoryID) \
        .join(models.Supplier, models.Product.SupplierID == models.Supplier.SupplierID).all()


def get_product_orders(db: Session, product_id: int):
    return db.query(models.OrderDetail.OrderID, models.Customer.CompanyName, models.OrderDetail.Quantity,
                    models.OrderDetail.UnitPrice, models.OrderDetail.Discount) \
        .join(models.Product, models.Product.ProductID == models.OrderDetail.ProductID) \
        .join(models.Order, models.Order.OrderID == models.OrderDetail.OrderID) \
        .join(models.Customer, models.Order.CustomerID == models.Customer.CustomerID) \
        .where(models.Product.ProductID == product_id).all()


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supp_id: int):
    return db.query(models.Supplier).filter(models.Supplier.SupplierID == supp_id).first()


def get_products_by_supp(db: Session, supp_id: int):
    return db.query(models.Product.ProductID, models.Product.ProductName,
                    models.Category.CategoryID, models.Category.CategoryName, models.Category.Description,
                    models.Product.Discontinued) \
        .join(models.Category, models.Product.CategoryID == models.Category.CategoryID) \
        .filter(models.Product.SupplierID == supp_id) \
        .order_by(models.Product.ProductID.desc()).all()


def get_last_supp_id(db: Session):
    return db.query(models.Supplier.SupplierID).order_by(models.Supplier.SupplierID.desc()).first()


def add_supplier(supp_id: int, db: Session, supp: schemas.SupplierCreator):
    db_supp = models.Supplier(SupplierID=supp_id, CompanyName=supp.CompanyName, ContactName=supp.ContactName,
                              ContactTitle=supp.ContactTitle, Address=supp.Address, City=supp.City,
                              PostalCode=supp.PostalCode, Country=supp.Country, Phone=supp.Phone)
    db.add(db_supp)
    db.commit()
    db.refresh(db_supp)
    return db_supp


def update_supplier(supp_id: int, db: Session, supp: schemas.SupplierUpdater):
    changes = [change for change in supp]
    changes_dict = {}
    for change in changes:
        if change[1] is not None:
            changes_dict[change[0]] = change[1]
    dbb = db.query(models.Supplier).filter(models.Supplier.SupplierID == supp_id).first()

    if "CompanyName" in changes_dict.keys(): dbb.CompanyName = changes_dict["CompanyName"]
    if "ContactName" in changes_dict.keys(): dbb.ContactName = changes_dict["ContactName"]
    if "ContactTitle" in changes_dict.keys(): dbb.ContactTitle = changes_dict["ContactTitle"]
    if "Address" in changes_dict.keys(): dbb.Address = changes_dict["Address"]
    if "City" in changes_dict.keys(): dbb.City = changes_dict["City"]
    # if "Region" in changes_dict.keys(): dbb.Region = changes_dict["Region"]
    if "PostalCode" in changes_dict.keys(): dbb.PostalCode = changes_dict["PostalCode"]
    if "Country" in changes_dict.keys(): dbb.Country = changes_dict["Country"]
    if "Phone" in changes_dict.keys(): dbb.Phone = changes_dict["Phone"],
    if "Fax" in changes_dict.keys(): dbb.Fax = changes_dict["Fax"]
    if "HomePage" in changes_dict.keys(): dbb.HomePage = changes_dict["HomePage"]
    db.commit()
    db.refresh(dbb)
    return dbb


def delete_supplier(supp_id: int, db: Session):
    supp_del = db.query(models.Supplier).filter(models.Supplier.SupplierID == supp_id).first()
    db.delete(supp_del)
    db.commit()


def get_last_cat_id(db: Session):
    return db.query(models.Category.CategoryID).order_by(models.Category.CategoryID.desc()).first()


def delete_category(db:Session, id:int):
    cat_del = db.query(models.Category).filter(models.Category.CategoryID == id).first()
    if cat_del is None:
        raise HTTPException(status_code=404)
    db.delete(cat_del)
    db.commit()
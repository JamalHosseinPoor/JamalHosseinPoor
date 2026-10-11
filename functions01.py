import json
from pydantic import BaseModel


class ProductModel (BaseModel):
    p_code: int = None
    title: str = None
    price: int = None
    qty: int = None


class ProductManyModel (BaseModel):
    products: list[ProductModel] = None


file_name = "./products.json"


def get_all_products() -> ProductManyModel:
    with open(file_name, "r") as f:
        p = json.load(f)
    return ProductManyModel(products=p)


def get_one_product(p_code: str) -> ProductModel:
    ap = get_all_products()
    for p in ap.products:
        if p.p_code == p_code:
            return p                     


def add_new_product(title: str, price: float, qty: int):
    old_p = get_all_products()
    old_p.products.append(
        ProductModel(
            p_code=old_p.products[-1].p_code+1,
            title=title,
            price=price,
            qty=qty,
        ))
    with open(file_name, "w") as f:
        json.dump(old_p.dict().get("products"), f, indent=2)


def delete_product(p_code: str):
    new_p = []
    for p in get_all_products().products:
        if p.p_code != p_code:
            new_p.append(p.dict())

    with open(file_name, "w") as f:
        json.dump(new_p, f, indent=2)


def update_product(p_code: str, title: str = None,
                   price: float = None, qty: int = None):
    new_p = []
    for p in get_all_products().products:
        if p.p_code == p_code:
            if title:
                p.title = title
            if price:
                p.price = price
            if qty:
                p.qty = qty
        new_p.append(p.dict(exclude_none=True))

    with open(file_name, "w") as f:
        json.dump(new_p, f, indent=2)

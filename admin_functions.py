from pydantic import BaseModel
import os
import json

file_name = "products.json"

###################################################################################

## subfunctions of products in Inventory##


class ProductModel (BaseModel):
    pr_code: int = None
    name: str = None
    price: float = None
    qty: int = None


class ProductManyModel (BaseModel):
    products: list[ProductModel] = None


def get_all_products() -> ProductManyModel:  # used in show_inventory
    with open(file_name, "r") as f:
        inventory = json.load(f)
    return ProductManyModel(products=inventory)


def get_one_product(pr_code) -> ProductModel:  # used in add_to_cart, show_cart,
    pr = get_all_products()
    for p in pr.products:
        if p.pr_code == pr_code:
            return p


def add_new_product(name: str, price: float, qty: int):
    old_p = get_all_products()
    new_code = old_p.products[-1].pr_code + 1 if old_p.products else 1
    old_p.products.append(
        ProductModel(pr_code=new_code, name=name, price=price, qty=qty)
    )
    with open(file_name, "w") as f:
        json.dump(old_p.model_dump()["products"], f, indent=2)


def delete_product(pr_code: int):
    new_p = [p.model_dump() for p in get_all_products().products
             if p.pr_code != pr_code]
    with open(file_name, "w") as f:
        json.dump(new_p, f, indent=2)


def update_product(pr_code: int, name: str = None,
                   price: float = None, qty: int = None):
    new_p = []
    for p in get_all_products().products:
        if p.pr_code == pr_code:
            if name:
                p.name = name
            if price:
                p.price = price
            if qty:
                p.qty = qty
        new_p.append(p.model_dump(exclude_none=True))
    with open(file_name, "w") as f:
        json.dump(new_p, f, indent=2)

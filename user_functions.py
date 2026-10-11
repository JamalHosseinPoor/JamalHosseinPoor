import os
from admin_functions import *
import uuid

cart_file = "cart.json"


class CartItemModel(BaseModel):
    cart_code: str = None
    qty: int = 0
    items: list[ProductModel] = []
    total_price: float = 0.0

############################################################################

## Sub Functions of Card###


def get_cart() -> CartItemModel:  # used in add_to_cart, show_cart, check_out menu 2, 3
    with open(cart_file, "r") as f:
        data = json.load(f)
    return CartItemModel.model_validate(data)


def save_cart(cart: CartItemModel):  # used in add_to_cart, check_out menu 3
    cart.cart_code = str(uuid.uuid4())
    with open(cart_file, "w") as f:
        json.dump(cart.model_dump(), f, indent=2)


def add_to_cart(pr_code: int, qty: int = 1):  # used in show_inventory menu 1
    if qty <= 0:
        print("Quantity must be greater than zero.")
        return False

    product = get_one_product(pr_code)
    if product is None:
        print("Product not found.")
        return False

    cart = get_cart()

    if cart and cart.items:
        for item in cart.items:
            if item.pr_code == pr_code:
                new_qty = item.qty + qty
                if new_qty > product.qty:
                    print(
                        f"Sorry, only {product.qty} of {product.name} in stock.")
                    return False
                item.qty = new_qty
                save_cart(cart)
                return True
    else:
        cart = CartItemModel()

    if qty > product.qty:
        input(
            f"Sorry, only {product.qty} of {product.name} in stock.\nPress Enter to continue...")
        return False

    cart.items += [ProductModel(
        qty=qty,
        pr_code=pr_code,
        price=product.price * qty,
        name=product.name
    )]
    cart.total_price += product.price * qty
    cart.qty += qty

    save_cart(cart)
    return True
    print(cart)
    print(product.price * qty, cart.total_price)

    input()

####################################################################################

## Menu Functions ###


def show_cart():
    cart = get_cart()
    if not cart.items:
        input("Your cart is empty. Press Enter to continue...")
        return

    print("Product\t\tQty\tPrice\tSubtotal")
    total = 0
    for item in cart.items:
        product = get_one_product(item.pr_code)
        if product is None:
            continue
        subtotal = product.price * item.qty
        total += subtotal
        print(f"{product.name}\t\t{item.qty}\t{product.price}\t{subtotal:.2f}")
    input(f"Total: {total:.2f}.Press Enter to continue...")

# Case 1: uses subfunctions of Inventory


def show_inventory():
    os.system("cls")
    inventory = get_all_products()

    print("num\t.\tProduct\t->\tPrice\t->Quantity")
    for i, o in enumerate(inventory.products):
        print(f" {i} . {o.name}\t->\t{o.price}\t->\t{o.qty}")
    p = int(input("Choose your product number : "))
    qty = int(input("Enter your desired amount: "))
    pr_code = inventory.products[p].pr_code
    add_to_cart(pr_code, qty)

# pr_code and qty of a chosen product are added to the costumer card.

# Case 2: uses subfunctions of Card


def check_out():
    cart = get_cart()
    if not cart.items:
        input("Your cart is empty. Press Enter to continue... ")
        return

    total_price = 0
    for item in cart.items:
        product = get_one_product(item.pr_code)
        if product is None:
            print(f"Product {item.pr_code} no longer exists.")
            input("Press Enter to continue... ")
            return
        if product.qty < item.qty:
            print(f"Sorry, we only have {product.qty} of {product.name} left.")
            input("Press Enter to continue... ")
            return
        total_price += product.price * item.qty

    answer = input(
        f"Your total price is {total_price:.2f}. Confirm purchase? (y/n): ")
    if answer.lower() != "y":
        print("Checkout cancelled. Your cart is kept.")
        input("Press Enter to continue... ")
        return

    all_products = get_all_products()
    for item in cart.items:
        for p in all_products.products:
            if p.pr_code == item.pr_code:
                p.qty -= item.qty
    with open(file_name, "w") as f:
        json.dump(all_products.model_dump()["products"], f, indent=2)

    save_cart(CartItemModel(items=[]))
    input("Purchase successful! Press Enter to continue... ")


############################################################################################
def menu():
    os.system("cls")
    show_cart()
    print("1.Inventory\n2.Show Cart\n3.Check Out\n4.Exit")
    match input("-> "):
        case "1":
            show_inventory()
        case "2":
            show_cart()
        case "3":
            check_out()
        case "4":
            exit()
        case _:
            input("Invalid Input. Press Enter to continue... ")

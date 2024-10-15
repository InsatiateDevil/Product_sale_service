
def get_cart_price(cart_items):
    return sum([cart_item.product.price * cart_item.quantity for cart_item in cart_items])

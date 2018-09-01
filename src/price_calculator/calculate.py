import json
import sys


def read_files(cart_file_name, base_price_file):
    with open(cart_file_name, 'r') as f:
        cart = json.load(f)

    with open(base_price_file, 'r') as f:
        base_prices = json.load(f)

    cart_value = 0
    for cart_item in cart:
        cart_value += calculate(get_base_price(cart_item['product-type'], cart_item['options'], base_prices),
                                cart_item['artist-markup'], cart_item['quantity'])

    return cart_value


def check_options(cart_option, baseprice_option):
    common_keys = set(baseprice_option.keys()) or set(cart_option.keys())
    for key in common_keys:
        if cart_option[key] not in baseprice_option[key]:
            return False
    return True


def get_base_price(product_type, options, base_prices):
    """

    kjasjoaijd
    :param product_type:
    :type product_type:  str
    :param options:
    :type options:
    :param base_prices:
    :return:
    """
    #
    filtered_list = list(filter(lambda x: x['product-type'] == product_type, base_prices))

    filtered_list_with_options = list(filter(lambda x: check_options(options, x['options']), filtered_list))

    if len(filtered_list_with_options) > 0:
        return filtered_list_with_options[0]['base-price']
    else:
        return 0


def calculate(base_price, artist_markup, quantity):
    return (base_price + round(base_price * artist_markup / 100)) * quantity


# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main():
    if len(sys.argv) != 3:
        print('Usage: python calculate.py <cart-file-path> <base-price-file-path>')
    else:
        print(read_files(sys.argv[1], sys.argv[2]))
        print()
    # Each line calls read_files, compares its result to the expected for that call.



# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()

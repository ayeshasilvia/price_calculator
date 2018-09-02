import json
import sys


def read_files(cart_file_name, base_price_file):
    """
    Reads the cart file and base-price file and calculates the cost of the cart
    based on the products in it and the base price of the product mentioned
    in the base-price file.
    :param cart_file_name: Name of the cart file
    :type cart_file_name: str
    :param base_price_file: Name of the base price file
    :type base_price_file: str
    :return: value of the cart
    :type: number
    """
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
    """
    Checks if the options of a product in the cart matches with the options of the given
    product in the base-price file.
    :param cart_option: The dict containing options provided with the product in the cart
    :type cart_option: dict
    :param baseprice_option: The dict containing options of the product in the base-price file
    :type baseprice_option: dict
    :return: True or False
    """

    # Get the common keys between the cart options and base-price options. For example:
    # cart_option.keys() = {'size' 'colour', 'print_location'}
    # baseprice_option.keys() = {'size' 'colour'}
    # The result will be {'size' 'colour'}
    common_keys = set(baseprice_option.keys()).intersection(set(cart_option.keys()))

    # For each of the common keys, check if the values of the key in the base-price options
    # contain the values of the key in the cart option.
    # For example:
    # cart_option['size] = 'xl'
    # baseprice_option['size] = {'xl', '3xl'}
    # Then this will return "True", because it's a match.
    for key in common_keys:
        if cart_option[key] not in baseprice_option[key]:
            return False
    return True


def get_base_price(product_type, options, base_prices):
    """
    Finds the base price of the products in the cart for given product type,
    options and the base-price dict.

    :param product_type: Name of the product
    :type product_type:  str
    :param options: Options of the product on the cart
    :type options: dict
    :param base_prices: The dict containing the base-price file
    :type base_prices: dict
    :return: The base price of the product
    """

    # Filtering the base_prices dict for given product-type.
    filtered_list = list(filter(lambda x: x['product-type'] == product_type, base_prices))

    # Filtering the above filtered list to scope it down with only the product whose options match with the
    # product's options in the cart.
    filtered_list_with_options = list(filter(lambda x: check_options(options, x['options']), filtered_list))

    # If the doubly filtered list has returned anything then that is our expected base price. If not, just returning 0.
    if len(filtered_list_with_options) > 0:
        return filtered_list_with_options[0]['base-price']
    else:
        return 0


def calculate(base_price, artist_markup, quantity):
    """
    Doing the math for getting total value of the cart.
    :param base_price: Base price of the product
    :param artist_markup: Artist markup value from the cart.
    :param quantity: Quntity from the cart.
    :return: Price of the product
    """
    return (base_price + round(base_price * artist_markup / 100)) * quantity


# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main():
    if len(sys.argv) != 3:
        print('Usage: python calculate.py <cart-file-path> <base-price-file-path>')
    else:
        print(read_files(sys.argv[1], sys.argv[2]))
        print()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import pytest
import os
from src.price_calculator.calculate import read_files, check_options, get_base_price, calculate

__author__ = "Ayesha Mosaddeque"
__copyright__ = "Ayesha Mosaddeque"
__license__ = "mit"


def test_read_files():
    assert read_files(os.path.abspath('tests/samples/cart-4560.json'),
                      os.path.abspath('tests/samples/base-prices.json')) == 4560
    assert read_files(os.path.abspath('tests/samples/cart-9363.json'),
                      os.path.abspath('tests/samples/base-prices.json')) == 9363
    assert read_files(os.path.abspath('tests/samples/cart-9500.json'),
                      os.path.abspath('tests/samples/base-prices.json')) == 9500
    assert read_files(os.path.abspath('tests/samples/cart-11356.json'),
                      os.path.abspath('tests/samples/base-prices.json')) == 11356
    assert read_files(os.path.abspath('tests/samples/cart-9363-non-existing-product.json'),
                      os.path.abspath('tests/samples/base-prices.json')) == 9363
    assert read_files(os.path.abspath('tests/samples/cart-9363-unknown-option.json'),
                      os.path.abspath('tests/samples/base-prices.json')) == 9363

    with pytest.raises(AssertionError):
        assert read_files(os.path.abspath('tests/samples/cart-9363-unknown-option.json'),
                          os.path.abspath('tests/samples/base-prices.json')) == 9369


def test_check_options_returns_true():
    cart_options = {
      "size": "small",
      "colour": "dark",
      "print-location": "front"
    }
    baseprice_options = {
      "colour": ["white", "dark"],
      "size": ["small", "medium"]
    }
    assert check_options(cart_options, baseprice_options)


def test_check_options_returns_false():
    cart_options = {
      "size": "xl",
      "colour": "dark",
      "print-location": "front"
    }
    baseprice_options = {
      "colour": ["white", "dark"],
      "size": ["small", "medium"]
    }
    assert not check_options(cart_options, baseprice_options)


def test_check_options_for_empty_options_at_cart():
    cart_options = {}
    baseprice_options = {
      "colour": ["white", "dark"],
      "size": ["small", "medium"]
    }
    assert check_options(cart_options, baseprice_options)


def test_check_options_for_empty_options_at_baseprice():
    cart_options = {
        "size": "xl",
        "colour": "dark",
        "print-location": "front"
    }
    baseprice_options = {
    }
    assert check_options(cart_options, baseprice_options)


def test_get_base_price_returns_price():
    with open(os.path.abspath('tests/samples/base-prices.json'), 'r') as f:
        base_price_dict = json.load(f)

    cart_options = {
        "size": "xl",
        "colour": "dark",
        "print-location": "front"
    }
    assert get_base_price('hoodie', cart_options, base_price_dict) == 4368


def test_get_base_price_returns_zero():
    with open(os.path.abspath('tests/samples/base-prices.json'), 'r') as f:
        base_price_dict = json.load(f)

    cart_options = {
        "size": "xl",
        "colour": "pink",
        "print-location": "front"
    }
    assert get_base_price('hoodie', cart_options, base_price_dict) == 0


def test_calculate():
    assert calculate(3800, 20, 1) == 4560

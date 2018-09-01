#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from src.price_calculator.calculate import read_files

__author__ = "Ayesha Mosaddeque"
__copyright__ = "Ayesha Mosaddeque"
__license__ = "mit"


def test_read_files():
    assert read_files(os.path.abspath('samples/cart-4560.json'),
                      os.path.abspath('samples/base-prices.json')) == 4560
    assert read_files(os.path.abspath('samples/cart-9363.json'),
                      os.path.abspath('samples/base-prices.json')) == 9363
    assert read_files(os.path.abspath('samples/cart-9500.json'),
                      os.path.abspath('samples/base-prices.json')) == 9500
    assert read_files(os.path.abspath('samples/cart-11356.json'),
                      os.path.abspath('samples/base-prices.json')) == 11356
    assert read_files(os.path.abspath('samples/cart-9363-non-existing-product.json'),
                      os.path.abspath('samples/base-prices.json')) == 9363
    assert read_files(os.path.abspath('samples/cart-9363-unknown-option.json'),
                      os.path.abspath('samples/base-prices.json')) == 9363

    with pytest.raises(AssertionError):
        assert read_files(os.path.abspath('samples/cart-9363-unknown-option.json'),
                          os.path.abspath('samples/base-prices.json')) == 9369

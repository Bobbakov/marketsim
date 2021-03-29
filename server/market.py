import itertools
import random
import numpy as np
import operator
from matplotlib import pyplot as plt
import pandas as pd
import time

from .order import order


class Market(object):
    # Initialize market
    def __init__(self,
                 meta_min_price=1,
                 meta_max_price=100,
                 meta_tick_size=0.05,
                 meta_min_quantity=1,
                 meta_max_quantity=10):
        # meta variables
        self.meta_transaction_counter = 0
        self.meta_min_price = meta_min_price
        self.meta_max_price = meta_max_price
        self.meta_tick_size = meta_tick_size
        self.meta_min_quantity = meta_min_quantity
        self.meta_max_quantity = meta_max_quantity

    def __str__(self):
        return "Market."


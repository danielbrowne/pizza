#!/usr/bin/env python
from __future__ import print_function
import json
import sys
try:
    from urllib.request import urlopen  # Python 3
except ImportError:
    from urllib2 import urlopen  # Python 2


# Place orders at http://collabedit.com/em3ev
URL = 'http://collabedit.com/download?id=em3ev'


def parse_data(data):
    orders = {}
    total = 0
    for category, items in data.items():
        # category will be "pizza", "pasta", etc.
        for item_type, item_name in items.items():
            # item_type will be pasta type or pizza name
            if 'choosers' in item_name:
                # item_type is pizza name
                count = len(item_name['choosers'])
                if count:
                    order = ' > '.join([category, item_type])
                    orders[order] = (count, item_name['choosers'])
                    total += count
            else:
                # item_type is pasta type, item_name is pasta name
                for name, choosers in item_name.items():
                    count = len(choosers['choosers'])
                    if count:
                        order = ' > '.join([category, item_type, name])
                        orders[order] = (count, choosers['choosers'])
                        total += count
    return orders, total


if __name__ == '__main__':
    #data = json.loads(sys.stdin.read())  # $ cat menu.json | ./get_orders.py
    resp = urlopen(URL)
    data = json.loads(resp.read().decode('utf-8'))
    orders, total = parse_data(data['orders']['data'])
    for item, (count, choosers) in orders.items():
        print(item + ': ', count, '(' + ', '.join(choosers) + ')')
    print('Total:', total)

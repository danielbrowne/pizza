import json
import sys
from urllib2 import urlopen


URL = 'http://collabedit.com/download?id=em3ev'


def parse_data(data):
    orders = {}
    total = 0
    for category, items in data.iteritems():
        # category will be "pizza", "pasta", etc.
        for item_type, item_name in items.iteritems():
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
                for name, choosers in item_name.iteritems():
                    count = len(choosers['choosers'])
                    if count:
                        order = ' > '.join([category, item_type, name])
                        orders[order] = (count, choosers['choosers'])
                        total += count
    return orders, total


if __name__ == '__main__':
    #data = json.loads(sys.stdin.read(), 'utf-8')
    resp = urlopen(URL)
    data = json.loads(resp.read(), 'utf-8')
    orders, total = parse_data(data['orders']['data'])
    for item, (count, choosers) in orders.iteritems():
        print item + ': ', count, '(' + ', '.join(choosers) + ')'
    print 'Total:', total

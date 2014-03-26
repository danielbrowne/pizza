#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals
from collections import OrderedDict
from datetime import date
import json
import re
from urllib2 import urlopen
from bs4 import BeautifulSoup


URL_INSALATA = 'http://www.colcacchio.co.za/menu/insalata'
URL_PASTA = 'http://www.colcacchio.co.za/menu/pasta'
URL_FILLED_PASTA = 'http://www.colcacchio.co.za/menu/filled_pasta_and_gnocchi'
URL_PIZZA = 'http://www.colcacchio.co.za/menu/pizza'


def add_choosers(menu_items):
    if isinstance(menu_items, dict):
        dict_ = {}
        for k, v in menu_items.iteritems():
            dict_[k] = add_choosers(v)
        return dict_

    else:
        return {i: {'choosers': []} for i in menu_items}


def build_orders():
    orders = OrderedDict([
        ['rules', [
            "You do not talk about Pizza Night.",
            "Snooze you looze! Late orders ignored.",
            "Quote your strings. Just do it."
        ]],
        ['orders', OrderedDict([
            ['meta', {
                "hierarchy": "sys/voss/voss2",
                "url": "http://www.colcacchio.co.za/menu",
                "e164": "+27 21 551 1658",
                "content-type": "application/json",
                "schema_version": date.today().isoformat(),
                "api": "https://github.com/kaapstorm/pizza/blob/master/get_orders.py"
            }],
            ['data', OrderedDict()]
        ])]
    ])
    orders['orders']['data']['pizzas'] = add_choosers(get_pizzas())
    pastas = get_pastas()
    pastas.update(get_filled_pastas())
    orders['orders']['data']['pasta'] = add_choosers(pastas)
    orders['orders']['data']['salad'] = add_choosers(get_salads())
    return orders


def get_filled_pastas():
    soup = get_soup(URL_FILLED_PASTA)
    pastas = {'gnocchi': [],
              'capelletti': []}
    for item in soup.select('li.menu-item'):
        name = item.select('div > p > span.name')[0].string.lower()
        if name == 'gnocchi':
            pastas['gnocchi'].append(item.select('div > p.terms-conditions')[0].string.lower())
        else:
            pastas['capelletti'].append(name)
    return pastas


def get_menu_items(url):
    soup = get_soup(url)
    names = []
    for name in soup.select('span.name'):
        just_name = name.string.split('(')[0].strip().lower()
        names.append(just_name)
    return names


def get_pastas():
    all_pastas = get_menu_items(URL_PASTA)
    pasta_types = all_pastas[0:4]
    menu_items = all_pastas[4:]
    menu_items.sort()
    # Remove lasagna
    menu_items.remove('home-made lasagna')
    pastas = {t: [i for i in menu_items] for t in pasta_types}
    # Insert lasagna
    pastas['lasagna'] = ['home-made lasagna']
    return pastas


def get_pizzas():
    return get_menu_items(URL_PIZZA)


def get_salads():
    return get_menu_items(URL_INSALATA)


def get_soup(url):
    resp = urlopen(url)
    return BeautifulSoup(resp.read())


if __name__ == '__main__':
    text = json.dumps(build_orders(), indent=2).replace('\\u2019', "'")  # Colcacchio can't decide on their apostrophes
    choosers = re.compile('\{\n *"choosers": \[]\n *}', re.MULTILINE)  # Put "choosers" on one line
    print choosers.sub('{"choosers": []}', text)

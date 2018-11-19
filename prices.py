#!/usr/bin/env python
import argparse
import datetime
from collections import Counter

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding


class AsJson(dict):
    def get_string(self, path, default=""):
        keys = path.split(".")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break
        return val


def find(verb, api_request, product_id):
    try:
        api = Finding(debug=False, domain='svcs.ebay.com', siteid='EBAY-GB', config_file='ebay.yaml')
        response = api.execute(verb, api_request)
        results = AsJson(response.dict())
        items = results.get_string('searchResult.item')

        if not product_id:
            # Find the most common product_id
            products = Counter()
            for item in items:
                products[AsJson(item).get_string('productId.value')] += 1
            else:
                if len(products) > 1:
                    # remove the null id counts
                    products.pop('', None)
                    # get id from [(<id>, <count>)]
                    product_id = products.most_common(1)[0][0]

        for item in items:
            if AsJson(item).get_string('productId.value') == product_id or product_id is None:
                # Filter on product id if there is one
                ending_date = AsJson(item).get_string('listingInfo.endTime')[:10]
                day = datetime.datetime.strptime(ending_date, '%Y-%m-%d').strftime('%A')
                amount = float(AsJson(item).get_string('sellingStatus.currentPrice.value'))
                shipping = float(AsJson(item).get_string('shippingInfo.shippingServiceCost.value'))
                item_id = AsJson(item).get_string('itemId')
                url = AsJson(item).get_string('viewItemURL')
                print('£{:03.2f} + £{:03.2f} - {} {} {} {}'.format(amount, shipping, day, ending_date, item_id, url))
        else:
            print()

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

    return product_id


def sold(search, product_id=''):
    print('Recently Sold:')
    api_request = {'keywords': search, 'itemFilter': [{'name': 'ListingType', 'value': 'Auction'}, {'name': 'LocatedIn', 'value': 'GB'}, {'name': 'SoldItemsOnly', 'value': True}]}
    return find('findCompletedItems', api_request, product_id)


def available(search, product_id=''):
    print('Available Auctions:')
    api_request = {'keywords': search, 'itemFilter': [{'name': 'ListingType', 'value': 'Auction'}, {'name': 'LocatedIn', 'value': 'GB'}], 'sortOrder': 'EndTimeSoonest'}
    return find('findItemsAdvanced', api_request, product_id)


def get_parser():
    parser = argparse.ArgumentParser(description='Ebay auctions - get recently completed and currently available auctions for sniping')
    parser.add_argument('--productId', action="store", nargs='?', help='Ebay product id')
    parser.add_argument('search', action="store", nargs='+', help='search terms')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    search = ' '.join(args['search'])
    id = args['productId']

    # search = 'Wii Mario Kart'
    # id = '219603758'
    # id = ''
    # sold(search='ps3 portal 2')
    # available(search='ps3 portal 2')
    # sold(search='amazon echo show', product_id='242648070')
    # find(search='amazon echo show', product_id='242648070')

    # print('Looking for: {}'.format(search))
    id = sold(search, id)
    available(search, id)


if __name__ == '__main__':
    command_line_runner()

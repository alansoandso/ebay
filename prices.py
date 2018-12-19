#!/usr/bin/env python
import argparse
import datetime
from collections import Counter
from pprint import pprint

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding


class AsJson(dict):
    def get_string(self, path, default=""):
        keys = path.split(".")
        val = None

        try:
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

        except AttributeError:
            return default


def find(verb, api_request, product_id):
    try:
        api = Finding(debug=False, domain='svcs.ebay.com', siteid='EBAY-GB', config_file='ebay.yaml')
        response = api.execute(verb, api_request)
        # pprint(response.dict())
        results = AsJson(response.dict())
        page = int(results.get_string('paginationOutput.pageNumber'))
        pages = int(results.get_string('paginationOutput.totalPages'))
        items = results.get_string('searchResult.item')

        while page < pages and page < 4:
            api_request['paginationInput']['pageNumber'] = page + 1
            response = api.execute(verb, api_request)
            # pprint(response.dict())
            results = AsJson(response.dict())
            page = int(results.get_string('paginationOutput.pageNumber'))
            items.extend(results.get_string('searchResult.item'))

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
            ending_date = AsJson(item).get_string('listingInfo.endTime')[:10]
            day = datetime.datetime.strptime(ending_date, '%Y-%m-%d').strftime('%A')
            amount = float(AsJson(item).get_string('sellingStatus.currentPrice.value', '999'))
            shipping = float(AsJson(item).get_string('shippingInfo.shippingServiceCost.value', '0'))

            item_id = AsJson(item).get_string('itemId', )
            url = AsJson(item).get_string('viewItemURL')
            total = '£{:03.2f} + £{:03.2f}'.format(amount, shipping)
            if AsJson(item).get_string('productId.value') == product_id:
                listing = '*{:<17} {} {} {} {}'.format(total, ending_date, day, item_id, url)
            else:
                listing = ' {:<17} {} {} {} {}'.format(total, ending_date, day, item_id, url)
            print(listing)
        else:
            print()

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

    return product_id


def sold(search, product_id=''):
    print('Recently Sold:')
    api_request = {'keywords': search,
                   'sortOrder': 'PricePlusShippingLowest',
                   'paginationInput': {'pageNumber': 1},
                   'itemFilter': [{'name': 'ListingType', 'value': 'Auction'},
                                  {'name': 'LocatedIn', 'value': 'GB'},
                                  {'name': 'SoldItemsOnly', 'value': True}]}
    return find('findCompletedItems', api_request, product_id)


def buy_it_now(search, product_id=''):
    print('Available as buy it now:')
    api_request = {'keywords': search,
                   'itemFilter': [{'name': 'ListingType', 'value': 'FixedPrice'}],
                   'sortOrder': 'PricePlusShippingLowest',
                   'paginationInput': {'pageNumber': 1}}
    # api_request = {'keywords': search, 'itemFilter': [{'name': 'ListingType', 'value': 'AuctionWithBIN'}]}
    # api_request = {'keywords': search}
    return find('findItemsAdvanced', api_request, product_id)


def available(search, product_id=''):
    print('Available Auctions:')
    api_request = {'keywords': search,
                   'itemFilter': [{'name': 'ListingType', 'value': 'Auction'},
                                  {'name': 'LocatedIn', 'value': 'GB'}],
                   'sortOrder': 'EndTimeSoonest',
                   'paginationInput': {'pageNumber': 1}}
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

    buy_it_now(search, id)
    id = sold(search, id)
    available(search, id)


if __name__ == '__main__':
    command_line_runner()

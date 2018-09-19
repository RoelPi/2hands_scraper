# -*- coding: utf-8 -*-

import time
import bs4 as bs
import requests
import pandas as pd
import datetime
from urllib import parse
import uuid
import csv



def test_value(v):
    if v is None:
        v = 'error'
    else:
        v = v.text.strip()
    return v

def scrape_bids(offer_id, parse, d, l):
    # Create DataTable for all the bids to be stored in
    table_bids = pd.DataFrame(columns=['offer_id','bid','bidder','bidder_link','bid_date'])
    
    # Select all parameters of a bid
    dom_start_bid = test_value(parse.select_one('form.bidding-form p')).replace('vanaf € ','')
    
    if dom_start_bid != 'error':
        dom_bid_prices = parse.select('.bidding-info .price')
        # Check if bids have actually been made
        if len(dom_bid_prices) > 0:
            dom_bid_bidders = parse.select('.bidding-info .name a')
            dom_bid_bidder_ids = [link['href'].replace('€ ','').replace('.','').replace('profiel','').replace('/','') \
                                  for link in parse.select('.bidding-info .name a')]
            dom_bid_dates = parse.select('.bidding-info .bidding-data time')
        
            # Add initial ask price
            table_bids = pd.concat([table_bids, pd.DataFrame({'offer_id': [offer_id], 'bid': [dom_start_bid], 'bidder': 'start', 'bidder_link': [l], 'bid_date': [d]})])
            
            # Loop through all bids
            for i, bid in enumerate(dom_bid_prices):
                table_bids = pd.concat([table_bids,pd.DataFrame({'offer_id': [offer_id], 'bid': [bid], 'bidder': [test_value(dom_bid_bidders[i])], 'bidder_link': [dom_bid_bidder_ids[i]], 'bid_date': [test_value(dom_bid_dates[i])]})])
            
            # Return all the bids as a DataFrame
        return table_bids
    else:
        return None
        
def scrape_car(offer_id, dimensions, values):
    
     # Test if car actually has dimensions
    if len(dimensions) > 0:
        table_car = pd.DataFrame(columns=['offer_id','dimension','value'])
        for i, dim in enumerate(dimensions):
            table_car = pd.concat([table_car, pd.DataFrame({'offer_id': [offer_id], 'dimension': [test_value(dim).replace(':','')], 'value': [test_value(values[i])]})])
        return table_car
    
    
def scrape_offer(url):
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    parsedPage = bs.BeautifulSoup(page.text, 'html.parser')
    
    # Product ID
    dom_id =  test_value(parsedPage.select_one('.active-breadcrumb-content')).replace('Zoekertje ','')
    
    # Product title
    dom_title = test_value(parsedPage.select_one('.main .title-wrapper h1'))
    
    # Product price
    dom_price = test_value(parsedPage.select_one('.main .item-info .price'))
    
    # Product brand
    dom_brand = test_value(parsedPage.select('.breadcrumb-list li a span')[2])

    # Product dimensions
    dom_dimension_names = parsedPage.select('div.item-details-lists dl.item-details-list dt') # To be texted
    dom_dimension_values = parsedPage.select('div.item-details-lists dl.item-details-list dd') # To be texted
    
    # Views
    dom_views = int(test_value(parsedPage.select_one('.main .item-counter .views-count')))
    
    # Date
    dom_date = test_value(parsedPage.select_one('.main .item-counter .views-since time'))
    
    # Seller
    dom_seller = test_value(parsedPage.select_one('.sidebar .about-seller .seller-name .name'))
    
    # Seller link
    dom_seller_link = parsedPage.select_one('.sidebar .about-seller .seller-name')['href']
    
    # Seller id
    dom_seller_id = dom_seller_link.replace('profiel','').replace('/','')
    
    # Seller ratings
    dom_seller_ratings = test_value(parsedPage.select_one('.sidebar .about-seller .number-of-ratings')).replace('(','').replace(')','')
    
    # Seller location
    dom_seller_location = parsedPage.select_one('.seller-data .icon-location-large-customBlack')['data-seller-map-location']
    
    # Seller started selling on
    dom_seller_start = test_value(parsedPage.select_one('.sidebar .seller-data .data-text')).replace('actief sinds ','')
        
    table_offer = pd.DataFrame({'scrape_date': [str(time.strftime("%c"))],
                                'offer_id': [dom_id],
                                'offer_url': [url],
                                'offer_title': [dom_title], 
                                'offer_price': [dom_price],
                                'offer_brand': [dom_brand],
                                'offer_views': [dom_views], 
                                'offer_date': [dom_date], 
                                'offer_seller': [dom_seller],
                                'offer_seller_id': [dom_seller_id],
                                'offer_seller_ratings': [dom_seller_ratings],
                                'offer_seller_location': [dom_seller_location],
                                'offer_seller_started_on': [dom_seller_start]})
    
    # Product bids
    table_bids = scrape_bids(dom_id, parsedPage, dom_date, dom_seller_link) # returns None if no bids were made
                                                 
    # Car specs
    table_car = scrape_car(dom_id, dom_dimension_names, dom_dimension_values) # returns None if no bids were made
    
    return table_offer, table_bids, table_car
    
    
a, b, c = scrape_offer('https://www.2dehands.be/autos/opel/signum/opel-signum-1-9-cdti-150-441064649.html')
    
def scrape_overview(url):
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    parsedPage = bs.BeautifulSoup(page.text, 'html.parser')
    links = [link['href'] for link in parsedPage.select('.listed-adv-item-link')]
    return links

test = 'https://www.2dehands.be/autos/?prijsmin=0.00&p=be&prijsmax=10000000&language=nl&language=fr&auto_bj=1990'
i = 0
dom_links = []
while i <= 105:
    dom_links.extend(scrape_overview(test))
    i = i + 35
    
    
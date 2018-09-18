# -*- coding: utf-8 -*-

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

def scrape_bid(bid_panel):
    dom_start_bid = test_value(bid_panel.select_one('form.bidding-form p'))
    dom_bid_prices = bid_panel.select('.bidding-info .price') # To be texted
    dom_bid_bidders = bid_panel.select('.bidding-info .name a') # To be texted
    dom_bid_bidder_links = bid_panel.select('.bidding-info .name a')['href'] # To be texted
    dom_bid_date = bid_panel.select('.bidding-info .bidding-date time') # To be texted
    return None # Format to be defined
    
def scrape_car(url):
    

    
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    parsedPage = bs.BeautifulSoup(page.text, 'html.parser')
    
    # Product ID
    dom_id =  test_value(parsedPage.select_one('.active-breadcrumb-content')).replace('Zoekertje ','')
    
    # Product title
    dom_title = test_value(parsedPage.select_one('.main .title-wrapper h1'))
    
    # Product price
    dom_price = test_value(parsedPage.select_one('.main .item-info .price'))
    
    # Product dimensions
    dom_dimension_names = parsedPage.select('div.item-details-lists dl.item-details-list dt') # To be texted
    dom_dimension_values = parsedPage.select('div.item-details-lists dl.item-details-list dd') # To be texted
    
    # Views
    dom_views = int(test_value(parsedPage.select_one('.main .item-counter .views-count')))
    
    # Date
    dom_date = test_value(parsedPage.select_one('.main .item-counter .views_since time'))
    
    # Seller
    dom_seller = test_value(parsedPage.select_one('.sidebar .about-seller .seller-name .name'))
    
    # Seller link
    dom_seller_link = parsedPage.select_one('.sidebar .about-seller .seller-name')['href'] # To be texted
    
    # Seller ratings
    dom_seller_ratins = test_value(parsedPage.select_one('.sidebar .about-seller .number-of-ratings'))
    
    # Seller location
    dom_seller_location = test_value(parsedPage.select_one('.sidebar .seller-data .data-text')).replace('actief sinds ','')
    
    # Seller's product link
    dom_seller_products_link = parsedPage.select_one('.sidebar .extra-data .data-text')['href'] # To be texted
    
    # Product bids
    dom_bids = scrape_bid(parsedPage.select_one('#bidding-form .panel-content'))
    
    
    
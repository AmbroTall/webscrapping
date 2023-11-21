import grequests
from gevent import Timeout
import requests
from requests.adapters import HTTPAdapter, Retry
import logging
from contextlib import contextmanager
import random
import json

countries = ['mk', 'si', 'me', 'rs', 'bg', 'hr']#al
proxies = {
    "http": '',
    "https": '',
    'no_proxy': 'localhost,127.0.0.1'
}
https_proxies = {
    #"http": '',
    "https": '',
    'no_proxy': 'localhost,127.0.0.1'
}
@contextmanager
def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        yield session
    except requests.RequestException as e:
        logging.error(f"RequestException occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        session.close()

max_requests_per_ip = 1  # Change IP after this number of requests
request_count = 0

def change_proxy():
    global request_count
    random_country = random.choice(countries)
    proxies['http'] = f'http://phscrapingtest:strongzerocola_country-{random_country}_streaming-1@geo.iproyal.com:12321'
    proxies['https'] = f'http://phscrapingtest:strongzerocola_country-{random_country}_streaming-1@geo.iproyal.com:12321'
    https_proxies['https'] = f'http://phscrapingtest:strongzerocola_country-{random_country}_streaming-1@geo.iproyal.com:12321'
    request_count = 0

def make_request(url, headers, payload = [], post = False, proxy_type = 'mixed'):
    global request_count
    if(request_count == max_requests_per_ip):
        change_proxy()

    if(proxy_type == 'mixed'):
        proxies_to_use = proxies
    elif(proxy_type == 'https'):
        proxies_to_use = https_proxies

    try:
        if(post == True):
            response = requests.post(url, headers=headers, data=payload, proxies=proxies_to_use)
            request_count += 1
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except json.JSONDecodeError as json_error:
                print("JSON decoding error:", json_error, url)
        else:    
            response = requests.get(url, headers=headers, data=payload, proxies=proxies_to_use)
            request_count += 1
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except json.JSONDecodeError as json_error:
                print("JSON decoding error:", json_error, url)
    except requests.exceptions.RequestException as request_error:
        print("Request error:", request_error)

def make_requestHTML(url, headers, payload = [], post = False):
    global request_count
    if(request_count == max_requests_per_ip):
        change_proxy()

    try:
        if(post == True):
            response = requests.post(url, headers=headers, data=payload, proxies=proxies)
            request_count += 1
            return response.content
        else:    
            response = requests.get(url, headers=headers, data=payload, proxies=proxies)
            request_count += 1
            return response.content
    except requests.exceptions.RequestException as request_error:
        print("Request error:", request_error)

def fetch_data(urls, headers, payload = [], post = False, proxy_type = 'mixed'):
  reqs = [make_requestAsync(url, headers, payload, post, proxy_type) for url in urls]
  responses = grequests.map(reqs)
  return responses
def fetch_dataHTML(urls, headers, payload = [], post = False, proxy_type = 'mixed'):
  reqs = [make_requestHTMLAsync(url, headers, payload, post, proxy_type) for url in urls]
  responses = grequests.map(reqs)
  return responses

def make_requestAsync(url, headers, payload = [], post = False, proxy_type = 'mixed'):
    global request_count
    if(request_count >= max_requests_per_ip):
        change_proxy()

    if(proxy_type == 'mixed'):
        proxies_to_use = proxies
    elif(proxy_type == 'https'):
        proxies_to_use = https_proxies
        
    try:
        if post:
            request_func = grequests.post
        else:
            request_func = grequests.get

        with Timeout(3, False):  # Set timeout for this request
            response = request_func(url, headers=headers, data=payload, proxies=proxies_to_use)
            request_count += 1
            return response
    except Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as request_error:
        print("Request error:", request_error)
def make_requestHTMLAsync(url, headers, payload = [], post = False, proxy_type = 'mixed'):
    global request_count
    if(request_count == max_requests_per_ip):
        change_proxy()
    
    if(proxy_type == 'mixed'):
        proxies_to_use = proxies
    elif(proxy_type == 'https'):
        proxies_to_use = https_proxies

    try:
        if(post == True):
            response = grequests.post(url, headers=headers, data=payload, proxies=proxies_to_use)
            request_count += 1
            return response
        else:    
            response = grequests.get(url, headers=headers, data=payload, proxies=proxies_to_use)
            request_count += 1
            return response
    except requests.exceptions.RequestException as request_error:
        print("Request error:", request_error)

def make_requestOld(url, headers, payload = [], post = False):
    try:
        if(post == True):
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except json.JSONDecodeError as json_error:
                print("JSON decoding error:", json_error, url)
        else:    
            response = requests.get(url, headers=headers, data=payload)
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except json.JSONDecodeError as json_error:
                print("JSON decoding error:", json_error, url)
    except requests.exceptions.RequestException as request_error:
        print("Request error:", request_error)

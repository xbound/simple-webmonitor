import asyncio
import concurrent.futures
import logging
import requests
import signal
import re

from bs4 import BeautifulSoup

CACHE = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s]:[%(message)s]')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


loop = asyncio.get_event_loop()

def request(url,requirement,timeout=10):
    try:
        response = requests.get(url,timeout=timeout)
        response_time = response.elapsed.total_seconds()
        if response.status_code in (404,500):
            response.raise_for_status()
        html_response = response.text
        soup = BeautifulSoup(html_response,'lxml')

        matched = soup.body.find_all(text=re.compile(requirement))
        if matched:
            logger.info("OK {}. Response time: {} seconds".format(url,response_time))
            CACHE[url].insert(0,'MATCHING: {}'.format(matched[0]))
            CACHE[url].insert(1,str(response_time))
        else:
            raise Exception()

    except requests.exceptions.ConnectionError:
        logger.error('Connection error. {} is down.'.format(url))
        CACHE[url].insert(0,'OFFLINE')
        CACHE[url].insert(1,'N/A')
    except requests.exceptions.Timeout:
        logger.error('Timeout. {} not responding.'.format(url))
        CACHE[url].insert(0,'TIMEOUT')
        CACHE[url].insert(1,'N/A')
    except requests.exceptions.HTTPError:
        logger.error('HTTP Error. {} returned status code {}. Response time: {} seconds'.format(url,response.status_code, response_time))
        CACHE[url].insert(0,'HTTP '+str(response.status_code))
        CACHE[url].insert(1,str(response_time))
    except requests.exceptions.TooManyRedirects:
        logger.error('Too many redirects for {}. Response time: {} seconds'.format(url,response_time))
        CACHE[url].insert(0,'REDIRECT')
    except Exception as e:
        logger.error('Content requirement not found for {}. Response time: {} seconds'.format(url,response_time))
        CACHE[url].insert(0,'NOT MATCHING')
        CACHE[url].insert(1,str(response_time))


def start_making_requests(urls,requirement):
    if 'token' not in CACHE:
        CACHE['token'] = requirement
    for url in urls:
        if url not in CACHE:
            CACHE[url] = ['N/A','N/A']
        loop.run_in_executor(None,request,url,requirement)

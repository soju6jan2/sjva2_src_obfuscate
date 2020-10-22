from framework.logger import get_logger
logger=get_logger('framework.common.daum')
from.tv import DaumTV
from.movie_search import MovieSearch
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
import requests
K=requests.Session
session=K()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

from bs4 import BeautifulSoup

from bak.meizi_mongodb_queue import MogoQueue
from request.request_helper import request

spider_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')
def start(url):
    response = request.get(url, 3)
    Soup = BeautifulSoup(response.text, 'lxml')
    all_a = Soup.find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url = a['href']
        spider_queue.push(url, title)

if __name__ == "__main__":
    start("myhttp://www.mzitu.com/all")

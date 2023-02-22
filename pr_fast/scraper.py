import httpx
from parsel import Selector


class Scraper():

    def scrapedata(tag):
        url = f'http://quotes.toscrape.com/tag/{tag}/'
        # print(url)
        s = httpx.Client()
        r = s.get(url)
        # print(r.status_code)

        parse = Selector(text=r.text)
        qlist = []
        quotes = parse.css("div.quote")

        for q in quotes:
            item = {
                'text': q.css("span::text").get(),
                'author': q.css("small::text").get(),
            }
            #print(item)
            qlist.append(item)
        return qlist



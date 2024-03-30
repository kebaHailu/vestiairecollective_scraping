import asyncio
import json
from typing import Dict, List

import httpx
from parsel import Selector

client = httpx.AsyncClient(
    follow_redirects=True,
    http2=True,
    headers={
        "User-Agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=-1.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    },
)


def find_hidden_data(html) -> dict:
    """extract hidden web cache from page html"""
    # use CSS selectors to find script tag with data
    data = Selector(html).css("script#__NEXT_DATA__::text").get()
    return json.loads(data)


async def scrape_product(url: str):
    # retrieve page HTML
    response = await client.get(url)
    # catch products that are no longer available as they redirect to 308
    for redirect in response.history:
        if redirect.status_code == 308:
            print(f"product {redirect.url} is no longer available")
            return None
    # find hidden web data
    data = find_hidden_data(response.text)
    # extract only product data from the page dataset
    product = data["props"]["pageProps"]["product"]
    return product


async def scrape_sitemap(url: str, max_pages: int = 100) -> List[Dict]:
    """Scrape Vestiaire Collective sitemap for products"""
    # retrieve sitemap
    print(f"scraping sitemap page: {url}")
    response_sitemap = await client.get(url)
    product_urls = Selector(response_sitemap.text).css("url>loc::text").getall()

    print(f"found {len(product_urls)} products in the sitemap: {url}\n  scraping the first {max_pages} products")
    # scrape products concurrently using asyncio
    product_scrapes = [asyncio.create_task(scrape_product(url)) for url in product_urls[:max_pages]]
    return await asyncio.gather(*product_scrapes)


# example scrape run:
print(asyncio.run(scrape_sitemap("https://www.vestiairecollective.com/sitemaps/https_en-new_items-1.xml", max_pages=5)))
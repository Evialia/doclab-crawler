import asyncio
import pyppeteer

from utils import crawl_author, get_href_for_node

pgn_btn_url_selector = '#gsc_authors_bottom_pag div button'


# Extract and store all found links to be crawled
async def extract_links():
    seed_url = "https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779&before_author=DgT7_5AYAAAJ&astart=0"

    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(seed_url)

    await crawl_authors(browser, page)
    pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)

    while len(pgn_btn) > 0:
        # Only do this if you can go to the next page
        await crawl_authors(browser, page)
        await goto_next_author_page(page)
        pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)


async def crawl_authors(browser, page):
    url_author_selector = '//*[@class="gs_ai_name"]/a'
    author_anchors = await page.xpath(url_author_selector)
    for author_anchor in author_anchors:
        await crawl_author(browser, await get_href_for_node(author_anchor))  # TODO - Make multi-threaded


async def goto_next_author_page(page):
    # Go to the next page
    pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
    await pgn_btn[1].click()
    await page.waitForNavigation()


asyncio.get_event_loop().run_until_complete(extract_links())
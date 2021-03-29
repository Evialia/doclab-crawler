import asyncio

import pyppeteer

from utils import crawl_author, get_href_for_node


async def main():
    seed_url = "https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779&before_author=DgT7_5AYAAAJ&astart=0"
    # async with browser.PageSession(seed_url) as page_session:

    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(seed_url)

    # get reference to current page (tab)
    # page = page_session.page
    url_author_selector = '//*[@class="gs_ai_name"]/a'
    pgn_btn_url_selector = '#gsc_authors_bottom_pag div button'

    author_anchors = await page.xpath(url_author_selector)
    for author_anchor in author_anchors:
        await crawl_author(browser, await get_href_for_node(author_anchor))  # TODO - Make multi-threaded

        # print('Author URLs found: ', len(author_urls))
        # # for author_url in author_urls:
        # print(await author_urls[0].xpath('/@href'))
        # await utils.crawl_author(page, await author_urls[0].xpath('@href'))
        # # utils.store(page.url, await page.content())


        # await page.screenshot({'path': 'before.png', 'fullPage': True})
        # pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
        # await pgn_btn[1].click()
        # await page.waitForNavigation()
        # # await page.screenshot({'path': 'after.png', 'fullPage': True})
        # utils.store(page.url, await page.content())


asyncio.get_event_loop().run_until_complete(main())
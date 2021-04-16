import asyncio
import os
import time
import pyppeteer
from dotenv import load_dotenv
from repository.AuthorRepository import AuthorRepository
from utils.dom_utils import get_href_for_node
from entity.Author import Author


load_dotenv()

seed_url = "https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779&before_author=DgT7_5AYAAAJ&astart=0"
pgn_btn_url_selector = '#gsc_authors_bottom_pag div button:not(:disabled)'


async def author_collector():
    author_repo = AuthorRepository()

    browser = await pyppeteer.launch(
        args=['--no-sandbox']
    )

    while True:
        page = await browser.newPage()
        await page.goto(seed_url)

        pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)

        while len(pgn_btn) > 1:
            pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
            # Only do this if you can go to the next page
            await extract_author_urls(page, author_repo)
            await goto_next_author_page(page)
            time.sleep(int(os.getenv('AUTHOR_URL_EXTRACTION_WAIT')))

        await page.close()
        print("Job complete, waiting", os.getenv('AUTHOR_URL_EXTRACTION_POLL'), "seconds for next run...")

        time.sleep(int(os.getenv('AUTHOR_URL_EXTRACTION_POLL')))


async def extract_author_urls(page, author_repo):
    url_author_selector = '//*[@class="gs_ai_name"]/a'
    author_anchors = await page.xpath(url_author_selector)
    for author_anchor in author_anchors:
        author = Author()
        author.set_url(await get_href_for_node(author_anchor))
        author.set_locked(False)

        # Make sure that the author doesn't already exist in the DB
        if author.get_url() and not author_repo.find_by_url(author.get_url()):
            print("Storing Author URL: ", author.get_url())
            author_repo.add(author)


async def goto_next_author_page(page):
    pgn_btn = await page.querySelectorAll(pgn_btn_url_selector)
    if len(pgn_btn) > 1:
        await pgn_btn[1].click()
        await page.waitForNavigation()
        print("Moving to next author page")
    else:
        print("No further author pages!")

asyncio.get_event_loop().run_until_complete(author_collector())

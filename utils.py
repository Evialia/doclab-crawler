import pyppeteer

from db_utils import does_url_exist, store_url


async def crawl_author(browser, url):
    page = await browser.newPage()
    await page.goto(url)

    # Expand all links hidden behind SHOW ALL button
    await show_all_doc_links(page)

    doc_selector = '.gsc_a_at'
    docs = await page.querySelectorAll(doc_selector)
    for doc in docs:
        external_doc_url = await get_doc_url(page, doc)

        if external_doc_url and not does_url_exist(external_doc_url):
            store_url(external_doc_url)
        # if external_doc_url and check_crawl_required(external_doc_url):
        #     # Only do the below if the URL needs to be crawled/re-crawled
        #     await crawl_doc(browser, external_doc_url)

        # Go back to the author's page
        await close_doc_modal(page)
        await page.waitFor(3000)


async def show_all_doc_links(page):
    show_more_selector = '#gsc_bpf_more:not(:disabled)'  # Get the "SHOW MORE" button if not disabled

    # Expand all available documents by clicking SHOW MORE button while it is enabled
    show_more_btn = await page.querySelector(show_more_selector)
    while show_more_btn is not None:
        await show_more_btn.click()
        await page.waitForResponse(lambda res: res.status == 200)
        show_more_btn = await page.querySelector(show_more_selector)


async def get_doc_url(page, doc):
    # Open the modal
    await doc.click()
    try:
        await page.waitForResponse(lambda res: res.status == 200)
    except pyppeteer.errors.TimeoutError:
        await page.screenshot({'path': 'TimeoutError.png', 'fullPage': True})
        print("TimeoutError on get_doc_url")

    # Get the link to the external document
    external_doc_anchor = await page.querySelector('.gsc_vcd_title_link')

    if external_doc_anchor is not None:
        return await get_href_for_node(external_doc_anchor)
    return False


async def close_doc_modal(page):
    # Close the modal
    closeButton = await page.querySelector('#gs_md_cita-d-x')
    await closeButton.click()
    await page.waitFor(1000)


async def get_href_for_node(node):
    url = await node.getProperty('href')
    return await url.jsonValue()


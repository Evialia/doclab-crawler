import asyncio
from Document import Document
from db_utils import get_next_url


# This can be run on multiple nodes in parallel
async def crawl_extracted_urls():
    next_url = get_next_url()

    while next_url is not None:
        # Only crawl if we are able to lock the url
        document = Document(next_url)
        if document.lock():
            await document.crawl_contents()
            document.unlock()
        next_url = get_next_url()

asyncio.get_event_loop().run_until_complete(crawl_extracted_urls())
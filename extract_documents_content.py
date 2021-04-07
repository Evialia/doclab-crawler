#!/usr/bin/env python
import asyncio
import os
from datetime import date, timedelta
import time

from dotenv import load_dotenv
from models.Document import Document
from utils.Connection import Connection

load_dotenv()

connection = Connection()

# This can be run on multiple nodes in parallel
async def extract_documents_content():
    while True:
        print("BEGIN DOCUMENT CONTENT EXTRACTION")
        next_url = get_next_url()

        while next_url is not None:
            print("EXTRACTING CONTENT:", next_url)
            # Only crawl if we are able to lock the url
            document = Document(next_url, connection)
            if document.lock():
                await document.crawl_contents()
                document.unlock()
            next_url = get_next_url()

        print("END DOCUMENT CONTENT EXTRACTION")

        time.sleep(int(os.getenv('DOCUMENT_CONTENT_EXTRACTION_POLL')))


def get_next_url():
    last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    db, cursor = connection.get()
    cursor.execute("SELECT url FROM documents WHERE (last_crawl IS NULL OR last_crawl < %(date)s) AND locked = 0 LIMIT 1", {'date': last_week})
    result = cursor.fetchone()

    if result is not None:
        return result[0]
    else:
        return None


asyncio.get_event_loop().run_until_complete(extract_documents_content())

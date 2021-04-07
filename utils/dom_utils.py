async def get_href_for_node(node):
    url = await node.getProperty('href')
    return await url.jsonValue()
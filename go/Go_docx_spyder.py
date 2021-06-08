"""
获取老男孩go教程

1、 获取go教程每一节链接

2、 针对每一节链接实现异步抓取
"""
import asyncio

import aiofiles
import aiohttp
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/90.0.4430.93"
}


def get_main_url(base_url, n):
    """
    获取每一节链接
    @base_url : 网站链接
    @n : 需要抓取的xpath位置，
    """
    resp = requests.get(base_url, headers=headers)
    if resp.status_code == 200:
        page_html = etree.HTML(resp.text)
        temp = page_html.xpath(f"//*[@class='chapters'][{n}]/a")
        urls = ([base_url.rsplit('/', 1)[0] + _.xpath("@href")[0], _.xpath("text()")[0]] for _ in temp)
        return urls


async def down_page(session, url, name):
    async with session.get(url, headers=headers) as resp:
        text = await resp.text()
        page_html = etree.HTML(text)
        content = page_html.xpath("//*[@id='mdeditor_preview_area']/textarea/text()")[0]
        async with aiofiles.open("./Go/" + name + ".md", 'w') as f:
            await f.write(content)


async def main(base_url, n=6):
    urls = get_main_url(base_url, n)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url, name in urls:
            obj = asyncio.create_task(down_page(session, url, name))
            tasks.append(obj)

        await asyncio.wait(tasks)


if __name__ == '__main__':
    import time

    t1 = time.time()
    base_url = 'https://pythonav.com/wiki'
    asyncio.run(main(base_url, 6))
    t2 = time.time()
    print("结束", t2 - t1)

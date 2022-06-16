import os
import aiofiles
from src.utils import get_project_root
from bs4 import BeautifulSoup


async def get_page(page_relative_path):
    page_path = os.path.join(get_project_root(), page_relative_path)
    async with aiofiles.open(page_path, 'r') as f:
        page = await f.read()
        return page.replace('\n', '')


async def get_main_page():
    page_path = os.path.join(get_project_root(), 'res/pages/main_page.html')
    async with aiofiles.open(page_path, 'r') as f:
        page = await f.read()
        page.replace('\n', '')
        soup = BeautifulSoup(page, 'html.parser')
        el = soup.find(id="MyFiles")
        x = el
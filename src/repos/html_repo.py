import os
import aiofiles
from src.utils import get_project_root
from jinja2 import Template


async def get_page(page_relative_path):
    page_path = os.path.join(get_project_root(), page_relative_path)
    async with aiofiles.open(page_path, 'r') as f:
        page = await f.read()
        return page.replace('\n', '')


async def get_main_page(main_folder_id, shared_folder_id):
    main_folder_path = "/folder/" + str(main_folder_id)
    shared_folder_id = "/folder/" + str(shared_folder_id)
    page_relative_path = "res/pages/main_page.html"
    page_path = os.path.join(get_project_root(), page_relative_path)
    async with aiofiles.open(page_path, 'r') as f:
        page = await f.read()
        page.replace('\n', '')
        template = Template(page)
        return template.render(my_files_href=main_folder_path, shared_files_href=shared_folder_id)


async def get_folders_page(folder):
    page_relative_path = "res/pages/folder_page.html"
    page_path = os.path.join(get_project_root(), page_relative_path)
    async with aiofiles.open(page_path, 'r') as f:
        page = await f.read()
        page.replace('\n', '')
        template = Template(page)
        if folder.folders:
            folder.folders.sort(key=lambda x: x["name"])
        if folder.files:
            folder.files.sort(key=lambda x: x["name"])
        return template.render(folder_path="/folder/",
                               file_path="/file/",
                               current_folder_id=str(folder._id),
                               folders=folder.folders,
                               files=folder.files)

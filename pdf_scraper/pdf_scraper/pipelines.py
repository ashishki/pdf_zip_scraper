from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
import os
import sqlite3
from datetime import datetime

class PDFDownloaderPipeline(FilesPipeline):
    """
    Pipeline for downloading PDF files.
    """
    def get_media_requests(self, item, info):
        pdf_link = item.get('pdf_link')
        if pdf_link:
            yield Request(url=pdf_link, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        # Create file path using project name and original PDF file name.
        project_name = request.meta['item'].get('project_name', 'default').replace(" ", "_")
        pdf_name = request.url.split('/')[-1]
        return f"{project_name}/{pdf_name}"


class ZipDownloaderPipeline(FilesPipeline):
    """
    Pipeline for downloading ZIP archives.
    """
    def get_media_requests(self, item, info):
        zip_link = item.get('zip_link')
        if zip_link:
            yield Request(url=zip_link, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        # Create file path using project name and original ZIP file name.
        project_name = request.meta['item'].get('project_name', 'default').replace(" ", "_")
        zip_filename = request.url.split('/')[-1]
        return f"{project_name}/{zip_filename}"


class SQLiteStorePipeline:
    """
    Pipeline for storing project metadata into a SQLite database.
    """
    def open_spider(self, spider):
        self.db_path = 'data/projects.db'
        spider.logger.info("SQLite DB initialized")
        # Ensure the data folder exists.
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                project_page TEXT,
                pdf_link TEXT,
                zip_link TEXT,
                zip_file_path TEXT,
                download_date TEXT
            )
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        zip_file_path = None
        if 'files' in item and item['files']:
            zip_file_path = item['files'][0].get('path')
        download_date = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO projects (project_name, project_page, pdf_link, zip_link, zip_file_path, download_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            item.get('project_name'),
            item.get('project_page'),
            item.get('pdf_link'),
            item.get('zip_link'),
            zip_file_path,
            download_date
        ))
        self.conn.commit()
        return item

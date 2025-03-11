# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProjectItem(scrapy.Item):
    # Name of the project extracted from the project page.
    project_name = scrapy.Field()
    # URL to the PDF file (if available)
    pdf_link = scrapy.Field()
    # URL to the ZIP archive (if available)
    zip_link = scrapy.Field()
    # URL of the project page (related-materials page)
    project_page = scrapy.Field()
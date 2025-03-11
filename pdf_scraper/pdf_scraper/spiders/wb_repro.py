import scrapy
import random
import asyncio
import urllib.parse
from datetime import datetime
from playwright_stealth import stealth_async
from pdf_scraper.items import ProjectItem

# Define user agent and referrer lists.
USER_AGENTS = [ ... ]
REFERERS = [ ... ]

async def apply_stealth(page):
    """
    Apply stealth techniques to avoid bot detection.
    """
    await stealth_async(page)
    for _ in range(5):
        x = random.randint(100, 1000)
        y = random.randint(100, 800)
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.5, 1.5))

class WBReproSpider(scrapy.Spider):
    name = "wb_repro"
    allowed_domains = ["reproducibility.worldbank.org"]
    
    def __init__(self, max_pages=5, *args, **kwargs):
        super(WBReproSpider, self).__init__(*args, **kwargs)
        self.max_pages = int(max_pages)
        self.current_date = datetime.now()

    def get_custom_headers(self):
        """
        Returns headers that simulate a real browser request.
        """
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": random.choice(REFERERS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }

    def start_requests(self):
        """
        Generate start requests for the catalog pages.
        """
        start_url = "https://reproducibility.worldbank.org/index.php/catalog/?&page=1"
        yield scrapy.Request(
            start_url,
            callback=self.parse,
            headers=self.get_custom_headers(),
            meta={
                "playwright": True,
                "page": 1,
                "playwright_page_coroutines": [
                    {"method": "call", "args": [apply_stealth]},
                    {"method": "wait_for_selector", "args": ['div.catalog-item'], "kwargs": {"timeout": 30000}},
                    {"method": "evaluate", "args": ["window.scrollTo(0, document.body.scrollHeight);"]},
                ],
            },
        )

    async def parse(self, response):
        """
        Parse the catalog page to extract project links.
        """
        current_page = response.meta.get("page", 1)
        self.logger.info("Processing global page: %s", response.url)
        await asyncio.sleep(random.uniform(2, 5))
        
        # Extract project links using the defined selector.
        project_links = response.css('a.d-flex::attr(href)').getall()
        self.logger.info("Found %d project links on page %d.", len(project_links), current_page)
        
        for link in project_links:
            if '/catalog/' in link and "?" not in link:
                absolute_link = response.urljoin(link)
                # Append /related-materials to get the correct project page.
                if not absolute_link.endswith("/related-materials"):
                    absolute_link = absolute_link.rstrip("/") + "/related-materials"
                self.logger.info("Processing project page: %s", absolute_link)
                yield scrapy.Request(
                    absolute_link,
                    callback=self.parse_project,
                    headers=self.get_custom_headers(),
                    meta={"playwright": True},
                )
                
        if project_links and current_page < self.max_pages:
            next_page = current_page + 1
            next_page_url = f"https://reproducibility.worldbank.org/index.php/catalog/?&page={next_page}"
            self.logger.info("Moving to next global page: %s", next_page_url)
            yield scrapy.Request(
                next_page_url,
                callback=self.parse,
                headers=self.get_custom_headers(),
                meta={
                    "playwright": True,
                    "page": next_page,
                    "playwright_page_coroutines": [
                        {"method": "call", "args": [apply_stealth]},
                        {"method": "wait_for_selector", "args": ['div.catalog-item'], "kwargs": {"timeout": 30000}},
                        {"method": "evaluate", "args": ["window.scrollTo(0, document.body.scrollHeight);"]},
                    ],
                },
            )
        else:
            self.logger.info("No project links found or max_pages reached on page %d.", current_page)

    async def parse_project(self, response):
        """
        Parse the related-materials page to extract project name, PDF and ZIP links.
        """
        self.logger.info("Processing related-materials page: %s", response.url)
        await asyncio.sleep(random.uniform(2, 5))
        
        project_name = response.css('h1#dataset-title span::text').get(default="").strip()
        pdf_link = response.xpath('//a[contains(@class, "download") and @data-extension="pdf"]/@href').get()
        if pdf_link:
            pdf_link = response.urljoin(pdf_link)
        zip_link = response.xpath('//a[contains(@class, "download") and @data-extension="zip"]/@href').get()
        if zip_link:
            zip_link = response.urljoin(zip_link)
        
        item = ProjectItem()
        item['project_name'] = project_name
        item['pdf_link'] = pdf_link
        item['zip_link'] = zip_link
        item['project_page'] = response.url
        self.logger.info("Extracted item: %s", item)
        yield item

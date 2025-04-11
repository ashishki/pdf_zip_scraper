# PDF/ZIP Scraper

A Scrapy-based web scraper that downloads PDF and ZIP files from the World Bank reproducibility catalog, extracts metadata, and stores it in a SQLite database. The project is containerized with Docker for easy deployment.

## Features

- **Dynamic Web Scraping**: Uses Scrapy integrated with Playwright to handle dynamic content.
- **File Downloads**: Automatically downloads PDF and ZIP files using custom pipelines.
- **Metadata Storage**: Extracts project metadata (project name, file URLs, etc.) and stores it in a SQLite database.
- **Dockerized Environment**: Includes a Dockerfile for containerized deployment, ensuring consistency across environments.

## Project Structure

```
pdf_zip_scraper/
├── project_scraper/              # Scrapy project package
│   ├── __init__.py
│   ├── items.py                  # Defines the ProjectItem
│   ├── pipelines.py              # Pipelines for downloading files and storing metadata in SQLite
│   ├── settings.py               # Scrapy settings (includes FILES_STORE and DOWNLOAD_MAXSIZE)
│   └── spiders/
│       ├── __init__.py
│       └── wb_repro.py           # Spider to scrape the World Bank reproducibility catalog
├── data/                         # Directory for downloaded files and the SQLite database (ignored by Git)
│   ├── raw_files/
│   └── projects.db
├── Dockerfile                    # Docker configuration for containerized deployment
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Installation

### Prerequisites

- Python 3.10 or later
- Docker (if you prefer containerized deployment)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ashishki/pdf_zip_scraper.git
   cd pdf_zip_scraper
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Spider**:
   ```bash
   scrapy crawl wb_repro -o output.json
   ```

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t pdf_zip_scraper .
   ```

2. **Run the container**:
   ```bash
   docker run -it --rm pdf_zip_scraper
   ```

## Future Updates

- **Text Extraction**: Integrate text extraction modules using libraries like PyMuPDF or Tesseract for OCR to process downloaded PDFs.
- **Search Functionality**: Add full-text search capabilities using Elasticsearch or Whoosh to query the extracted metadata.
- **Web Interface**: Develop a simple web UI (using Flask or Django) for searching and displaying project details and file excerpts.
- **Improved Logging & Error Handling**: Enhance logging and add robust error handling for increased reliability.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
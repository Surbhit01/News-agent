# src/config/settings.py

# news_source: The website to scrape for news
# headlines_limit: The number of headlines to scrape
# timeout: Time to wait for page or component to load
# max_retries: Maximum number of attempts for page/component in case TimeoutError.
# load_state: Which action to wait for in case of wait_for_load_state
# output_dir: Storage path for output dir

CONFIG = {
    "news_url": "https://www.thehindu.com/news/national/",
    "headlines_limit": 5,
    "timeout": 60000,
    "max_retries": 3,
    "load_state": "domcontentloaded",
    "output_dir": "src/data/",
}

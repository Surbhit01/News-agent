from dotenv import load_dotenv
load_dotenv()
import asyncio
import json
from config.settings import CONFIG
from scraper.browser_manager import launch_browser
from scraper.browser_scraper import get_headlines, get_article_from_headline
from summarizer.news_summarizer import get_article_summary

async def run_pipeline():
    p, browser = await launch_browser()
    page = await browser.new_page()
    headlines = await get_headlines(page, CONFIG)
    print(f"Found {len(headlines)} headlines\n")

    results = []
    for headline in headlines:
        article = await get_article_from_headline(page, headline['url'], CONFIG)
        summary = get_article_summary(article)
        d = {}
        d['title'] = headline['title']
        d['url'] = headline['url']
        d['summary'] = summary['summary']
        results.append(d)

    with open('response.json', "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    await browser.close()
    await p.stop()
    return results

if __name__ == "__main__":
    asyncio.run(run_pipeline())

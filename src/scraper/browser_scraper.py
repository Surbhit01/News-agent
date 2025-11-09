from .browser_manager import load_page

async def get_headlines(page, cfg):
    page_loaded = await load_page(page, cfg["news_url"], selector="h3.title a")
    if not page_loaded:
        return []
    
    headlines = []
    links = await page.query_selector_all("h3.title a")
    for link in links[:cfg['headlines_limit']]:
        href = await link.get_attribute("href")
        text = await link.inner_text()
        if href and text:
            headlines.append({"title": text.strip(), "url": href.strip()})

    return headlines

async def get_article_from_headline(page, article_url, cfg):
    page_loaded = await load_page(page, article_url, selector="article, div.articlebodycontent", cfg=cfg)
    if not page_loaded:
        return ""
    
    try:
        content = await page.locator("article, div.articlebodycontent").inner_text()
        return content.strip()
    except Exception as e:
        print(f"[ERROR] Failed to extract main text for {article_url} - {e}")
        return ""
    
    

from playwright.async_api import async_playwright, TimeoutError
import asyncio

async def launch_browser():
    # async with async_playwright() as p:
    #     browser = await p.chromium.launch(headless=True)
    #     return p, browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    return playwright, browser
    
async def load_page(page, url, selector=None, cfg=None):
    if not cfg:
        cfg = {}
    max_retries = cfg.get("max_retries", 3)
    timeout = cfg.get("timeout", 60000)
    load_state = cfg.get("load_state", "domcontentloaded")
    timeout = cfg.get("timeout", timeout)
    # url = cfg.get("url", url)

    for attempt in range(1, max_retries + 1):
        try:
            await page.goto(url, timeout=timeout)
            await page.wait_for_load_state(load_state, timeout=timeout)
            if selector:
                await page.wait_for_selector(selector, timeout=timeout)
            return True
        except TimeoutError:
            print(f"Timeout Error while loading {url} - (Attempt {attempt} of {max_retries})")
            if attempt < max_retries:
                await asyncio.sleep(2*attempt)
            else:
                print(f"Failed to load {url} after {max_retries} attempts")
                return False
        except Exception as e:
            print(f"Error while loading {url} - {e}")
            return False
    return False








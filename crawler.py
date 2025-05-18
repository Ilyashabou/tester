import os
import re
import time
import logging
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)

def is_internal_link(base_url, link):
    return urlparse(link).netloc in (urlparse(base_url).netloc, '')

def normalize_url(url):
    parsed = urlparse(url)
    # Normalize scheme and netloc
    normalized = parsed._replace(fragment="", query="").geturl().rstrip('/')
    return normalized

def make_safe_filename(url, max_length=150):
    safe = re.sub(r'[^a-zA-Z0-9]', '_', url)
    return safe[:max_length]

def sanitize_filename(url):
    """Convert URL to a valid filename"""
    # Remove protocol and domain
    filename = re.sub(r'^https?://', '', url)
    # Replace invalid filename characters
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Replace slashes with underscores
    filename = filename.replace('/', '_')
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def crawl_website_and_screenshot(base_url, out_dir="screenshots", max_depth=3, throttle_seconds=1):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs('html_files', exist_ok=True)
    visited = set()
    to_visit = [(normalize_url(base_url), 0)]
    pages = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        while to_visit:
            url, depth = to_visit.pop(0)
            if url in visited or depth > max_depth:
                continue
            visited.add(url)

            for attempt in range(3):  # Retry logic
                try:
                    logging.info(f"Crawling: {url} (depth {depth})")
                    page = browser.new_page()
                    page.goto(url, timeout=60000)
                    page.wait_for_load_state('networkidle', timeout=60000)

                    final_url = normalize_url(page.url)
                    if final_url != url:
                        if final_url in visited:
                            page.close()
                            break
                        visited.add(final_url)
                        url = final_url

                    # Save screenshot
                    filename = make_safe_filename(url)
                    screenshot_path = os.path.join(out_dir, filename + ".png")
                    page.screenshot(path=screenshot_path, full_page=True)

                    # Save HTML
                    html = page.content()
                    html_path = os.path.join('html_files', filename + ".html")
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html)

                    # Store page info
                    pages.append({
                        'url': url,
                        'html': html,
                        'screenshot': screenshot_path,
                        'html_file': html_path
                    })

                    # Extract internal links
                    links = page.eval_on_selector_all('a[href]', 'elements => elements.map(a => a.href)')
                    for link in links:
                        normalized_link = normalize_url(link)
                        if is_internal_link(base_url, normalized_link) and normalized_link not in visited:
                            to_visit.append((normalized_link, depth + 1))

                    page.close()
                    time.sleep(throttle_seconds)  # Optional throttling
                    break  # Successful crawl
                except Exception as e:
                    logging.warning(f"Failed to process {url} (attempt {attempt + 1}/3): {e}")
                    if attempt == 2:
                        logging.error(f"Giving up on {url} after 3 failed attempts.")
                    if 'page' in locals():
                        page.close()
        browser.close()
    return pages

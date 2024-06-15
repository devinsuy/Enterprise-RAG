import json
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import os

##### DEFINITIONS #####

def save_content(url, content, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_') + '.txt'
    filepath = f"{output_dir}/{filename}"
    cleaned_content = remove_extra_blank_lines(content)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def remove_extra_blank_lines(content):
    lines = content.splitlines()
    cleaned_lines = []
    blank_line = False
    
    for line in lines:
        if line.strip() == '':
            if not blank_line:
                cleaned_lines.append(line)
                blank_line = True
        else:
            cleaned_lines.append(line)
            blank_line = False
    
    return "\n".join(cleaned_lines)

def scrape_page(page, url):
    try:
        page.goto(url)
        page.wait_for_load_state('networkidle')
        
        # Wait for a specific element that indicates JavaScript has fully loaded the page
        page.wait_for_selector('body')  # Adjust this selector to a specific element on your page if needed

        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')

        # Remove <noscript> tags
        for noscript in soup.find_all('noscript'):
            noscript.decompose()

        text = soup.get_text(separator="\n")
        return text, soup
    except PlaywrightTimeoutError:
        print(f"Timeout error while scraping: {url}")
        return None, None
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return None, None

def scrape_site(page, url, output_dir, seen_urls):
    if url in seen_urls:
        return

    seen_urls.add(url)

    # Scrape the page content
    page_content, soup = scrape_page(page, url)
    if soup is None:
        return  # Skip further processing if there was an error

    # Check for the specific span element containing the text "[ARCHIVED CATALOG]" and skip saving if found
    if soup.find('span', string='[ARCHIVED CATALOG]'):
        print(f"Skipping archived catalog page: {url}")
    else:
        save_content(url, page_content, output_dir)

    # Find all links and recursively scrape them
    links = [a['href'] for a in soup.find_all('a', href=True) 
             if 'catalog.csulb.edu' in urljoin(url, a['href']) and 
             'preview_course' not in a['href'] and 
             not a['href'].startswith('#')]
    for link in links:
        full_link = urljoin(url, link)
        scrape_site(page, full_link, output_dir, seen_urls)

def scrape_urls(url_list, output_dir='output'):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to False for debugging
        context = browser.new_context()
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.new_page()

        for url in url_list:
            seen_urls = set()
            scrape_site(page, url, output_dir, seen_urls)

        browser.close()

##### MAIN #####

if __name__ == "__main__":
    base_url = "http://catalog.csulb.edu"
    scrape_urls([base_url])

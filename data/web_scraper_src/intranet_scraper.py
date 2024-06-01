import json
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

##### DEFINITIONS #####

# Reuse auth cookies
# I didn't upload my auth cookies file to the repository (for obvious reasons)
def load_cookies(cookie_file):
    with open(cookie_file, 'r') as file:
        cookies = json.load(file)
    return cookies


# Write to file
# File name preserves the url structure with / => _
# EX: berkeley.edu/courses/1234 => berkeley.edu_courses_1234.txt
def save_content(url, content, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = url.replace('https://', '').replace('/', '_').replace(':', '_') + '.txt'
    filepath = f"{output_dir}/{filename}"
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


# We inject cookes to maintain auth as if we were actually logged in
# Replicates the web browser session state to simulate navigating between pages
def add_cookies(context, cookies):
    for cookie in cookies:
        same_site = cookie.get('sameSite', 'Lax')
        if same_site not in ['Strict', 'Lax', 'None']:
            same_site = 'Lax'
        context.add_cookies([{
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie['domain'],
            'path': cookie.get('path', '/'),
            'secure': cookie.get('secure', False),
            'httpOnly': cookie.get('httpOnly', False),
            'sameSite': same_site,
            'expires': cookie.get('expirationDate', -1)
        }])

# Scrape an individual page
# "page" is webbrowser context
# We need to simulate webbrowser to get the full page content 
# since it simulates the javascript rendered HTML from we wouldn't otherwise get
def scrape_page(page, url):
    page.goto(url)
    page.wait_for_load_state('networkidle')
    page_content = page.content()
    soup = BeautifulSoup(page_content, 'html.parser')
    text = soup.get_text(separator="\n")

    # Use this implementation below to scrape all content into a single text chunk without whitespace 
    # text = ' '.join(soup.stripped_strings)

    return text


# Instruments the mocked browser context using webdriver for scraping each page
# Starts from a base_url and expands scraping to accessible links from the page
# if the adjacent page has /mids in the url
def scrape_site(base_url, output_dir='output'):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Load cookies
        cookies = load_cookies('cookies.json')
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.new_page()

        # Load cookies into the browser context
        page.goto(base_url)
        add_cookies(context, cookies)
        page.reload()

        # Get the homepage content
        homepage_content = scrape_page(page, base_url)
        save_content(base_url, homepage_content, output_dir)

        # Find all candidate links to expand
        # Only scrape pages with /mids in the url
        # Prevents us from jumping into irrelevant ischool content from this page
        soup = BeautifulSoup(page.content(), 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if 'mids' in a['href']]

        # Scrape each linked page we identified
        for link in links:
            full_link = urljoin(base_url, link)
            page_content = scrape_page(page, full_link)
            save_content(full_link, page_content, output_dir)

        browser.close()


# Util to scrape urls from a pre-defined list without further expansion 
def scrape_urls(url_list, output_dir='output'):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        cookies = load_cookies('cookies.json')
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.new_page()
        for url in url_list:
            page.goto(url)
            add_cookies(context, cookies)
            page.reload()
            page_content = scrape_page(page, url)
            save_content(url, page_content, output_dir)
        browser.close()


##### MAIN #####

if __name__ == "__main__":
    # Start scraping from student handbook
    # All urls are on intranet
    base_url = "https://www.ischool.berkeley.edu/intranet/students/mids"
    scrape_site(base_url)

    # Scrape other mids specific urls
    # These are public sites with related mids content
    additional_urls = [
        "https://ischoolonline.berkeley.edu/admissions/",
        "https://ischoolonline.berkeley.edu/admissions/international-admission",
        "https://ischoolonline.berkeley.edu/admissions/tuition-financial-aid",
        "https://ischoolonline.berkeley.edu/admissions/tuition-financial-aid/fellowship",
        "https://ischoolonline.berkeley.edu/admissions/events",
        "https://ischoolonline.berkeley.edu/form-data-science/",
        "https://ischoolonline.berkeley.edu/data-science/curriculum/",
        "https://ischoolonline.berkeley.edu/data-science/what-is-data-science/",
        "https://ischoolonline.berkeley.edu/data-science/careers-data-science/",
        "https://ischoolonline.berkeley.edu/data-science/study-applied-statistics/",
        "https://ischoolonline.berkeley.edu/data-science/class-profile/",
        "https://ischoolonline.berkeley.edu/data-science",
        "https://ischoolonline.berkeley.edu/experience",
        "https://ischoolonline.berkeley.edu/contact-us"
    ]
    scrape_urls(additional_urls)

    # Scrape couse catalog
    course_urls = [
        "https://www.ischool.berkeley.edu/courses/datasci",
        "https://www.ischool.berkeley.edu/courses/datasci/200",
        "https://www.ischool.berkeley.edu/courses/datasci/201",
        "https://www.ischool.berkeley.edu/courses/datasci/203",
        "https://www.ischool.berkeley.edu/courses/datasci/205",
        "https://www.ischool.berkeley.edu/courses/datasci/207",
        "https://www.ischool.berkeley.edu/courses/datasci/209",
        "https://www.ischool.berkeley.edu/courses/datasci/210",
        "https://www.ischool.berkeley.edu/courses/datasci/210a",
        "https://www.ischool.berkeley.edu/courses/datasci/221",
        "https://www.ischool.berkeley.edu/courses/datasci/231",
        "https://www.ischool.berkeley.edu/courses/datasci/233",
        "https://www.ischool.berkeley.edu/courses/datasci/241",
        "https://www.ischool.berkeley.edu/courses/datasci/255",
        "https://www.ischool.berkeley.edu/courses/datasci/261",
        "https://www.ischool.berkeley.edu/courses/datasci/266",
        "https://www.ischool.berkeley.edu/courses/datasci/271",
        "https://www.ischool.berkeley.edu/courses/datasci/281",
        "https://www.ischool.berkeley.edu/courses/datasci/290",
        "https://www.ischool.berkeley.edu/courses/datasci/293",
    ]
    scrape_urls(course_urls)


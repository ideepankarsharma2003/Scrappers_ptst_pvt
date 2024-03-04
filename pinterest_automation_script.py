#!/home/ubuntu/PinterestScrapper/.env/bin python
from playwright.sync_api import Playwright, sync_playwright, expect
import argparse

import argparse

parser = argparse.ArgumentParser(description='Scrape Pinterest.')
parser.add_argument('query', metavar='-q', type=str, nargs='+',
                    help='query')
parser.add_argument('filename', metavar='-f', type=str, nargs='+',
                    help='filename')
args= parser.parse_args()
print(f"""
      args= {args}
      """)
query= args.query[0]
filename= args.filename[0]

print(f"query: '{query}'")
print(f"filename: '{filename}'")

def run(playwright: Playwright, topic:str) -> None:
    
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pinterest.com/")
    page.locator("[data-test-id=\"unauth-header\"]").get_by_role("link", name="Explore").click()
    page.locator("[data-test-id=\"search-box-input\"]").click()
    page.locator("[data-test-id=\"search-box-input\"]").fill(topic)
    page.locator("[data-test-id=\"search-box-input\"]").press("ArrowDown")
    page.locator("[data-test-id=\"search-box-input\"]").press("Enter")

    div= page.locator('.vbI.XiG[role="list"]')
    inner_html= div.inner_html()
    # print(f"""
    #       div: 
    #       {div}
          
    #       HTML: 
    #       {inner_html}
    #       """)
    with open(filename, "wb") as f:
        f.write(inner_html.encode())
    # ---------------------
    context.close()
    browser.close()
    
    return inner_html
    
    
    


with sync_playwright() as playwright:
    run(playwright, topic=query)

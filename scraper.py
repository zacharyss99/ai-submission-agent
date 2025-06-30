import asyncio
from playwright.async_api import async_playwright
import sys

#asynchronous programming
#allows Python to run tasks that wait for something to load
#w/o freezing everything else
#used with Web Scraping (waiting for site to load)
#used with File I/O (waiting for response)
async def scrape_chatgpt_share_url(url):
    
    #async_playright() launches Playwright as asynch
    #program while async with opens the web browser
    #then closes it cleanly when done
    #with open("file.txt", "r") as f:
        #content = f.read() - 
        #opens the file, assigns it to f, then closes file
    #with = do this safely, then clean up after
    async with async_playwright() as p:
        
        #launch chromium browser headless - invisible
        #await says wait for this to finish, then move on
        #chromium is open source web browser made by Google
        browser = await p.chromium.launch(headless=False)
        
        #open a new tab
        page = await browser.new_page()
        #assuming two lines above just create 
        #a new blank google chrome tab
        
        #paste url inside tab
        await page.goto(url)
        
        #check if url is shareable, if not, return invalid
        if "share" not in url or not url.startswith("https://chat.openai.com/share"):
            return {"error": "Invalid or unshareable link"}

        
        #wait until at least one chat msg visible on the page
        #chatgpt uses div.markdown to wrap each message
        await page.wait_for_selector('[data-testid="conversation-turn"]')
        turns = await page.query_selector_all('[data-testid="conversation-turn"]')

        conversation = []
        for i, turn in enumerate(turns):
            role_el = await turn.query_selector("div.flex > div > div:first-child")
            message_el = await turn.query_selector("div.markdown")

            if role_el and message_el:
                role_text = await role_el.inner_text()
                role = "user" if "User" in role_text else "assistant"
                content = await message_el.inner_text()
                conversation.append({"role": role, "content": content.strip()})

        #loops over messages alternating between
        #"User" if index is even
        #"Assistant" if index is odd
        await browser.close()
        return conversation
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <chatgpt_share_url>")
        sys.exit(1)

    url = sys.argv[1]
    output = asyncio.run(scrape_chatgpt_share_url(url))

    from pprint import pprint
    pprint(output)    

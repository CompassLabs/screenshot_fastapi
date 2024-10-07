from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from playwright.async_api import async_playwright
import uuid
import os

app = FastAPI()

# Directory to store screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@app.get("/screenshot")
async def capture_screenshot(url: str = Query(..., description="URL of the website to capture")):
    # Generate a unique filename for the screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{uuid.uuid4()}.png")

    # Use Playwright to capture the screenshot
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path=screenshot_path)
        await browser.close()

    # Return the screenshot as a file response
    return FileResponse(screenshot_path, media_type='image/png')

"""
uvicorn main:app --reload
"""
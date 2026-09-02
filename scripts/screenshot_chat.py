import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    os.makedirs('e2e_screenshots', exist_ok=True)
    
    async with async_playwright() as p:
        # 1. Desktop AI Chat test
        browser = await p.chromium.launch(headless=True)
        context_desktop = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context_desktop.new_page()
        
        print("Loading desktop...")
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(1000)
        
        # Login
        await page.locator(".guest-mode-btn").first.click()
        await page.wait_for_timeout(2000)
        
        # Open AI widget
        print("Testing desktop AI widget...")
        await page.click('#ai-floating-btn')
        await page.wait_for_timeout(500)
        
        # Send a message to trigger the mock response
        await page.fill('#ai-input', 'Hello, testing demo mode')
        await page.click('#ai-send-btn')
        await page.wait_for_timeout(2000) # wait for response
        
        await page.screenshot(path="e2e_screenshots/04_chat_desktop.png")
        
        # 2. Mobile AI Chat test
        print("Testing mobile AI widget (480px)...")
        context_mobile = await browser.new_context(viewport={'width': 480, 'height': 800})
        page_mobile = await context_mobile.new_page()
        
        await page_mobile.goto("http://127.0.0.1:8000")
        await page_mobile.wait_for_timeout(1000)
        await page_mobile.locator(".guest-mode-btn").first.click()
        await page_mobile.wait_for_timeout(2000)
        
        await page_mobile.click('#ai-floating-btn')
        await page_mobile.wait_for_timeout(500)
        
        await page_mobile.screenshot(path="e2e_screenshots/05_chat_mobile.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

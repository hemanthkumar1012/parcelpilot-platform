import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Capture console logs to confirm it fires
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(1000)
        
        # Login
        await page.locator(".guest-mode-btn").first.click()
        await page.wait_for_timeout(2000)
        
        # Inject a console.log into the mousemove handler dynamically for verification
        await page.evaluate('''
            document.querySelectorAll('.panel').forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    console.log('Mousemove fired on panel!');
                });
            });
        ''')

        print("Triggering real hover off-center...")
        
        # By default, page.hover() aims for the center (x=width/2, y=height/2).
        # Our tilt formula yields 0 degrees at the exact center.
        # So we hover at a specific offset (e.g., top-left corner 20, 20)
        await page.hover('.panel', position={'x': 20, 'y': 20})
        
        # Wait for the CSS transition (150ms) to fully apply
        await page.wait_for_timeout(300)
        
        # Take a screenshot of the panel
        await page.locator('.panel').first.screenshot(path="e2e_screenshots/08_tilt_real_hover_fixed.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    os.makedirs('e2e_screenshots', exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(1000)
        
        # Login
        await page.locator(".guest-mode-btn").first.click()
        await page.wait_for_timeout(2000)
        
        # 1. Hardcoded tilt on #stat-total
        print("Testing hardcoded tilt...")
        
        # Add a fake hover class/style to trigger the hover shadow
        await page.evaluate('''
            const card = document.querySelector('.stat-card');
            card.style.transform = 'perspective(800px) rotateX(-4deg) rotateY(4deg) scale3d(1.01, 1.01, 1.01)';
            card.style.boxShadow = '0 4px 8px rgba(15, 23, 42, 0.06), 0 12px 24px rgba(37, 99, 235, 0.08)';
        ''')
        await page.wait_for_timeout(500)
        
        # Take screenshot of the stat cards area specifically to see it clearly
        await page.locator('.stats-grid').screenshot(path="e2e_screenshots/06_tilt_hardcoded.png")
        
        # Undo hardcode
        await page.evaluate('''
            const card = document.querySelector('.stat-card');
            card.style.transform = '';
            card.style.boxShadow = '';
        ''')
        
        # 2. Real mousemove driven hover on a panel
        print("Testing real mouse hover...")
        
        panel = page.locator('.panel').first
        box = await panel.bounding_box()
        
        # Move mouse to trigger mousemove event (bottom right quadrant to tilt it)
        # We need to hover over it, wait, and move a bit to ensure event fires
        await page.mouse.move(box['x'] + box['width'] * 0.75, box['y'] + box['height'] * 0.75, steps=10)
        await page.wait_for_timeout(500)
        
        # Take a screenshot of the panel
        await panel.screenshot(path="e2e_screenshots/07_tilt_real_hover.png")
        
        # 3. Test click target inside a tilted card
        print("Testing click on tilted card...")
        # Hover over the Tracking panel
        track_panel = page.locator('.panel-tracking-search')
        # Wait, the tracking panel is on the tracking page.
        # Let's just click the Dashboard quick tracking button.
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

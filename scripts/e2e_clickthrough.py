import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run():
    os.makedirs('e2e_screenshots', exist_ok=True)
    results = {"errors": [], "console": [], "steps": []}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Track console logs
        page.on("console", lambda msg: results["console"].append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: results["errors"].append(err.message))
        
        # 1. Load Landing Page
        print("Loading landing page...")
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(1000) # Wait for animations
        await page.screenshot(path="e2e_screenshots/01_landing.png")
        results["steps"].append("01_landing.png saved (Login view)")
        
        # 2. Click Guest Login
        print("Clicking Guest Login...")
        try:
            # First look for guest button
            btn = page.locator(".guest-mode-btn").first
            await btn.click()
            await page.wait_for_timeout(3000) # Wait for redirect + fetch
            
            await page.locator('[data-page="dashboard"]').click()
            await page.wait_for_timeout(500)
            
            await page.screenshot(path="e2e_screenshots/02_dashboard.png", full_page=True)
            results["steps"].append("02_dashboard.png saved (Dashboard view)")
            
            print("Testing Shipments page...")
            await page.locator('[data-page="shipments"]').click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path="e2e_screenshots/02_shipments.png", full_page=True)
            results["steps"].append("02_shipments.png saved")
            
            print("Testing Tracking page...")
            await page.locator('[data-page="tracking"]').click()
            await page.wait_for_timeout(500)
            await page.fill('#tracking-input', 'PP-DEMO-1001')
            await page.click('#tracking-form button[type="submit"]')
            await page.wait_for_timeout(1000)
            await page.screenshot(path="e2e_screenshots/02_tracking.png", full_page=True)
            results["steps"].append("02_tracking.png saved")
            
            print("Testing Drivers page...")
            await page.locator('[data-page="drivers"]').click()
            await page.wait_for_timeout(500)
            await page.screenshot(path="e2e_screenshots/02_drivers.png", full_page=True)
            results["steps"].append("02_drivers.png saved")
            
            print("Testing Notifications page...")
            await page.locator('[data-page="notifications"]').click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path="e2e_screenshots/02_notifications.png", full_page=True)
            results["steps"].append("02_notifications.png saved")


            results["steps"].append("02_dashboard.png saved (Dashboard view)")
            
            # 3. Look for shipment list
            shipments_count = await page.locator("#recent-shipments-body tr").count()
            results["steps"].append(f"Shipments rendered: {shipments_count}")
            
        except Exception as e:
            results["errors"].append(f"Guest login step failed: {str(e)}")


        print("Clicking logout...")
        await page.click('#logout-btn')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='e2e_screenshots/03_logout.png')
        results['steps'].append('03_logout.png saved (Logout view)')
        await browser.close()

        
    with open("e2e_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run())

import os

path = 'scripts/e2e_clickthrough.py'
with open(path, 'r', encoding='utf-8') as f:
    p = f.read()

replacement = """
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
"""
import re
p = re.sub(r'await page\.screenshot\(path="e2e_screenshots/02_dashboard\.png", full_page=True\)', replacement, p)

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(p)

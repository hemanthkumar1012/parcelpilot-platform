import os

path = 'scripts/e2e_clickthrough.py'
with open(path, 'r', encoding='utf-8') as f:
    p = f.read()

replacement = """
            await page.locator('[data-page="dashboard"]').click()
            await page.wait_for_timeout(500)
            await page.screenshot(path="e2e_screenshots/02_dashboard.png", full_page=True)
"""
p = p.replace('await page.screenshot(path="e2e_screenshots/02_dashboard.png", full_page=True)', replacement)

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(p)

import os

path = 'scripts/e2e_clickthrough.py'
with open(path, 'r', encoding='utf-8') as f:
    p = f.read()

replacement = """
        print("Clicking logout...")
        await page.click('#logout-btn')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='e2e_screenshots/03_logout.png')
        results['steps'].append('03_logout.png saved (Logout view)')
        await browser.close()
"""
p = p.replace("        await browser.close()", replacement)

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(p)

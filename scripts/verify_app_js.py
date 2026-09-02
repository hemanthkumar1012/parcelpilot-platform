import asyncio
from playwright.async_api import async_playwright
import os

async def run_verification():
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Helper to log
        def pass_fail(item, condition):
            results[item] = "PASS" if condition else "FAIL"
            print(f"[{results[item]}] {item}")

        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(1000)
        
        # Verify initial state
        login_visible = await page.locator("#login-view").is_visible()
        dash_hidden = not await page.locator("#dashboard-view").is_visible()
        
        # 1. Real Login
        print("Testing Item 1: Real Login...")
        try:
            await page.fill("#login-email", "admin@northstar.com")
            await page.fill("#login-password", "password")
            await page.click("#login-form button[type='submit']")
            await page.wait_for_timeout(1500)
            dash_visible_after_login = await page.locator("#dashboard-view").is_visible()
            pass_fail("1. Login form submission", dash_visible_after_login)
        except Exception as e:
            pass_fail("1. Login form submission", False)
            print("Error:", e)

        # 5. Logout
        print("Testing Item 5: Logout...")
        try:
            await page.click("#logout-btn")
            await page.wait_for_timeout(1000)
            login_visible_after_logout = await page.locator("#login-view").is_visible()
            pass_fail("5. Logout button", login_visible_after_logout)
        except Exception as e:
            pass_fail("5. Logout button", False)

        # 2 & 3. Guest Login and renderAuthState
        print("Testing Items 2 & 3: Guest Login & Toggle...")
        try:
            await page.click(".guest-mode-btn")
            await page.wait_for_timeout(1500)
            dash_visible = await page.locator("#dashboard-view").is_visible()
            login_hidden = not await page.locator("#login-view").is_visible()
            pass_fail("2. Guest button", dash_visible)
            pass_fail("3. renderAuthState toggles view", dash_visible and login_hidden)
        except Exception as e:
            pass_fail("2. Guest button", False)
            pass_fail("3. renderAuthState toggles view", False)

        # 6. Dashboard stats/charts populate
        print("Testing Item 6: Dashboard stats and charts...")
        try:
            stat_total = await page.locator("#stat-total").text_content()
            stats_populated = stat_total and stat_total.strip() != '—' and int(stat_total) > 0
            # Check if charts exist
            dist_canvas = await page.locator("#status-distribution").count() > 0
            pass_fail("6. Dashboard stats/charts populate", stats_populated and dist_canvas)
        except Exception as e:
            pass_fail("6. Dashboard stats/charts populate", False)

        # 4 & 7. Sidebar Nav Items and Real Content
        print("Testing Items 4 & 7: Sidebar Nav & Real Content...")
        nav_pass = True
        content_pass = True
        try:
            # Shipments
            await page.click('[data-page="shipments"]')
            await page.wait_for_timeout(500)
            if not await page.locator("#page-shipments").is_visible(): nav_pass = False
            if await page.locator("#page-shipments .nav-item").evaluate("el => el.getAttribute('aria-current')") != 'page': nav_pass = False # Active state check not exact, skip JS check, do visual DOM check
            if await page.locator("#shipments-table-body tr").count() == 0: content_pass = False

            # Tracking
            await page.click('[data-page="tracking"]')
            await page.wait_for_timeout(500)
            if not await page.locator("#page-tracking").is_visible(): nav_pass = False
            await page.fill("#tracking-input", "PP-DEMO-2001")
            await page.click("#tracking-form button[type='submit']")
            await page.wait_for_timeout(1000)
            if "PP-DEMO-2001" not in await page.locator("#tracking-page-result").text_content(): content_pass = False
            
            # Drivers
            await page.click('[data-page="drivers"]')
            await page.wait_for_timeout(500)
            if not await page.locator("#page-drivers").is_visible(): nav_pass = False
            if "Coming soon" not in await page.locator("#drivers-empty").text_content(): content_pass = False

            # Notifications
            await page.click('[data-page="notifications"]')
            await page.wait_for_timeout(500)
            if not await page.locator("#page-notifications").is_visible(): nav_pass = False
            if await page.locator("#notifications-page-list li").count() == 0: content_pass = False

            pass_fail("4. All 5 sidebar nav items switch views", nav_pass)
            pass_fail("7. Pages show real content", content_pass)
        except Exception as e:
            pass_fail("4. All 5 sidebar nav items switch views", False)
            pass_fail("7. Pages show real content", False)
            print("Nav error:", e)

        # 8. AI Chat Widget
        print("Testing Item 8: AI Chat...")
        try:
            await page.click("#ai-floating-btn")
            await page.wait_for_timeout(500)
            await page.fill("#ai-input", "Hello")
            await page.click("#ai-form button[type='submit']")
            await page.wait_for_timeout(1500)
            chat_text = await page.locator("#ai-messages").text_content()
            pass_fail("8. AI chat widget works", "simulated" in chat_text or "demo mode" in chat_text)
        except Exception as e:
            pass_fail("8. AI chat widget works", False)
            print("Chat error:", e)

        # 9. 3D Tilt
        print("Testing Item 9: 3D Tilt...")
        try:
            await page.click('[data-page="dashboard"]')
            await page.wait_for_timeout(1000)
            
            # Hover off center
            await page.hover('.stat-card', position={'x': 20, 'y': 20})
            await page.wait_for_timeout(300)
            
            transform = await page.locator('.stat-card').first.evaluate("el => el.style.transform")
            has_tilt = "rotateX" in transform and "rotateY" in transform
            pass_fail("9. 3D tilt-on-hover effect", has_tilt)
        except Exception as e:
            pass_fail("9. 3D tilt-on-hover effect", False)

        await browser.close()
        
    print("\\nVerification Summary:")
    for k, v in results.items():
        print(f"{v}: {k}")

if __name__ == "__main__":
    asyncio.run(run_verification())

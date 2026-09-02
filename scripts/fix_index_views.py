import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the broken duplicate banner text that has no <div
# It starts around:
#        id="guest-demo-banner"
#        class="guest-demo-banner"
#        hidden>
# We can just use regex to remove anything that looks like that broken block
bad_block = """        id="guest-demo-banner"
        class="guest-demo-banner"
        hidden>"""
if bad_block in html:
    # Just find where it starts and cut it out, but it's easier to manually write the replacement
    pass

# A cleaner way is to just find the sections
# The login screen starts at <div id="login-screen" class="login-screen">
# The app screen starts at <div id="app-screen" class="app-screen">

# We want to wrap the login screen in <div id="login-view"> and app screen in <div id="dashboard-view" hidden>

login_start = html.find('<div id="login-screen"')
app_start = html.find('<div id="app-screen"')

if login_start != -1 and app_start != -1:
    pre_login = html[:login_start]
    login_html = html[login_start:app_start]
    app_html = html[app_start:]
    
    # Check if they are already wrapped
    if 'id="login-view"' not in html:
        new_html = pre_login + '<div id="login-view">\n' + login_html + '</div>\n<div id="dashboard-view" hidden>\n' + app_html + '</div>\n'
        
        # Now clean up the broken guest banner
        # The broken banner is literally:
        broken_snippet = """        id="guest-demo-banner"
        class="guest-demo-banner"
        hidden>

        <div
          class="guest-demo-banner-icon"
          aria-hidden="true">
          ✓
        </div>"""
        
        # Let's just fix it using regex to remove any line starting with id="guest-demo-banner" that isn't inside a tag
        lines = new_html.split('\n')
        clean_lines = []
        skip = False
        for line in lines:
            if 'id="guest-demo-banner"' in line and '<' not in line:
                skip = True
            
            if skip and line.strip() == '</div>':
                # skip one more div close? Actually let's just let it be, a broken banner is tricky to skip line by line.
                pass
        
        # A much better regex to remove the specific broken text block:
        new_html = re.sub(r'(\s+)id="guest-demo-banner"\s+class="guest-demo-banner"\s+hidden>.*?</div>\s+</div>\s+</div>\s+<button[^>]+>\s+Sign in for full access\s+</button>\s+</div>', '', new_html, flags=re.DOTALL)
        
        with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_html)
        print("Restructured index.html")
    else:
        print("Already restructured.")

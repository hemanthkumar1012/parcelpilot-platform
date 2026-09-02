import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean backticks
html = html.replace('```', '')

# 2. Wrap views
login_match = re.search(r'<div\s+id="login-screen"', html)
app_match = re.search(r'<div\s+id="app-screen"', html)

if login_match and app_match and 'id="login-view"' not in html:
    login_start = login_match.start()
    app_start = app_match.start()
    
    pre_login = html[:login_start]
    login_html = html[login_start:app_start]
    app_html = html[app_start:]
    
    html = pre_login + '<div id="login-view">\n' + login_html + '</div>\n<div id="dashboard-view" hidden>\n' + app_html + '</div>\n'
    print("Wrapped views")

# 3. Fix the broken HTML tag near guest-demo-banner.
# The broken chunk starts with <div <!-- and has `id="guest-demo-banner"` without `<`
# Let's just find `        id="guest-demo-banner"\n        class="guest-demo-banner"\n        hidden>` and remove the block
broken_regex = r'\s+id="guest-demo-banner"\s+class="guest-demo-banner"\s+hidden>.*?Sign in for full access\s+</button>\s+</div>'
html = re.sub(broken_regex, '', html, flags=re.DOTALL)

# Fix the `<div <!-- ============================= RECRUITER DEMO BANNER ============================= -->`
html = html.replace('<div <!-- ============================= RECRUITER DEMO BANNER ============================= -->', '<!-- ============================= RECRUITER DEMO BANNER ============================= -->')

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Done fixing index.html")

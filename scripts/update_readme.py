import os

readme_path = 'README.md'
with open(readme_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('python -m scripts.seed_ai_data', 'python scripts/seed_demo.py')
with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print("Updated README.md")

#!/usr/bin/env python3
"""Add h3 sub-links to sidebar navigation and add IDs to h3 elements."""
import re

# Read file
with open('claude-code-guide.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add sub-link CSS if not present
if '.sub-link' not in html:
    sublink_css = """
  .sidebar a.sub-link { padding-left: 16px; font-weight: 400; margin-top: 4px; font-size: 13px; color: var(--text-secondary); }
  .sidebar a.sub-link:hover { color: var(--accent); }
"""
    html = html.replace(
        '.sidebar a.section-link { font-weight: 600; color: var(--text); margin-top: 12px; font-size: 14px; }',
        '.sidebar a.section-link { font-weight: 600; color: var(--text); margin-top: 12px; font-size: 14px; }' + sublink_css
    )
    print("Added sub-link CSS")

# 2. Add IDs to h3 elements that don't have them
def add_h3_id(match):
    tag = match.group(0)
    if 'id=' in tag:
        return tag
    text = match.group(1)
    # Generate ID from text
    h3_id = re.sub(r'[^\w\s-]', '', text.lower())
    h3_id = re.sub(r'[\s]+', '-', h3_id).strip('-')
    return f'<h3 id="{h3_id}">{text}</h3>'

html = re.sub(r'<h3>(.*?)</h3>', add_h3_id, html)
print("Added IDs to h3 elements")

# 3. Extract all h2 and h3 headings with their IDs
h2_pattern = r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>'
h3_pattern = r'<h3[^>]*id="([^"]*)"[^>]*>(.*?)</h3>'

# Build a list of (h2_id, h2_text, [h3_texts])
lines = html.split('\n')
h2_sections = []
current_h2 = None
current_h2_text = None
current_h3s = []

for line in lines:
    h2_match = re.search(h2_pattern, line)
    h3_match = re.search(h3_pattern, line)

    if h2_match:
        if current_h2:
            h2_sections.append((current_h2, current_h2_text, current_h3s))
        current_h2 = h2_match.group(1)
        current_h2_text = re.sub(r'<[^>]+>', '', h2_match.group(2)).strip()
        current_h3s = []
    elif h3_match and current_h2:
        h3_id = h3_match.group(1)
        h3_text = re.sub(r'<[^>]+>', '', h3_match.group(2)).strip()
        current_h3s.append((h3_id, h3_text))

if current_h2:
    h2_sections.append((current_h2, current_h2_text, current_h3s))

print(f"Found {len(h2_sections)} h2 sections with sub-sections")

# 4. Build new sidebar navigation
sidebar_lines = []
for h2_id, h2_text, h3s in h2_sections:
    sidebar_lines.append(f'  <a href="#{h2_id}" class="section-link">{h2_text}</a>')
    for h3_id, h3_text in h3s:
        sidebar_lines.append(f'  <a href="#{h3_id}" class="sub-link">{h3_text}</a>')

sidebar_html = '\n'.join(sidebar_lines)

# 5. Replace the sidebar content
sidebar_pattern = r'(<nav class="sidebar">.*?)</nav>'
sidebar_match = re.search(sidebar_pattern, html, re.DOTALL)

if sidebar_match:
    old_sidebar = sidebar_match.group(0)
    title_match = re.search(r'(<div class="sidebar-title">.*?</div>\s*<a href="index\.html"[^>]*>.*?</a>)', old_sidebar, re.DOTALL)
    if title_match:
        prefix = title_match.group(1)
    else:
        prefix = '<div class="sidebar-title">📖 目录导航</div>'

    new_sidebar = f'''<nav class="sidebar">
{prefix}
{sidebar_html}
</nav>'''

    html = html.replace(old_sidebar, new_sidebar)
    print("Updated sidebar navigation")

# Write back
with open('claude-code-guide.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")

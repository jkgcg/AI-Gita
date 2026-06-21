import re, os

html_path = r'c:\Users\girijyo\OneDrive - adidas\Desktop\Work\AI Learning\AI_Gita.html'
panels_dir = r'c:\Users\girijyo\OneDrive - adidas\Desktop\Work\AI Learning\html_panels'

PANELS = ['tab-llm', 'tab-math', 'tab-infra', 'tab-rag', 'tab-agents']

with open(html_path, encoding='utf-8') as f:
    html = f.read()

print(f'Original size: {len(html):,} chars')

# Find all panel regions
panel_starts = list(re.finditer(r'<div id="tab-(\w+)" class="panel[^"]*">', html))

# Build a map of id -> (start, end, opening_tag)
# end = position just after the closing </div> that closes the panel's own div
# We'll find it by div-balancing
def find_panel_end(html, open_pos, open_tag_end):
    """Return position just after the </div> that closes the panel's outermost div."""
    depth = 1
    pos = open_tag_end
    while pos < len(html) and depth > 0:
        next_open = html.find('<div', pos)
        next_close = html.find('</div>', pos)
        if next_close < 0:
            break
        if next_open >= 0 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                return next_close + len('</div>')
            pos = next_close + len('</div>')
    return -1

replaceable = []
for m in panel_starts:
    tid = m.group(1)
    if tid not in [p.replace('tab-', '') for p in PANELS]:
        continue
    start = m.start()
    open_tag_end = m.end()
    opening_tag = m.group(0)
    end = find_panel_end(html, start, open_tag_end)
    if end < 0:
        print(f'WARNING: could not find end of panel {tid}')
        continue
    replaceable.append((tid, start, end, opening_tag))
    print(f'  Found {tid}: chars {start}–{end} (len {end-start:,})')

print(f'\nReplacing {len(replaceable)} panels...')
replaceable.sort(key=lambda x: x[1], reverse=True)

for tid, start, end, opening_tag in replaceable:
    panel_file = os.path.join(panels_dir, f'tab-{tid}.html')
    if not os.path.exists(panel_file):
        print(f'  SKIP {tid}: file not found at {panel_file}')
        continue
    with open(panel_file, encoding='utf-8') as f:
        new_content = f.read().strip()
    replacement = opening_tag + '\n\n' + new_content + '\n\n</div>'
    html = html[:start] + replacement + html[end:]
    print(f'  Replaced {tid}: new len {len(replacement):,}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone. New file size: {len(html):,} chars ({len(html)//1024} KB)')
